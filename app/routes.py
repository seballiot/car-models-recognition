from flask import render_template, request, redirect, url_for, Markup, session
from app import app, db
from app.models import *
from app.labels_map import labels
import os
import time

import numpy as np
from PIL import Image
import matplotlib.image as mpimg

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import preprocess_input

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'cars_img')
app.config['MODEL_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'model.h5')


###
# HOMEPAGE
###
@app.route('/', methods=['GET'])
def dashboard():
    return render_template(
        'dashboard.html',
        page='dashboard'
    )


@app.route('/cars/', methods=['GET'], defaults={"page": 1})
@app.route('/cars/<int:page>', methods=['GET'])
def cars(page):
    page = page
    per_page = 50

    cars = Cars.query.paginate(page, per_page, error_out=False)
    nb_cars = Cars.query.count()

    return render_template(
        'cars.html',
        cars=cars,
        per_page=per_page,
        nb_cars=nb_cars,
        page='cars'
    )


@app.route('/car', methods=['POST', 'GET'])
def car():
    if request.method == 'POST':
        #
        # 1. Enregistrement de l'image
        #
        if 'car_img' not in request.files:
            return redirect(url_for('dashboard'))
        file = request.files['car_img']

        if file.filename == '':
            return redirect(url_for('dashboard'))

        if file and allowed_file(file.filename):

            filename = str(time.time()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            filename_preprocess = str(time.time()) + 'preprocess..' + file.filename.rsplit('.', 1)[1].lower()
            path_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            path_file_preprocess = os.path.join(app.config['UPLOAD_FOLDER'], filename_preprocess)

            file.save(path_file)
        else:
            return redirect(url_for('dashboard'))

        #
        # 2. Predictions
        #

        # Lecture de l'image
        img = Image.open(path_file)

        # Resize de l'image
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img.save(path_file_preprocess)

        # Preprocessing
        img = mpimg.imread(path_file_preprocess)
        img = preprocess_input(img)

        # Appel au model et prediction
        start_time_pred = time.time()
        model = load_model(app.config['MODEL_PATH'])
        probas = model.predict(np.expand_dims(img, axis=0))
        exec_time_pred = round((time.time() - start_time_pred), 2)

        predictions = []
        for idx in probas.argsort()[0][::-1][:5]:
            predictions.append({'label': labels[idx], 'proba': round(probas[0][idx] * 100, 2)})

        #
        # 3. Recuperation en base du modele de voiture avec plus gros %
        #
        car_predicted = db.engine.execute("SELECT * FROM cars_table WHERE id = '"+predictions[0]['label']+"';")

        os.remove(path_file_preprocess)

    else:
        filename = 'car_placeholder.jpeg'
        car_predicted = db.engine.execute("SELECT * FROM cars_table WHERE id = 'Audi R8 Coupe 2012';")
        exec_time_pred = 0.12
        predictions = [
            {'label': 'Audi R8 Coupe 2012', 'proba': 15.33},
            {'label': 'Acura TL Type-S 2008', 'proba': 8.43},
            {'label': 'Volvo XC90 SUV 2007', 'proba': 5.68},
            {'label': 'Volvo XC90 SUV 2007', 'proba': 4.2},
            {'label': 'Volvo XC90 SUV 2007', 'proba': 1.4}
        ]

    car = car_predicted.fetchone()
    return render_template(
        'car.html',
        car=car,
        filename=filename,
        predictions=predictions,
        exec_time_pred=exec_time_pred,
        page='car'
    )


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS