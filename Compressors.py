import bz2
import gzip
import lzma
import zlib
from io import BytesIO


def compress_file_gzip(content,compression_level=9):
    return gzip.compress(content, compresslevel=compression_level)


def compress_file_bz2(content, compression_level=9):
    return bz2.compress(content, compresslevel=compression_level)


def compress_file_lzma(content):
    return lzma.compress(content)


def compress_file_zlib(content, compression_level=9):
    return zlib.compress(content, level=compression_level)


def compress_file_jpeg_png(image, type):
    buffer = BytesIO()
    image.save(buffer, type)
    return buffer.tell()


def parse_compressor(c_name):
    compressors = {'gzip': compress_file_gzip,
                   'bzip2': compress_file_bz2,
                   'lzma': compress_file_lzma,
                   'zlib': compress_file_zlib,
                   'jpeg': compress_file_jpeg_png,
                   'png': compress_file_jpeg_png}
    return compressors[c_name]
