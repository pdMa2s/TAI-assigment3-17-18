from os import listdir, path

class Subject():

    def __init__(self, folder_subject, num_ref_files, list_ref_files):
        self.folder_subject = folder_subject
        self.id_subject = str(path.basename(folder_subject))
        self.num_ref_files = num_ref_files
        self.array_ref_files = list_ref_files

    def __str__(self) -> str:
        return str(self.id_subject)+str([image_file.folder for image_file in self.array_ref_files])



