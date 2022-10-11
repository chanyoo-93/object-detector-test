import os
import cv2

def calc_overlap(width, height, crop_size, count_x, count_y):
    ovl_x = ((crop_size * count_x) - width) / (count_x - 1)
    ovl_y = ((crop_size * count_y) - height) / (count_y - 1)
    return ovl_x, ovl_y

def save_crop_images(image, save_path, name, crop_size, countx, county, file_format):
    width, height = image.shape[1], image.shape[0]
    crop_size = crop_size
    count_x = countx
    count_y = county
    overlap_x, overlap_y = calc_overlap(width, height, crop_size, count_x, count_y)

    for x in range(count_x):
        for y in range(count_y):
            sx = int(crop_width * x) - int(overlap_x * x)
            sy = int(crop_height * y) - int(overlap_y * y)
            ex = int(crop_width * (x + 1)) - int(overlap_x * x)
            ey = int(crop_height * (y + 1)) - int(overlap_y * y)
            crop = image[sy:ey, sx:ex]
            cv2.imwrite(f'{save_path}/{name}_{x + 1}-{y + 1}.{file_format}', crop)
            print(f'IMAGE WRITE >> {save_path}/{name}_{x + 1}-{y + 1}.{file_format}')

def crop_images(image, crop_dict, name, crop_size, countx, county, file_format):
    width  : int = image.shape[1]
    height : int = image.shape[0]
    crop_size = crop_size
    count_x = countx
    count_y = county
    overlap_x, overlap_y = calc_overlap(width, height, crop_size, count_x, count_y)

    for x in range(count_x):
        for y in range(count_y):
            sx = int(crop_size * x) - int(overlap_x * x)
            sy = int(crop_size * y) - int(overlap_y * y)
            ex = int(crop_size * (x + 1)) - int(overlap_x * x)
            ey = int(crop_size * (y + 1)) - int(overlap_y * y)
            crop = image[sy:ey, sx:ex]
            crop_dict[f'{name}_{x + 1}-{y + 1}.{file_format}'] = crop

def listup_files(files_dir):
    _files = os.listdir(files_dir)  # source폴더 내 전체 파일 리스트
    files = list(set([_file[:-4] for _file in _files]))
    files.sort()
    return files  # 확장자 없는 파일 이름 리스트 반환

COLOR = {"0": (0, 255, 0),       # Green
         "1": (0, 0, 255),       # Red
         "2": (255, 0, 0),       # Blue
         "3": (0, 255, 255),     # Yellow
         "4": (255, 255, 0),     # Cyan
         "5": (255, 0, 255),     # Magenta
         "6": (0, 127, 255),     # Orange
         "7": (127, 0, 255),     # Pink
         "8": (42, 42, 165),     # Brown
         "9": (226, 43, 138),    # Blueviolet
         "10": (80, 127, 255),   # Coral
         "11": (60, 20, 220),    # Crimson
         "12": (139, 0, 0),      # Darkblue
         "13": (139, 139, 0),    # Darkcyan
         "14": (0, 100, 0),      # Darkgreen
         "15": (169, 169, 169),  # Darkgray
         "16": (0, 140, 255),    # Darkorange
         "17": (143, 188, 143),  # Darkseagreen
         "18": (139, 61, 72),    # Darkslateblue
         "19": (255, 191, 0),    # Deekskyblue
         "20": (105, 105, 105),  # Dimgray
         "21": (0, 215, 255),    # Gold
         "22": (47, 255, 173),   # Greenyellow
         "23": (180, 105, 255),  # Hotpink
         "24": (92, 92, 205),    # Indianred
         "25": (240, 255, 255),  # Ivory
         "26": (0, 255, 0),      # Lime
         "27": (219, 112, 147),  # Mediumpruple
         "28": (238, 130, 238),  # Violet
         "29": (50, 205, 154),   # Yellowgreen
         "30": (255, 255, 240),  # Azure
         "31": (220, 245, 245),  # Beige
         "32": (107, 183, 189),  # Darkkhaki
         "33": (47, 107, 85)}    # Darkolivegreen