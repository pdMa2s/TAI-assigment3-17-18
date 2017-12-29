class Subject:

    def __init__(self, subject_id):
        self.id_subject = subject_id
        self.test_files = []
        self.candidates = []
        self.accuracy = -1
        self.recall = -1

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

    def set_recall(self, recall):
        self.recall = recall

    def print_statistics(self):
        return str(self.id_subject) + " " + str(self.candidates) + " Recall: "\
               + str.format('%.2f' % self.recall) + "%" + " Accuracy: "\
               + str.format('%.2f' % self.accuracy) + "%"
