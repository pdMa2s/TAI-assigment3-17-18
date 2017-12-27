import argparse
import bz2
import gzip
import lzma
import zlib
from os import listdir, path
from itertools import product

from image_file import ImageFile
from ncd import NCD

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("compressor", help="compressor to be used", choices=['gzip', 'bzip2', 'lzma', 'zip'])
    args = parser.parse_args()

    compressor_name = args.compressor
    compressors = {'gzip': compress_file_gzip,
                   'bzip2': compress_file_bz2,
                   'lzma': compress_file_lzma,
                   'zip': compress_file_zlib}
    compressor = compressors[compressor_name]

    list_dir = [path.join("orl_faces", f) for f in listdir("orl_faces") if path.isdir(path.join("orl_faces", f))]
    list_dir.sort()

    all_target_files = [ImageFile(path.join(dir, f), compressor) for dir in list_dir for f in listdir(dir) if path.isfile(path.join(dir, f))]
    all_target_files.sort(key=lambda x: x.folder)

    list_subject = []
    inittial_files = 0
    final_files = 3
    for dir in list_dir:
        list_ref_files = [image_file for image_file in all_target_files[inittial_files:final_files]]
        subject = Subject(dir, 3, list_ref_files)
        list_subject.append(subject)
        inittial_files += 10
        final_files += 10
    for i in list_subject:
        print(i)
    """
    file_content = read_file_content("s01/01.pgm")

    print("original:", len(file_content))

    print("Target files:", all_target_files)
    #all_target_combinations = list(product(all_target_files, repeat=2))

    for c_name, compressor in compressors.items():
        print("compressor " + c_name + ": " + str(len(compressor(file_content))))
        list_subject = []
        for dir in list_dir:
            subject = Subject(dir, 3, compressor)
            list_subject.append(subject)
        print(list_subject[1])
        break

    #ncd = NCD(all_target_files, all_target_combinations, compressors['gzip'])
    #res = ncd.get_array_files_ncd()
    #print(res)
    #print("{}: {}".format('gzip', res[('orl_faces/s22/05.pgm', 'orl_faces/s22/05.pgm')]))
    """