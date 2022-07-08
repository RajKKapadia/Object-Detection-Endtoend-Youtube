import os

cwd = os.getcwd()

# Create folders required for the code
if not os.path.exists(f'{cwd}/downloaded_images'):
    os.mkdir(f'{cwd}/downloaded_images')

if not os.path.exists(f'{cwd}/dataset'):
    os.mkdir(f'{cwd}/dataset')
    os.mkdir(f'{cwd}/dataset/train')
    os.mkdir(f'{cwd}/dataset/valid')
    os.mkdir(f'{cwd}/dataset/test')

if not os.path.exists('model'):
    os.mkdir('model')

if not os.path.exists(f'{cwd}/result'):
    os.mkdir(f'{cwd}/result')

if not os.path.exists(f'{cwd}/upload'):
    os.mkdir(f'{cwd}/upload')

if not os.path.exists(f'{cwd}/download'):
    os.mkdir(f'{cwd}/download')

# Different paths
DOWNLOADED_IMAGES_PATH = f'{cwd}/downloaded_images'
TRAIN_DATASET_PATH = f'{cwd}/dataset/train'
VALID_DATASET_PATH = f'{cwd}/dataset/valid'
TEST_DATASET_PATH = f'{cwd}/dataset/test'
TAGS_PATH = f'{cwd}/tags.json'
UPLOAD = f'{cwd}/upload'
DOWNLOAD = f'{cwd}/download'
MODEL_PATH = f'{cwd}/model'

# Number of images to download per class
NUMBER_OF_IMAGES_PER_CLASS = 15

# Create dataset
NUMBER_OF_TEST_IMAGES = 5
TRAIN_PERCENTAGE = 0.80

# Training the model
MODEL_NAME = 'celebrity_detector.tflite'
MODEL = 'efficientdet_lite0'
EPOCHS = 20
BATCH_SIZE = 4
CLASSES = ['Bill_Gates', 'Elon_Musk', 'Sundar_Pichai', 'Steve_Jobs', 'Tim_Cook']

# Testing the model
DETECTION_THRESHOLD = 0.3

# Python Flask
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
PORT=5000
HOST='0.0.0.0'