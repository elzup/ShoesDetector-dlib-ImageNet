#! /usr/bin/python
# -*- coding: utf-8 -*-
u"""rect.txtと画像データを用いてdlibを追加学習するスクリプト.
矩形ファイルの中は
x1 y1 x2 y2 file_name
x1 y1 x2 y2 file_name2
のような空白CSVっぽくなってる前提
矩形が複数ある場合の1行は
x1 y1 x2 y2 x3 y3 x4 y4 file_name
こんな感じで作る
boxes_img1 = ([dlib.rectangle(left=329, top=78, right=437, bottom=186),
               dlib.rectangle(left=224, top=95, right=314, bottom=185),
               dlib.rectangle(left=125, top=65, right=214, bottom=155)])
boxes_img2 = ([dlib.rectangle(left=154, top=46, right=228, bottom=121),
               dlib.rectangle(left=266, top=280, right=328, bottom=342)])
boxes = [boxes_img1, boxes_img2]
images = [io.imread(faces_folder + '/xxxxxx.jpg'),
          io.imread(faces_folder + '/yyyyyy.jpg')]
"""

import dlib
import os
from skimage import io
import xml.etree.ElementTree as ET

'''--------------'''
image_folder = './images/'
rect_folder = './Annotation/n13926786/'
rect_file = './true_rect.txt'
'''--------------'''


def get_rect(rect_file):
    u"""矩形ファイルを読み込みリスト化."""
    rect_list = []
    for line in open(rect_file, 'r'):
        rect_list.append(line)
    return rect_list


def make_train_data(ids):
    u"""矩形リストから学習用データを生成する."""
    boxes = []
    images = []

    for id in ids:
        rect_path = rect_folder + id + '.xml'
        image_path = image_folder + id + '.jpg'
        if not os.path.isfile(image_path) or not os.path.isfile(rect_path):
            continue
        root = ET.parse(rect_path).getroot()

        # 矩形をdlib.rectangle形式でリスト化
        img_rect = []
        for bndbox in root.iter('bndbox'):
            left, top, right, bottom = map(lambda x: int(x.text), bndbox)
            img_rect.append(dlib.rectangle(left, top, right, bottom))

        # boxesに矩形リストをtupleにして追加
        # imagesにファイル情報を追加
        boxes.append(tuple(img_rect))
        images.append(io.imread(image_path))
    return boxes, images


def training(boxes, images):
    u"""学習するマン."""
    # simple_object_detectorの訓練用オプションを取ってくる
    options = dlib.simple_object_detector_training_options()
    # 左右対照に学習データを増やすならtrueで訓練(メモリを使う)
    options.add_left_right_image_flips = True
    # SVMを使ってるのでC値を設定する必要がある
    options.C = 5
    # スレッド数指定
    options.num_threads = 16
    # 学習途中の出力をするかどうか
    options.be_verbose = True
    # 停止許容範囲
    options.epsilon = 0.001
    # サンプルを増やす最大数(大きすぎるとメモリを使う)
    options.upsample_limit = 8
    # 矩形検出の最小窓サイズ(80*80=6400となる)
    options.detection_window_size = 6400

    # 学習してsvmファイルを保存
    print('train...')
    detector = dlib.train_simple_object_detector(images, boxes, options)
    detector.save('./detector.svm')

if __name__ == '__main__':
    ids = list(map(lambda s: os.path.splitext(s)[0], os.listdir(rect_folder)))

    # # 矩形情報を取ってくる
    # rect_list = get_rect(rect_file)
    # # 学習用データを作る
    boxes, images = make_train_data(ids)
    print(boxes)
    # # 学習する
    # training(boxes, images)
