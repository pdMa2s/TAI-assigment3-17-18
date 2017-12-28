from os import listdir, path

class Subject():

    def __init__(self, subject_id):
        self.id_subject = subject_id
        self.test_files = []

    def __str__(self) -> str:
        return self.id_subject

    def __repr__(self):
        return self.id_subject

    def add_test_file(self, file):
        self.test_files.append(file)