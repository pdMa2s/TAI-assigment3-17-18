class NCD:
    def __init__(self, target_files, target_files_combinations, compressor):
        self.compressor = compressor
        self.compressed_files = {}
        self.compress_files(target_files)
        self.target_files_combinations = target_files_combinations
        self.array_files_ncd = {}
        self.calculate_pair_ncd()

    def compress_files(self, files):
        for file in files:
            content = open(file, 'rb').read()
            self.compressed_files[file] = self.compressor(content)

    def calculate_pair_ncd(self):
        for x, y in self.target_files_combinations:
            compressed_x = len(self.compressed_files[x])
            compressed_y = len(self.compressed_files[y])
            compressed_pair = len(self.compressor(self.compressed_files[x] + self.compressed_files[y]))
            ncd = (compressed_pair - min([compressed_x, compressed_y])) / max([compressed_x, compressed_y])
            self.array_files_ncd[(x, y)] = ncd

    def get_array_files_ncd(self):
        return self.array_files_ncd
