#! /usr/bin/python
# -*- coding: utf-8 -*-

import dlib
import os
from skimage import io
from skimage.transform import rescale
import xml.etree.ElementTree as ET

'''--------------'''
image_folder = './images/'
rect_folder = './Annotation/n13926786/'
img_scale = 1
'''--------------'''


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
        # print(image_path)
        for bndbox in root.iter('bndbox'):
            left, top, right, bottom = map(lambda x: int(int(x.text) * img_scale), bndbox)
            # print(left, top, right, bottom)
            # print(right - left, bottom - top)
            if not (0.9 < (right - left) / (bottom - top) < 1.1):
                # print('skip', right - left, bottom - top)
                continue
            print(right - left, bottom - top)
            w = right - left
            if w >= 200:
                continue
            img_rect.append(dlib.rectangle(left, top, left + w, top + w))
            print('->', left, top, left + w, top + w)
            # img_rect.append(dlib.rectangle(left, top, right, bottom))

        # boxesに矩形リストをtupleにして追加
        # imagesにファイル情報を追加
        boxes.append(tuple(img_rect))
        images.append(rescale(io.imread(image_path), img_scale))
    return boxes, images


def training(boxes, images):
    u"""学習"""
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
    # options.epsilon = 0.001
    options.epsilon = 0.01
    # サンプルを増やす最大数(大きすぎるとメモリを使う)
    options.upsample_limit = 1
    # 矩形検出の最小窓サイズ(80*80=6400となる)
    options.detection_window_size = 6400
    # options.detection_window_size = 100

    # 学習してsvmファイルを保存
    print('train...')
    detector = dlib.train_simple_object_detector(images, boxes, options)
    detector.save('./detector.svm')

if __name__ == '__main__':
    ids = list(map(lambda s: os.path.splitext(s)[0], os.listdir(rect_folder)))

    # # 学習用データを作る
    boxes, images = make_train_data(ids)
    # # 学習する
    training(boxes, images)
