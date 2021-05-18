import os
from re import template
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory, render_template
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import  load_model
import numpy as np
from flask_cors import CORS, cross_origin
from PIL import Image

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
IMAGE_SIZE = (224,224)  ## Based on the file size

def get_model():
    global model
    model = load_model('model.h5')
get_model()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def predict(file):
    img = Image.open(file)
    resized_image = img.resize(IMAGE_SIZE)
    img = img_to_array(resized_image)/255.0
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

app = Flask(__name__, template_folder = 'templates')  ## To upload files to folder
CORS(app)

@app.route('/predict', methods=['GET','POST','OPTIONS'])
@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
def upload_file(): 
    if request.method == 'GET':
        return 'Connected Backend API'
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            output = predict(file)

    return jsonify({
        'Covid' : float(output['Covid']),
        'Normal' : float(output['Normal']),
        'Pneumoniae' : float(output['Pneumoniae']),
        'Pneumothorax' : float(output['Pneumothorax']),
        'Tuberculosis' : float(output['Tuberculosis'])
    })

if __name__ == "__main__":
    app.run(debug=False)
    # app.run(host="0.0.0.0", port="80", debug=False)