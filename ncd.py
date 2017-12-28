class NCD:
    def __init__(self, target_files, ref_files, compressor):
        self.target_files = target_files
        self.ref_files = ref_files
        self.compressor = compressor
        """self.pairs_compress_size = self.generate_pairs()
        self.array_files_ncd = {}
        self.calculate_pair_ncd()"""


    """def generate_pairs(self):
        compression = {}
        for ref in self.ref_files:
            for tar in self.target_files:
                reference_content = ref.content
                target_content = tar.content
                content = reference_content + target_content
                compression[(ref, tar)] = len(self.compressor(content))
        return compression"""

    """def calculate_pair_ncd(self):
        for x, y in self.pairs_compress_size:
            compressed_x = x.compress_file_size
            compressed_y = y.compress_file_size

            compressed_pair = self.pairs_compress_size[(x, y)]
            ncd = self.ncd(compressed_pair, compressed_x, compressed_y)
            self.array_files_ncd[(x, y)] = ncd"""

    def mean_ncd(self):
        ref_totals = {}
        for targ in self.target_files:
            y = targ.compress_file_size
            for ref in self.ref_files:
                concat_size = len(self.compressor(ref.content + targ.content))
                x = ref.compress_file_size
                ncd = self.ncd(concat_size,x, y)
                if ref in ref_totals:
                    ref_totals[ref] += ncd
                else:
                    ref_totals[ref] = ncd
        return [total/(len(self.target_files)) for r, total in ref_totals.items()]

    """def get_array_files_ncd(self):
        return self.array_files_ncd"""

    def ncd(self, concat, x, y):
        return (concat - min(x, y)) / max(x, y)