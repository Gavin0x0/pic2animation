#!/usr/bin/python

import cv2
import dlib
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='required', type=str)
args = parser.parse_args()
path = args.i
detector = dlib.get_frontal_face_detector()
im = cv2.imread(path, cv2.IMREAD_COLOR)

if im is None:
    exit()

rects = detector(im, 1)
if len(rects) == 0:
    exit()

faces = []
for rect in rects:
    faces.append({
        'top': int(rect.top()),
        'left': int(rect.left()),
        'width': int(rect.width()),
        'height': int(rect.height())
    })
print(json.dumps(faces))
