import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from flask import Flask,request,render_template 
from werkzeug.utils import secure_filename

app = Flask(__name__)
model = tf.keras.models.load_model(r"best.hdf5")

label_dict={0:'Mask',1:'No Mask'}

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f = request.files['file']
        basepath=os.path.dirname(__file__)
        file_path=os.path.join(basepath,'uploads',secure_filename(f.filename))
        f.save(file_path)
        img = load_img(file_path)
        x = img_to_array(img)
        images = np.array([x],dtype="float32")
        classes = model.predict(images)
        result = label_dict[np.argmax(classes)]
        os.remove(file_path)
        return result
    return None
    

if __name__ == "__main__":
    app.run(debug=True)
