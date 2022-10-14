import os
import pathlib
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
            image file format (str)
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
        self.countx   = config["countx"]
        self.county   = config["county"]
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
    == DESCRIPTION ==
    input : (path)
    :return : 
    =================
    usage:
    models=./models
    =================
    output example:

    PROCESS FINISHED
    """


class DetectByYolo:
    """
    """


class DetectCropByYolo:
    """
    == DESCRIPTION ==
    input : model file name (path)
            crop size (int)
            x crop count (int)
            y crop count (int)
            image file format (str)
            confidence threshold (float)
            running device (str)
    :return : Yolo test results (image, txt)
    =================
    usage:
    models=./models
    cropsize=416
    countx=10
    county==10
    fileform=jpg
    confTH=0.8
    device=gpu
    =================
    output example:
    CONFIG, WEIGHTS, NAMES FILE LOADING
    CONFIG, WEIGHTS, NAMES FILE LOAD DONE

    MODEL FILE LOADING
    MODEL FILE LOAD DONE

    DETECT BEGINS
    image01_01-01.jpg >> CROP DETECT TIME : 00.00 sec.
    ...
    image01.jpg >> IMAGE DETECT TIME : 00.00 sec.
    TOTAL DETECT TIME : 00.00 sec.

    PROCESS FINISHED
    """
    def __init__(self, config: dict):
        self.models   = config["models"]
        self.cropsize = config["cropsize"]
        self.countx   = config["countx"]
        self.county   = config["county"]
        self.fileform = config["fileform"]
        self.confTH   = config["confTH"]
        self.device   = config["device"]
        self.nmsTH = 0.4

    def detect(self):
        # 전역변수 선언
        # src_size : 입력 이미지 크기. filename-shape -> key:value
        # cfg      : Yolo cfg file
        # weights  : Yolo weights file
        # names    : Yolo names file
        global src_size, cfg, weights, names
        src_size = dict()

        print('CONFIG, WEIGHTS, NAMES FILE LOADING')
        cfg = f'{self.models}.cfg'
        weights = f'{self.models}.weights'
        names = f'{self.models}.names'
        print('CONFIG, WEIGHTS, NAMES FILE LOAD DONE\n')

        time.sleep(3.0)

        # network load
        print('MODEL FILE LOADING')
        net = cv2.dnn.readNetFromDarknet(cfg, weights)
        print('MODEL FILE LOAD DONE\n')

        time.sleep(3.0)

        # defined 4D blob size
        with open(f'{cfg}', 'r') as f:
            cfg_array = list(csv.reader(f, delimiter=' '))
            cfg_array = np.array(cfg_array)
        (blob_width, blob_height) = (0, 0)
        for line_num in range(len(cfg_array)):
            if 'width' in cfg_array[line_num]:
                blob_width = int(cfg_array[line_num][2])
                blob_height = int(cfg_array[line_num + 1][2])

        with open(f'{names}', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers: list = []

        # device setting
        if self.device == 'gpu':
            cv2.cuda.setDevice(0)
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        else:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            output_layers = [layer_names[int(i) - 1] for i in net.getUnconnectedOutLayers()]

        files = listup_files('./Test')

        crops: dict = {}
        for file in files:
            results_save_path = f'./Results/{file}'
            os.mkdir(results_save_path)
            src = cv2.imread(f'./Test/{file}.{self.fileform}', cv2.IMREAD_ANYCOLOR)

            # 이미지에 표시할 결과 bounding box와 문자의 두께
            global thickness
            thickness = int(min(src.shape[1], src.shape[0]) / 500)

            # 분할 검사를 위한 이미지 분할
            crop_images(src, crops, file, self.cropsize, self.countx, self.county, self.fileform)

            global ovl_x, ovl_y
            ovl_x, ovl_y = calc_overlap(src.shape[1], src.shape[0], self.cropsize, self.countx, self.county)

            size = [src.shape[1], src.shape[0]]
            src_size[file] = size
            del src

        start_detect = time.time()
        print('DETECT BEGINS')
        for file in files:
            start_crop_detect = time.time()
            for ix in range(self.countx):
                for iy in range(self.county):
                    src = crops[f'{file}_{ix + 1}-{iy + 1}.{self.fileform}']

                    start = time.time()
                    blob = cv2.dnn.blobFromImage(src, 1 / 255, (blob_width, blob_height), (0, 0, 0), True, crop=False)
                    net.setInput(blob)
                    outs = net.forward(output_layers)

                    class_ids:   list = []
                    confidences: list = []
                    boxes:       list = []

                    for out in outs:
                        for detection in out:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]

                            if confidence >= self.confTH:
                                c_x = int(detection[0] * src.shape[1])
                                c_y = int(detection[1] * src.shape[0])
                                w = int(detection[2] * src.shape[1])
                                h = int(detection[3] * src.shape[0])

                                x = int(c_x - w / 2)
                                y = int(c_y - h / 2)
                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)
                    indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confTH, self.nmsTH)
                    src = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
                    pathlib.Path(f'./Results/{file}/{file}_{ix + 1}-{iy + 1}.txt').touch()

                    for idx in range(len(boxes)):
                        if idx in indices:
                            x, y, w, h = boxes[idx]
                            label = str(classes[class_ids[idx]])
                            conf = float(confidences[idx])
                            cv2.rectangle(src, (x, y), (x + w, y + h), COLOR[str(class_ids[idx])], 1)
                            cv2.putText(src, f'{label}, {conf * 100:.2f}%', (x, y - 10), STR_FONT, 0.5, COLOR[str(class_ids[idx])], 1)
                            cx = (x + (w / 2)) / src.shape[1]
                            cy = (y + (h / 2)) / src.shape[0]
                            ww = w / src.shape[1]
                            hh = h / src.shape[0]

                            with open(f'./Results/{file}/{file}_{ix + 1}-{iy + 1}.txt', 'a') as f:
                                f.write(f'{class_ids[idx]} {cx:.8f} {cy:.8f} {ww:.8f} {hh:.8f} {conf * 100:.2f}\n')
                    print(f'{file}_{ix + 1}-{iy + 1}.{self.fileform} >> CROP DETECT TIME : {time.time() - start:.2f} sec.')
                    cv2.imwrite(f'./Results/{file}/{file}_{ix + 1}-{iy + 1}.{self.fileform}', src)
            print(f'{file}.{self.fileform} >> IMAGE DETECT TIME : {time.time() - start_crop_detect:.2f} sec.')
        print(f'TOTAL RUN TIME : {time.time() - start_detect:.2f} sec.')