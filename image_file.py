
class ImageFile:

    def __init__(self, folder, compressor):
        self.folder = folder
        self.content = open(folder, 'rb').read()
        self.compress_file_size = len(compressor(self.content))

    def __str__(self) -> str:
        return self.folder

    def __repr__(self) -> str:
        return self.__str__()



