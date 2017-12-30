import numpy as np
from PIL import Image


class NCD:
    def __init__(self, target_files, ref_files, compressor, compressor_type, subject_classif_type):
        self.target_files = target_files
        self.ref_files = ref_files
        self.compressor = compressor
        self.compressor_type = compressor_type
        self.subject_classif_type = subject_classif_type

    def compute_ncd(self):
        list_ncd_mean = []
        for targ in self.target_files:
            y = targ.compress_file_size
            if self.subject_classif_type == "mean":
                ncd_total = self.compute_mean_ncd(targ, y)
            else:
                ncd_total = self.compute_ncd_from_super_image(targ, y)
            list_ncd_mean.append((targ, ncd_total))
        return list_ncd_mean

    def ncd(self, concat, x, y):
        return (concat - min(x, y)) / max(x, y)

    def concate_images(self, list_images):
        imgs_comb = np.hstack((np.asarray(i) for i in list_images))
        imgs_comb = Image.fromarray(imgs_comb)
        return imgs_comb

    def compute_mean_ncd(self, targ, y):
        ncd_total = 0
        for ref in self.ref_files:
            if self.compressor_type == 'jpeg' or self.compressor_type == 'png':
                concat_size = self.compressor(self.concate_images([ref.content_image, targ.content_image]),
                                              self.compressor_type)
            else:
                concat_size = len(self.compressor(ref.content_image + targ.content_image))
            x = ref.compress_file_size
            ncd = self.ncd(concat_size, x, y)
            ncd_total += ncd
        ncd_total /= len(self.ref_files)
        return ncd_total

    def compute_ncd_from_super_image(self, targ, y):
        if self.compressor_type == 'jpeg' or self.compressor_type == 'png':
            list_images_ref = [image_ref.content_image for image_ref in self.ref_files]
            imgs_comb = self.concate_images(list_images_ref)
            x = self.compressor(imgs_comb, self.compressor_type)
            list_images_ref_targ = list_images_ref + [targ.content_image]
            imgs_comb_ref_targ = self.concate_images(list_images_ref_targ)
            concat = self.compressor(imgs_comb_ref_targ, self.compressor_type)
        else:
            concatenate_reg_files = bytearray()
            for ref in self.ref_files:
                concatenate_reg_files.extend(ref.content_image)
            x = len(self.compressor(concatenate_reg_files))
            concat = len(self.compressor(concatenate_reg_files + targ.content_image))
        return self.ncd(concat, x, y)