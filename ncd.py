class NCD:
    def __init__(self, target_files, ref_files, compressor):
        self.target_files = target_files
        self.ref_files = ref_files
        self.compressor = compressor
        self.pairs_compress_size = self.generate_pairs()
        self.array_files_ncd = {}
        self.calculate_pair_ncd()

    def generate_pairs(self):
        compression = {}
        for ref in self.ref_files:
            for tar in self.target_files:
                reference_content = [element for element in self.ref_files if element == ref][0].content
                target_content = [element for element in self.target_files if element == tar][0].content
                content = reference_content + target_content
                compression[(ref, tar)] = len(self.compressor(content))
        return compression

    def calculate_pair_ncd(self):
        for x, y in self.pairs_compress_size:
            compressed_x = [ref for ref in self.ref_files if ref == x][0].compress_file_size
            compressed_y = [tar for tar in self.target_files if tar == y][0].compress_file_size
            compressed_pair = self.pairs_compress_size[(x, y)]
            ncd = (compressed_pair - min([compressed_x, compressed_y])) / max([compressed_x, compressed_y])
            self.array_files_ncd[(x, y)] = ncd

    def get_array_files_ncd(self):
        return self.array_files_ncd
