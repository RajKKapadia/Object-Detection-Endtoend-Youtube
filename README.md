# Object Detection using Tensorflow

## Youtube videos
* [Introduction](https://youtu.be/EeQEcoEl1VE)
* [Download images](https://youtu.be/-LJZM6gfCf4)
* [Create dataset](https://youtu.be/Dp7lYkFcooc)
* [Develop model](model final)
* [Python API](https://youtu.be/LdvlSPIgkto)

## Setup
* create a new folder and pull the repository into that folder

* navigate to the directory

* create a new vidrual environment

    > `python3 -m venv venv`

* activate the environment (this step will depend on your system), you can read more about the virtual environements [here](https://docs.python.org/3/tutorial/venv.html)
    
    > `source venv/bin/activate` (linux/mac)
    > `venv\Scripts\activate.bat` (windows)

* install the Python packages from the requirements.txt file
    
    > `pip install requirements.txt`

## Create Dataset
* add the tags in `tags.json` file

* run the `download_google_images.py` file, in this file there is a variable `NUMBER_OF_IMAGES` change it to your requirement, but not more than `500`

* run the `create_dataset.py` file, this will create a `dataset` folder and `train`, `valid`, and `test` folder inside `dataset` and randomly separate all the images into training, validation, and testing dataset

    > a variable `TRAIN_PERCENTAGE` to set your value between 0 to 1 to get the training images
    > a variable `NUMBER_OF_TEST_IMAGES` set this for number of testing images, must be a small values between 1 to 10

* use labelImg to annotate the images, make sure to use the class name as in the config variable `CLASSES`

    > `pip3 install labelImg`

## Train a model
* to train a new model on your dataset run `train_model.py` file this will create a `model` directory and save the trained model in to it

    > there are some things like `batch_size`, `epochs`, and  the `type of model` that you can change in the file before running it

    > there are different model architecture you can choose from, you can read more on it [here](https://www.tensorflow.org/lite/models/modify/model_maker/object_detection#quickstart)

    > when you train a model, make sure you have provided the correct labels to the variable in config file `CLASSES`

## Test an image
* there is a file `helper_functions.py`, there are `CLASSES` and `LABEL_MAP` variables, change them to your classes

* you can test any image by running `test.py` file

    > there is a variable `INPUT_IMAGE_PATH` in the file, please change it with the path of your image

* this will create a `result` folder and save the `input` and `output` image in to that

## Python + Flask APIs
* there is a file called `app.py`, it contains a simple Python, Flask API endpoint '`detect_object`, this will serve the model, it will take an image as a form input and give annotated image in response

    > there is a variable in `config.py` called `ALLOWED_EXTENSIONS`, we will use it make sure that the input is a valid image