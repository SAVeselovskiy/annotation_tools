import json
from merge_annotations import process_images
with open('0.3_ssd_full_coco_unlabeled_dev_results.json', 'r') as myfile:
    data_ssd = myfile.read()
    unlab_ssd = json.loads(data_ssd)
    ssd_count = len(unlab_ssd["annotation"])
    ids = []
    for annotation in unlab_ssd['annotation']:
        ids.append(annotation['id'])

    set_count = len(set(ids))
    _, ssd_image_count = process_images(unlab_ssd["annotation"], unlab_ssd["images"])
    print("annotations ssd = ", ssd_count)
    print("images ssd = ", ssd_image_count)

with open('instances_train2014.json', 'r') as coco_file:
    data_coco = coco_file.read()
    unlab_coco = json.loads(data_coco)
    coco_count = len(unlab_coco["annotations"])
    coco_image_count = len(unlab_coco["images"])
    print("annotations coco = ", coco_count)
    print("images coco = ", coco_image_count)
    ids = []
    for annotation in unlab_coco['annotations']:
        ids.append(annotation['id'])

    set_orig_count = len(set(ids))
    print('')

with open('new_dataset_2018_train111.json', 'r') as file:
    data = file.read()
    unlab = json.loads(data)
    result_count = len(unlab["annotations"])
    result_image_count = len(unlab["images"])
    print("annotations result = ", result_count)
    print("images result = ", result_image_count)

    ids = []
    for annotation in unlab['annotations']:
        ids.append(annotation['id'])
    id_num = len(ids)
    id_set = set(ids)
    num_set = len(id_set)
    print('')

if result_count != (coco_count + ssd_count):
    print("Failed. Wrong result annotation count count")
elif result_image_count != coco_image_count + ssd_image_count:
    print ("Failed. Wrong result image count")
elif id_num != num_set:
    print('Failed. Duplicate annotation id')
else:
    print("Success")
