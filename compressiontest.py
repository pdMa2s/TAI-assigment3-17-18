import bz2
import gzip
import lzma
import zlib
from os import listdir, path

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
    list_dir = [path.join("orl_faces",f) for f in listdir("orl_faces") if path.isdir(path.join("orl_faces", f))]
    print(list_dir)

    file_content = read_file_content("s01/01.pgm")
    compressors = {'gzip': compress_file_gzip,
                   'bz2': compress_file_bz2,
                   'lzma': compress_file_lzma,
                   'zlib': compress_file_zlib}
    print("original:", len(file_content))

    for c_name, compressor in compressors.items():
        print("compressor " + c_name + ": " + str(len(compressor(file_content))))
        list_subject = []
        for dir in list_dir:
            subject = Subject(dir, 3, compressor)
            list_subject.append(subject)
        print(list_subject[0])