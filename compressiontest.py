import argparse
import bz2
import gzip
import lzma
import zlib
import re
from image_file import ImageFile
from ncd import NCD
import os
from subject import Subject


def compress_file_gzip(content):
    return gzip.compress(content)


def compress_file_bz2(content):
    return bz2.compress(content)


def compress_file_lzma(content):
    return lzma.compress(content)


def compress_file_zlib(content):
    return zlib.compress(content, level=9)


def read_file_content(file_path):
    return open('orl_faces/'+ file_path, 'rb').read()


def parse_compressor(c_name):
    compressors = {'gzip': compress_file_gzip,
                   'bzip2': compress_file_bz2,
                   'lzma': compress_file_lzma,
                   'zip': compress_file_zlib}
    return compressors[c_name]


def is_directory(directory):
    if not os.path.isdir(directory):
        parser.error("The directory %s does not exist!" % directory)
    return directory


def create_refs_and_subjects(directory_in_str, compressor):
    refs = {}
    subjects = []
    general_directory = os.fsencode(directory_in_str)

    for dir in os.listdir(general_directory):
        dir_name = os.fsdecode(dir)
        sub_dir = os.path.join(directory_in_str, dir_name)
        if os.path.isdir(sub_dir):
            imgs = os.listdir(sub_dir)
            imgs.sort()
            image_files = []
            new_subject = Subject(dir_name)

            for i in imgs:
                img_dir = os.path.join(sub_dir, i)
                file = ImageFile(img_dir, compressor)
                if len(image_files) < 3:
                    image_files.append(file)
                new_subject.add_test_file(file)
            refs[dir_name] = image_files
            subjects.append(new_subject)
    return refs, subjects


def handle_means(means):
    return sum(means)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory that contains the image files", type=is_directory)
    parser.add_argument("compressor", help="compressor to be used", choices=['gzip', 'bzip2', 'lzma', 'zip'])
    args = parser.parse_args()

    compressor = parse_compressor(args.compressor)
    references, subjects = create_refs_and_subjects(args.directory, compressor)

    test_results = {}
    for ref in references:
        test_results[ref] = []
        for sub in subjects:
            means = NCD(sub.test_files, references[ref], compressor).mean_ncd()
            test_results[ref] += means
    #print(test_results)

    dic_min = {}
    for subject, list_results in test_results.items():
        for image, ncd in list_results:
            if image in dic_min.keys():
                value = dic_min[image][1]
                if value > ncd:
                    dic_min[image] = (subject, ncd)
            else:
                dic_min[image] = (subject, ncd)

    #print(dic_min)

    matrix_confusion = [[0 for i in range(len(subjects))] for j in range(len(subjects))]
    for sub in subjects:
        all_test_file_of_subject = [list_subject_min_ncd[0] for image, list_subject_min_ncd in dic_min.items()
                          if image in sub.test_files]
        print(all_test_file_of_subject)
        for candidate in all_test_file_of_subject:
            sub.add_candidate(candidate)
            subject_predicted_id = int(re.search(r'\d+', candidate).group())
            subject_real_id = int(re.search(r'\d+', sub.id_subject).group())
            matrix_confusion[subject_predicted_id-1][subject_real_id-1] += 1

    print(matrix_confusion)

    total = sum([sum(f) for f in matrix_confusion])
    avg_accuracy = 0
    for i in range(len(subjects)):
        tp = matrix_confusion[i][i]
        fp = sum(matrix_confusion[i])-tp
        fn = sum([d[0] for d in matrix_confusion])-tp
        tn = total - (tp+fp+fn)
        accuracy_subject = ((tp+tn)/total)*100
        subjects[i].set_accuracy(accuracy_subject)
        print(subjects[i].print_statistics())
        avg_accuracy += accuracy_subject
    print("Average accuracy: "+str.format('%.2f' % float(avg_accuracy/len(subjects)))+"%")
