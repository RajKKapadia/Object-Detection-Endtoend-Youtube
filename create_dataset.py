import os
from random import shuffle
import random
import shutil

import config

random.seed(a=2022)

DOWNLOADED_IMAGES_PATH = config.DOWNLOADED_IMAGES_PATH

image_names = os.listdir(DOWNLOADED_IMAGES_PATH)
shuffle(image_names)

TRAIN_PERCENTAGE = config.TRAIN_PERCENTAGE
NUMBER_OF_TEST_IMAGES = config.NUMBER_OF_TEST_IMAGES

train_image_names = image_names[:int(len(image_names) * TRAIN_PERCENTAGE)]
valid_image_names = image_names[int(len(image_names) * TRAIN_PERCENTAGE):len(image_names) - NUMBER_OF_TEST_IMAGES]
test_image_names = image_names[(len(train_image_names) + len(valid_image_names)):]

for train_image_name in train_image_names:
    shutil.move(
        src=f'{DOWNLOADED_IMAGES_PATH}/{train_image_name}',
        dst=config.TRAIN_DATASET_PATH
    )

for valid_image_name in valid_image_names:
    shutil.move(
        src=f'{DOWNLOADED_IMAGES_PATH}/{valid_image_name}',
        dst=config.VALID_DATASET_PATH
    )

for test_image_name in test_image_names:
    shutil.move(
        src=f'{DOWNLOADED_IMAGES_PATH}/{test_image_name}',
        dst=config.TEST_DATASET_PATH
    )

print('Dataset created successfully.')