from flask import Flask,render_template,redirect,request,url_for, send_file
import mysql.connector
from werkzeug.utils import secure_filename
import pandas as pd
import os
import uuid
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pickle
from tensorflow.keras.applications.mobilenet import preprocess_input, MobileNet
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Reshape
from tensorflow.keras.preprocessing import image
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__)


# Configuration
UPLOAD_FOLDER = os.path.join('static', 'img')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='AIdriven'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data


@app.route('/')
def index():


    return render_template('index.html')




@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT UPPER(email) FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered! Please go to login section")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Confirm password is not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                global user_email
                user_email = email

                return redirect("/home")
            return render_template('home.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')





# Reload the MobileNet feature extractor
base_model = MobileNet(weights='imagenet', include_top=False)
feature_extractor = Model(inputs=base_model.input, outputs=GlobalAveragePooling2D()(base_model.output))

class_names =  ['agricultural', 'airplane', 'baseballdiamond', 'beach', 'buildings', 'chaparral', 'cloudy', 'denseresidential', 'desert', 'forest', 'freeway', 'golfcourse', 'harbor', 'intersection', 'mediumresidential', 'mobilehomepark', 'overpass', 'parkinglot', 'river', 'runway', 'sparseresidential', 'storagetanks', 'tenniscourt', 'unknow']

def make_prediction(image_path):
    """
    Preprocess the image and make a prediction using the MobileNet model.
    """
    # Load the image and preprocess it
    img = load_img(image_path, target_size=(224, 224))  # Resize to MobileNet input size
    img_array = img_to_array(img)  # Convert to a NumPy array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Preprocess for MobileNet

    # Extract features using the MobileNet feature extractor
    features = feature_extractor.predict(img_array)

    # Predict the class using the trained MobileNet model
    predictions = mobilenet_model.predict(features)
    predicted_class_idx = np.argmax(predictions)  # Get index of the highest probability
    predicted_class = class_names[predicted_class_idx]  # Map index to class name

    return predicted_class

# Load the MobileNet model
mobilenet_model = load_model('mobilenet_model.h5')

@app.route('/algorithm', methods=["GET", "POST"])
def algorithm():
    if request.method == "POST":
        myfile = request.files['file']  # Get the uploaded file
        fn = myfile.filename  # Extract filename
        mypath = os.path.join('static', 'img', fn)  # Save path
        myfile.save(mypath)  # Save the file to the server

        # Make prediction using MobileNet model
        predicted_class = make_prediction(mypath)

        # Return result to the template
        return render_template('algorithm.html', path=mypath, prediction=predicted_class)

    return render_template('algorithm.html')



from dotenv import load_dotenv
import os
import google.generativeai as genai
import re
load_dotenv() 

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# Function to clean Gemini output
def clean_gemini_output(text):
    return re.sub(r'(\*\*|\*)', '', text)  # remove all * and **

# Load the saved model
model = load_model('cnn_lstm_aqi_model.h5')

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        # Collect form inputs
        features = [
            float(request.form['PM2.5']),
            float(request.form['PM10']),
            float(request.form['NO']),
            float(request.form['NO2']),
            float(request.form['NOx']),
            float(request.form['NH3']),
            float(request.form['CO']),
            float(request.form['SO2']),
            float(request.form['O3']),
            float(request.form['Benzene']),
            float(request.form['Toluene']),
            float(request.form['Xylene']),
            int(request.form['City_Encoded'])
        ]

        # Scale and reshape input
        input_data = np.array([features])
        input_scaled = scaler.transform(input_data)
        input_reshaped = input_scaled.reshape((1, 1, input_scaled.shape[1]))

        # Predict AQI
        predicted_aqi = model.predict(input_reshaped)[0][0]

        # Gemini prompt
        prompt = f"""
        The predicted Air Quality Index (AQI) is {predicted_aqi:.2f}. 
        Based on this AQI value, provide:
        1. A brief summary of the health of the environment.
        2. Health recommendations for people (especially vulnerable groups).
        3. Actionable suggestions for improving air quality.
        """

        # Get Gemini response
        try:
            response = gemini_model.generate_content(prompt)
            raw_output = response.text
            cleaned_output = clean_gemini_output(raw_output)
        except Exception as e:
            cleaned_output = f"Gemini API failed: {str(e)}"

        return render_template('prediction.html', prediction=predicted_aqi, gemini_output=cleaned_output)

    return render_template('prediction.html')


@app.route('/graph')
def graph():
    return render_template('graph.html')


if __name__ == '__main__':
    app.run(debug = True)