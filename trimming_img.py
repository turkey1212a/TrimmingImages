import cv2
import pandas as pd
import sys
import shutil
import img2pdf

import config
import utils

def draw_rectangle_for_test(img_src, left_x, upper_y, right_x, lower_y):
    height, width = img_src.shape[:2]
    print(f'image size : width {width} * height {height}')
    print(f'  upper left  : ({left_x}, {upper_y})')
    print(f'  lower right : ({right_x}, {lower_y})')
    print('')

    if left_x < 0 or upper_y < 0 or right_x >= width or lower_y >= height:
        print('[error]')
        print(f'needed :')
        print(f'  left_x({left_x}) >= 0')
        print(f'  upper_y({upper_y}) >= 0')
        print(f'  right_x({right_x}) < {width}')
        print(f'  lower_y({lower_y}) < {height}')
        return None

    img_dst = cv2.rectangle(img_src.copy(), (left_x, upper_y), (right_x , lower_y), (255, 0, 255))

    text_pos = (left_x + 10, upper_y + 30)
    cv2.putText(img_dst, f'upper left  : ({left_x}, {upper_y})', text_pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 0, 255))
    text_pos = (left_x + 10, upper_y + 60)
    cv2.putText(img_dst, f'lower right : ({right_x}, {lower_y})', text_pos, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(0, 0, 255))

    return img_dst


def cut_out_rectangle(img_src, left_x, upper_y, right_x, lower_y):
    return img_src[upper_y : lower_y + 1, left_x : right_x + 1]


# 実行コマンド
# python3 trimmng_img.py 
# (コマンドライン引数なし)
#


if __name__ == '__main__':

    # files = pd.read_csv(config.FILES_LIST, header=None, names=['No',  'File name'])
    files = pd.read_csv(config.FILES_LIST, header=None, encoding = "shift-jis")
    if len(files.columns) == 2:
        # files.columns = ['No',  'File name']
        input_fnames = files.iloc[:, 1]
        suffixes = files.iloc[:, 0]
    else:
        # files.columns = ['File name']
        input_fnames = files.iloc[:, 0]
        suffixes = range(len(input_fnames))

    if config.MODE == 'test':
        output_dir = f'out_{utils.timestamp_now()}'
        files_num = config.TEST_NUM
    else:
        output_dir = config.OUTPUT_DIR
        files_num = len(input_fnames)

    utils.madir_if_absent(output_dir)

    # configファイルを出力フォルダにコピーしておく
    shutil.copy('./config.py', output_dir)

    output_img_list = []
    for file_no in range(files_num):
        print(f'[#{file_no}]')
        fname_src = f'{config.INPUT_DIR}/{input_fnames[file_no]}'
        fname_dst = f'{output_dir}/{config.FNAME_BASE}_{suffixes[file_no]:03}.png'
        print(f'input  : [{fname_src}]')
        print(f'output : [{fname_dst}]')

        img_src = cv2.imread(fname_src)
        print(f'height : {img_src.shape[0]}')
        print(f'width  : {img_src.shape[1]}')

        if config.MODE == 'test':
            img_test = draw_rectangle_for_test(
                img_src,
                config.LEFT_X,
                config.UPPER_Y,
                config.RIGHT_X,
                config.LOWER_Y
            )
            if img_test is None:
                break
            fname_test = f'{output_dir}/{config.FNAME_BASE}__{suffixes[file_no]:03}.png'
            cv2.imwrite(fname_test, img_test)
        img_dst = cut_out_rectangle(
            img_src,
            config.LEFT_X,
            config.UPPER_Y,
            config.RIGHT_X,
            config.LOWER_Y
        )
        cv2.imwrite(fname_dst, img_dst)
        output_img_list.append(fname_dst)

    if config.CONVERT_TO_PDF and config.MODE != 'test':
        fname_pdf = f'{config.PARENT_DIR}/{config.TITLE}/{config.FNAME_BASE}.pdf'
        print('')
        print (f'PDFファイル作成：{fname_pdf}')
        with open(fname_pdf,'wb') as f:
            f.write(img2pdf.convert(output_img_list))
