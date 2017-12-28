import argparse
import bz2
import gzip
import lzma
import zlib
from os import listdir, path
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
    if not path.isdir(directory):
        parser.error("The directory %s does not exist!" % directory)
    return directory


def create_refs_and_subjects(directory_in_str, compressor):
    refs = {}
    subjects = []
    general_directory = os.fsencode(directory_in_str)

    for dir in os.listdir(general_directory):
        dir_name = os.fsdecode(dir)
        sub_dir = path.join(directory_in_str, dir_name)
        if os.path.isdir(sub_dir):
            imgs = os.listdir(sub_dir)
            imgs.sort()
            image_files = []
            new_subject = Subject(dir_name)

            for i in imgs:
                img_dir = path.join(sub_dir, i)
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

    list_dir = [path.join(args.directory, f) for f in listdir(args.directory) if path.isdir(path.join(args.directory, f))]
    list_dir.sort()

    #all_target_files = [ImageFile(path.join(dir, f), compressor) for dir in list_dir for f in listdir(dir) if path.isfile(path.join(dir, f))]
    #all_target_files.sort(key=lambda x: x.folder)
    #all_reference_files = [[image_file for image_file in all_target_files if path.basename(dir) == path.basename(path.dirname(image_file.folder))][:3] for dir in list_dir]

    test_results = {}
    for ref in references:
        test_results[ref] = []
        for sub in subjects:
            means = NCD(sub.test_files, references[ref], compressor).mean_ncd()
            processed_means = handle_means(means)
            test_results[ref].append((sub, processed_means))

    print(test_results)

