import os
import re

def rename(dir):
    onlyfiles = [f for f in os.listdir(dir)]
    for file in onlyfiles:
        result = re.match(r'COCO_train2014_', file)
        if result == None:
            os.rename(dir+file,dir+'COCO_train2014_'+file)
        else:
            continue

def find(dir, name):
    onlyfiles = [f for f in os.listdir(dir)]
    result = False
    for file in onlyfiles:
        if file == name:
            result = True
    return result

def check_missing_images(dir, annotations):
    onlyfiles = sorted([f for f in os.listdir(dir)])
    image_ids = []
    # for ann in annotations


rename('/Users/sergejveselovskij/diplom/tf-faster-rcnn/data/coco/images/train2014/')
# t = find('/Users/sergejveselovskij/diplom/tf-faster-rcnn/data/coco/images/unlabeled2017/', '000000000025.jpg')
# print(t)