import json
from operator import itemgetter
# import pycocotools._mask
import pycocotools._mask as _mask
import numpy as np
from pycocotools.mask import area
from pycocotools.mask import toBbox
from pycocotools.coco import COCO
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
import re

def read_one_image(image_file):
    try:
        img = cv2.imread(image_file)
        b, g, r = cv2.split(img)
        img_rgb = cv2.merge((r, g, b))
    except:
        print('Error reading image file: ', image_file)
        img_rgb = None
    return img_rgb

def binary_search(a_list, item):

    first = 0
    last = len(a_list) - 1
    while first <= last:
        i = (first + last) / 2
        if a_list[i]['image_id'] == item:
            return True
        elif a_list[i]['image_id'] > item:
                    last = i - 1
        elif a_list[i]['image_id'] < item:
                    first = i + 1
    return False

def process_images(orig_annotations, orig_images):
    indexes = []
    annotations = sorted(orig_annotations, key=itemgetter('image_id'))
    print ("len before = ", len(annotations))
    a = annotations[0]['image_id']
    uniq_annotations = [annotations[0]]
    for i in xrange(0, len(annotations)):
        if annotations[i]['image_id'] != a:
            a = annotations[i]['image_id']
            uniq_annotations.append(annotations[i])
    print ("len after = ", len(uniq_annotations))

    for j in xrange(0, len(orig_images)):
        if binary_search(uniq_annotations, orig_images[j]['id']):
            indexes.append(j)
    new_images = []
    for i in indexes:
        new_images.append(orig_images[i])
    print("len indexes = ", len(indexes))
    print ("len before = ", len(annotations))
    print ("len after = ", len(uniq_annotations))
    print ("images array size = ", len(orig_images))
    return new_images, len(new_images)

def start():

    with open('0.3_ssd_full_coco_unlabeled_dev_results.json', 'r') as myfile:
        data = myfile.read()
        unlab = json.loads(data)
        # annotation = unlab['annotation'][0]
        # x = annotation['bbox'][0]
        # y = annotation['bbox'][1]
        # w = annotation['bbox'][2]
        # h = annotation['bbox'][3]
        #
        # image_name = ''
        # for image in unlab['images']:
        #     if image['id'] == annotation['image_id']:
        #         image_name = image['file_name']
        #         break
        # directory_path = '/Users/sergejveselovskij/diplom/tf-faster-rcnn/data/coco/images/unlabeled2017/'

        # im = np.array(Image.open(directory_path+image_name), dtype=np.uint8)
        #
        # # Create figure and axes
        # fig, ax = plt.subplots(1)
        #
        # # Display the image
        # ax.imshow(im)
        #
        # # Create a Rectangle patch
        # rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        #
        # # Add the patch to the Axes
        # ax.add_patch(rect)

        # plt.show()

        for i in unlab['annotation']:
            x = i['bbox'][0]
            y = i['bbox'][1]
            w = i['bbox'][2]
            h = i['bbox'][3]
            t = _mask.frBbox(np.array([[x, y, w, h]]), w, h)
            # # t = _mask.frBbox(np.array([[100.0, 100.0, 480.0, 640.0]]), 640.0, 480.0)
            tt = toBbox(t)
            # # ttt = _mask.encode(np.array(t))
            ttt = area(t)
            i["area"] = int(ttt[0])
            print(i['area'])
        new_images, new_images_count = process_images(unlab["annotation"], unlab["images"])
        directory_path = '/Users/sergejveselovskij/diplom/tf-faster-rcnn/data/coco/images/train_2014/'
        

    with open('instances_train2014.json', 'r') as origfile:
        data1 = origfile.read()
        orig = json.loads(data1)
        # test = orig["annotations"].copy()
        orig_annotations = sorted(orig['annotations'], key=itemgetter('id'))
        ann_count = len(orig_annotations) + len(unlab['annotation'])
        last_id = orig_annotations[len(orig_annotations) - 1]['id'] + 1
        i = 0
        ids = []
        for ann in orig_annotations:
            ids.append(ann['id'])
        for new_annotation in unlab['annotation']:
            new_annotation['id'] = new_annotation['id'] + last_id
            ids.append(new_annotation['id'])

        uniq_count = len(set(ids))

        new_orig_images, new_orig_images_count = process_images(orig["annotation"], orig["images"])
        orig["annotations"].extend(unlab["annotation"])
        orig["images"] = new_orig_images.extend(new_images)

        # res_ids = []
        # for new_ann in orig['images']:
        #     result = re.match(r'COCO_train2014_', new_ann['file_name'])
        #     if result == None:
        #         res_ids.append('COCO_train2014_' + new_ann['file_name'])
        #     else:
        #         res_ids.append(new_ann['file_name'])
        # res_count = len(res_ids)
        # res_uniq = len(set(res_ids))

        with open('new_dataset_2018_train111.json', 'w') as file:
            js = json.dumps(orig, sort_keys=True)
            file.write(js)
            print('Saved json to disk!')

# start()