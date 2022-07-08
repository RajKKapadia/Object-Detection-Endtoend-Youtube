from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename

import tensorflow as tf
from PIL import Image

from helper_functions import run_odt_and_draw_results
import config
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
UPLOAD = config.UPLOAD
DOWNLOAD = config.DOWNLOAD
PORT = config.PORT
HOST = config.HOST

def allowed_file(filename):
    flag = '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return flag

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello World'

def get_annotated_image(image_path: str, image_name: str) -> str:

    MODEL_PATH = config.MODEL_PATH
    MODEL_NAME = config.MODEL_NAME

    DETECTION_THRESHOLD = config.DETECTION_THRESHOLD

    im = Image.open(image_path)
    im.thumbnail((512, 512), Image.ANTIALIAS)

    # Load the TFLite model
    model_path = f'{MODEL_PATH}/{MODEL_NAME}'
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Run inference and draw detection result on the local copy of the original file
    detection_result_image = run_odt_and_draw_results(
        image_path,
        interpreter,
        threshold=DETECTION_THRESHOLD
    )

    # Show the detection result
    img = Image.fromarray(detection_result_image)
    img.save(f'{DOWNLOAD}/{image_name}')



@app.route('/api/detect_object', methods=['POST'])
def detect_object():
    if 'image' not in request.files:
        return jsonify(
            {
                'status': 400,
                'message': 'Make sure file name is image in the request data.'
            }
        )
    file = request.files['image']
    if file.filename == '':
        return jsonify(
            {
                'status': 400,
                'message': 'Make sure file name is image in the request data.'
            }
        )
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = f'{UPLOAD}/{filename}'
        file.save(file_path)
        try:
            get_annotated_image(image_path=file_path, image_name=filename)
            return send_file(path_or_file=f'{DOWNLOAD}/{filename}')
        except:
            return jsonify(
                {
                    'status': 400,
                    'message': 'Some error occured.'
                }
            )
    else:
        return jsonify(
            {
                'status': 400,
                'message': 'Allowed file types are JPG, JPEG, and PNG.'
            }
        )

if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=True
    )