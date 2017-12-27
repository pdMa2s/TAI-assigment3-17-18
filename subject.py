from os import listdir, path

class Subject():

    def __init__(self, folder_subject, num_ref_files):
        self.folder_subject = folder_subject
        self.id_subject = str(path.basename(folder_subject))
        self.num_ref_files = num_ref_files
        self.array_ref_files_content = []
        self.read_subject_files()

    def read_subject_files(self):
        all_files = [path.join(self.folder_subject,f) for f in listdir(self.folder_subject) if path.isfile(path.join(self.folder_subject, f))]
        for i in range(len(all_files[:self.num_ref_files])):
            content = open(all_files[i], 'rb').read()
            self.array_ref_files_content.append(content)

    def __str__(self) -> str:
        return str(self.id_subject)



