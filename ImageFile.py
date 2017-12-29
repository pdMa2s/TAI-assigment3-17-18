#from PIL import Image


class ImageFile:
    def __init__(self, folder, compressor, compressor_type):
        self.folder = folder
        self.content_image = self.read_image(compressor, compressor_type)
        self.compress_file_size = self.get_compress_size(compressor, compressor_type)

    def __str__(self) -> str:
        return self.folder

    def __repr__(self) -> str:
        return self.__str__()

    def read_image(self, compressor, compressor_type):
        #if compressor_type == 'png' or compressor_type == 'jpeg':
            #return Image.open(self.folder)
        return open(self.folder, 'rb').read()

    def get_compress_size(self, compressor, compressor_type):
        if compressor_type == 'png' or compressor_type == 'jpeg':
            return compressor(self.content_image, compressor_type)
        return len(compressor(self.content_image))



