import os
import sys
import copy
import time
import csv
import numpy as np
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS'] = pow(2, 40).__str__()
import cv2
from utils import calc_overlap, save_crop_images, crop_images, listup_files, COLOR


# constant setting. / color, font
COLOR    = COLOR
STR_FONT = cv2.FONT_HERSHEY_SIMPLEX


class TrainTestSplit:
    """
    == DESCRIPTION ==
    input : dataset directory (path)
            save directory (path)
            train:test ratio (float)
    :return : train.txt, val.txt
    =================
    usage:
    datadir=./Train
    savedir=./Save
    ratio=0.8
    fileform=jpg
    =================
    output example:
    TRAIN DATA NAME >> image01.jpg
    ...
    TEST DATA NAME >> image02.jpg
    ...
    TRAIN DATA >> 80 files
    TEST DATA >> 20 files
    SAVE FILE >> ./train.txt, ./val.txt
    """
    def __init__(self, config: dict):#datadir, savedir, ratio):
        self.datadir  = config["datadir"]
        self.savedir  = config["savedir"]
        self.ratio    = config["ratio"]
        self.fileform = config["fileform"]

    def split(self):
        files = listup_files(self.datadir)
        files_copy = copy.deepcopy(files)
        num_of_files: int = len(files)  # number of dataset's files

        # 전역변수 선언
        global files_train, files_test

        # train set
        files_train = np.random.choice(files, int(num_of_files * self.ratio), False)
        files_train.sort()  # train set 오름차순 정렬
        for file in files_train:
            if file in files_copy:
                files_copy.remove(file)
        # test set
        files_test = files_copy

    def write(self):
        abs_path = os.path.abspath(self.datadir)
        with open(f'{self.savedir}/train.txt', 'w') as f:
            for file in files_train:
                f.write(f'{abs_path}\{file}.{self.fileform}\n')
                print(f'TRAIN DATA NAME >> {file}.{self.fileform}')

        with open(f'{self.savedir}/val.txt', 'w') as f:
            for file in files_test:
                f.write(f'{abs_path}\{file}.{self.fileform}\n')
                print(f'TEST DATA NAME >> {file}.{self.fileform}')

        print(f'TRAIN DATA >> {len(files_train)} files')
        print(f'TEST DATA >> {len(files_test)} files')
        print(f'SAVE FILE >> {self.savedir}train.txt, {self.savedir}val.txt')


class CropImages:
    """
    """


class MultipleTemplateMatching:
    """
    """


class DetectByYolo:
    """
    """


class DetectCropByYolo:
    """
    """


traintestsplit = TrainTestSplit(
    {
        "datadir" : input('datadir='),
        "savedir" : input('savedir='),
        "ratio"   : float(input('ratio=')),
        "fileform": input('fileform=')
    },
)
traintestsplit.split()
traintestsplit.write()