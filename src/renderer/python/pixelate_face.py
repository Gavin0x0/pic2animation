#!/usr/bin/python

import cv2
import json
import os
import argparse

PIXEL_RATIO = 0.01

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='required', type=str)
parser.add_argument('-p', help='required', type=str)
args = parser.parse_args()
path = args.i
faces = json.loads(args.p)

im = cv2.imread(path, cv2.IMREAD_COLOR)
rows,cols = im.shape[:2]

for face in faces:
    x = face['left']
    y = face['top']
    width = face['width']
    height = face['height']
    block_im = im[y:y+height, x:x+width]
    pixel_x = int(cols*PIXEL_RATIO)
    pixel_y = int(rows*PIXEL_RATIO)
    small_im = cv2.resize(block_im, (pixel_x, pixel_y), interpolation=cv2.INTER_NEAREST)
    mosaic_im = cv2.resize(small_im, (width, height), interpolation=cv2.INTER_NEAREST)
    im[y:y+height, x:x+width] = mosaic_im
    
save_path = os.path.dirname(path) +'/pixelated-'+ os.path.basename(path)
cv2.imwrite(save_path, im)
print('pixelated')
