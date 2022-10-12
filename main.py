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
            file format (txt)
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
    PROCESS FINISHED
    """
    def __init__(self, config: dict):
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
        print('PROCESS FINISHED')


class CropImage:
    """
    == DESCRIPTION ==
    input : image directory (path)
            crop save directory (path)
            crop size (int)
            file format (txt)
            target image's channel (bool)
    :return : cropped images
    =================
    usage:
    datadir=./Data
    savedir=./Save
    cropsize=416
    countx=10
    county=10
    fileform=jpg
    =================
    output example:
    IMAGE NAME >> image01.jpg
    CROP SIZE >> 416
    CROP IMAGE NAME >> image01-01-01.jpg
    CROP IMAGE NAME >> image01-01-02.jpg
    ...
    IMAGE NAME >> image02.jpg
    CROP SIZE >> 416
    CROP IMAGE NAME >> image02-01-01.jpg
    CROP IMAGE NAME >> image02-01-02.jpg
    ...
    PROCESS FINISHED
    """
    def __init__(self, config: dict):
        self.datadir  = config["datadir"]
        self.savedir  = config["savedir"]
        self.cropsize = config["cropsize"]
        self.countx  = config["countx"]
        self.county  = config["county"]
        self.fileform = config["fileform"]

    def write_crop(self):
        files = listup_files(self.datadir)
        for file in files:
            src = cv2.imread(f'{self.datadir}/{file}.{self.fileform}', cv2.IMREAD_ANYCOLOR)
            print(f'IMAGE NAME >> {file}.{self.fileform}')
            print(f'CROP SIZE >> {self.cropsize}')
            save_crop_images(src, self.savedir, file, self.cropsize, self.countx, self.county, self.fileform)
        print('PROCESS FINISHED')


class TemplateMatching:
    """
    """


class DetectByYolo:
    """
    """


class DetectCropByYolo:
    """
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
"""
cropimage = CropImage(
    {
        "datadir"  : input('datadir='),
        "savedir"  : input('savedir='),
        "cropsize" : int(input('cropsize=')),
        "countx"   : int(input('countx=')),
        "county"   : int(input('county=')),
        "fileform" : input('fileform=')
    }
)
cropimage.write_crop()