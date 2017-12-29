import numpy as np
from PIL import Image


class NCD:
    def __init__(self, target_files, ref_files, compressor, compressor_type):
        self.target_files = target_files
        self.ref_files = ref_files
        self.compressor = compressor
        self.compressor_type = compressor_type

    def mean_ncd(self):
        list_ncd_mean = []
        for targ in self.target_files:
            y = targ.compress_file_size
            ncd_total = 0
            for ref in self.ref_files:
                concat_size = 0
                if self.compressor_type == 'jpeg' or self.compressor_type == 'png':
                    concat_size = self.compressor(self.concate_images(ref.content_image, targ.content_image), self.compressor_type)
                else:
                    concat_size = len(self.compressor(ref.content_image + targ.content_image))
                x = ref.compress_file_size
                ncd = self.ncd(concat_size,x, y)
                ncd_total += ncd
            ncd_total /= len(self.ref_files)
            list_ncd_mean.append((targ, ncd_total))
        return list_ncd_mean

    def ncd(self, concat, x, y):
        return (concat - min(x, y)) / max(x, y)

    def concate_images(self, image1, image2):
        imgs_comb = np.hstack((np.asarray(i) for i in [image1, image2]))
        imgs_comb = Image.fromarray(imgs_comb)
        return imgs_comb