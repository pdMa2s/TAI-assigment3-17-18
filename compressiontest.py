import gzip


def compress_file():
    return gzip.compress(open('orl_faces/s01/01.pgm', 'rb').read())


if __name__ == '__main__':
    print(len(compress_file()))