from os import listdir, path

class Subject():

    def __init__(self, subject_id):
        self.id_subject = subject_id
        self.test_files = []
        self.candidates = []
        self.accuracy = 0

    def __str__(self) -> str:
        return self.id_subject

    def __repr__(self):
        return self.id_subject

    def add_test_file(self, file):
        self.test_files.append(file)

    def add_candidate(self,candidate):
        self.candidates.append(candidate)

    def set_accuracy(self, accuracy):
        self.accuracy = accuracy

    def print_statistics(self):
        return str(self.id_subject) + " " + str(self.candidates) + " Accuracy: "+str(self.accuracy) +"%"