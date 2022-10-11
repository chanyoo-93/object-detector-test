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
    files = list()
    for _file in _files:
        files.append(_file[:-4])
    files = list(set(files))
    files.sort()
    return files  # 확장자 없는 파일 이름 리스트 반환