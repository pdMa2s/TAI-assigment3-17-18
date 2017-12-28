import argparse
import bz2
import gzip
import lzma
import zlib
from image_file import ImageFile
from ncd import NCD
import os
from subject import Subject


def compress_file_gzip(content):
    return gzip.compress(content)


def compress_file_bz2(content):
    return bz2.compress(content)


def compress_file_lzma(content):
    return lzma.compress(content)


def compress_file_zlib(content):
    return zlib.compress(content, level=9)


def read_file_content(file_path):
    return open('orl_faces/'+ file_path, 'rb').read()


def parse_compressor(c_name):
    compressors = {'gzip': compress_file_gzip,
                   'bzip2': compress_file_bz2,
                   'lzma': compress_file_lzma,
                   'zip': compress_file_zlib}
    return compressors[c_name]


def is_directory(directory):
    if not os.path.isdir(directory):
        parser.error("The directory %s does not exist!" % directory)
    return directory


def create_refs_and_subjects(directory_in_str, compressor):
    refs = {}
    subjects = []
    general_directory = os.fsencode(directory_in_str)

    for dir in os.listdir(general_directory):
        dir_name = os.fsdecode(dir)
        sub_dir = os.path.join(directory_in_str, dir_name)
        if os.path.isdir(sub_dir):
            imgs = os.listdir(sub_dir)
            imgs.sort()
            image_files = []
            new_subject = Subject(dir_name)

            for i in imgs:
                img_dir = os.path.join(sub_dir, i)
                file = ImageFile(img_dir, compressor)
                if len(image_files) < 3:
                    image_files.append(file)
                new_subject.add_test_file(file)
            refs[dir_name] = image_files
            subjects.append(new_subject)
    return refs, subjects


def handle_means(means):
    return sum(means)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory that contains the image files", type=is_directory)
    parser.add_argument("compressor", help="compressor to be used", choices=['gzip', 'bzip2', 'lzma', 'zip'])
    args = parser.parse_args()

    compressor = parse_compressor(args.compressor)
    references, subjects = create_refs_and_subjects(args.directory, compressor)

    test_results = {}
    for ref in references:
        test_results[ref] = []
        for sub in subjects:
            means = NCD(sub.test_files, references[ref], compressor).mean_ncd()
            test_results[ref] += means
    #print(test_results)

    dic_min = {}
    for subject, list_results in test_results.items():
        for image, ndc in list_results:
            value = (subject, ndc)
            if image in dic_min.keys():
                value = dic_min[image]
                if value[1] > ndc:
                    dic_min[image] = (subject, ndc)
            else:
                dic_min[image] = (subject, ndc)

    print(dic_min)

    for sub in subjects:
        [sub.add_candidate(list_subject_min_ndc[0]) for image, list_subject_min_ndc in dic_min.items()
                          if image in sub.test_files]
        print(sub.id_subject,sub.candidates)
