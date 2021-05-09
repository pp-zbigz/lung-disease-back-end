import os
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import  load_model
from werkzeug.utils import secure_filename
import numpy as np
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
IMAGE_SIZE = (224,224)  ## Based on the file size
UPLOAD_FOLDER = 'uploads'

def get_model():
    global model
    # model = tf.keras.models.load_model('model/covid_pneumoniae_pneumothorax_tuberculosis_normal_model')
    model = tf.keras.models.load_model('model.h5')
get_model()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def predict(file):
    img  = load_img(file, target_size=IMAGE_SIZE)
    img = img_to_array(img)/255.0
    img = np.expand_dims(img, axis=0)
    probs = model.predict(img)[0]
    output = {
        'Covid':        probs[0],
        'Normal':       probs[1],
        'Pneumoniae':   probs[2],
        'Pneumothorax': probs[3],
        'Tuberculosis': probs[4]
    }
    return output

app = Flask(__name__)  ## To upload files to folder
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
def upload_file(): 
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            output = predict(file_path)

    return jsonify({
        'Covid' : float(output['Covid']),
        'Normal' : float(output['Normal']),
        'Pneumoniae' : float(output['Pneumoniae']),
        'Pneumothorax' : float(output['Pneumothorax']),
        'Tuberculosis' : float(output['Tuberculosis'])
    })

if __name__ == "__main__":
   app.run(port = 5000)