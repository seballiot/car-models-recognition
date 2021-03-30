from flask import render_template, request, redirect, url_for, Markup, session
from app import app, db
from app.models import *
from app.labels_map import labels
import os
import time

import numpy as np
from PIL import Image
import matplotlib.image as mpimg

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import preprocess_input

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'cars_img')
app.config['MODEL_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'model.h5')

###
# INDEX
###
@app.route('/', methods=['GET'])
def accueil():
    return render_template('accueil.html')


###
# HOMEPAGE
###
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template(
        'dashboard.html',
        page='dashboard'
    )


@app.route('/cars/', methods=['GET'], defaults={"page": 1})
@app.route('/cars/<int:page>', methods=['GET'])
def cars(page):
    if 'username' not in session:
        return redirect(url_for('accueil'))
    page = page
    per_page = 20

    cars = Cars.query.paginate(page, per_page, error_out=False)
    nb_cars = Cars.query.count()

    return render_template(
        'cars.html',
        cars=cars,
        per_page=20,
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
        model = load_model(app.config['MODEL_PATH'], compile=False)
        model.compile(
            optimizer=Adam(lr=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        probas = model.predict(np.expand_dims(img, axis=0))
        exec_time_pred = round((time.time() - start_time_pred), 2)

        predictions = []
        for idx in probas.argsort()[0][::-1][:3]:
            predictions.append({'label': labels[idx], 'proba': round(probas[0][idx] * 100, 2)})

        #
        # 3. Recuperation en base du modele de voiture avec plus gros %
        #
        car_predicted = db.engine.execute("SELECT * FROM cars_table WHERE id = '"+predictions[0]['label']+"';")

        os.remove(path_file_preprocess)

    else:
        filename = '1617132551.066227.jpg'
        car_predicted = db.engine.execute("SELECT * FROM cars_table WHERE id = 'Audi R8 Coupe 2012';")
        exec_time_pred = 0.12
        predictions = [
            {'label': 'Audi R8 Coupe 2012', 'proba': 15.33},
            {'label': 'Acura TL Type-S 2008', 'proba': 8.43},
            {'label': 'Volvo XC90 SUV 2007', 'proba': 5.68}
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

###
# ROUTES CONNEXION / INSCRIPTION
###
@app.route('/super_admin', methods=['GET'])
def super_admin():
    return render_template('super_admin.html')


@app.route('/inscription', methods=['GET'])
def inscription():
    return render_template('inscription.html')


@app.route('/connexion', methods=['POST'])
def connexion():
    userpost = Markup.escape(request.form ['username'])
    mdppost = Markup.escape(request.form ['mdp'])

    utilisateur = db.engine.execute('SELECT username, mdp '
                                    'FROM users')
    user=utilisateur.fetchall()
    for x in user:
        if userpost == x[0] and mdppost == x[1]:
            session['username'] = x[0]
            return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('accueil'))


@app.route('/deconnexion', methods=['GET'])
def deconnexion():
    session.pop('username', None)
    return redirect(url_for('accueil'))


@app.route('/super_connex', methods=['POST'])
def super_connex():

    userpost = Markup.escape(request.form ['username'])
    mdppost = Markup.escape(request.form ['mdp'])

    utilisateur = db.engine.execute('SELECT username, mdp '
                                    'FROM super_admin')
    user=utilisateur.fetchall()
    for x in user:
        if userpost == x[0] and mdppost == x[1]:
            session['username'] = "Admin"
            return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('super_admin'))


@app.route('/create', methods=['POST'])
def create():
    userpost = request.form ['username']
    mdppost = request.form ['mdp']
    mailpost = request.form['email']

    db.engine.execute('INSERT INTO users_temp (username, mdp, mail) VALUES ("'+userpost+'", "'+mdppost+'", "'+mailpost+'")')

    return render_template('accueil.html')


@app.route('/users_temp', methods=['GET'])
def get_users_temp():
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    users_temp = db.engine.execute('SELECT * FROM users_temp')

    return render_template(
        'users_temp.html',
        users_temp=users_temp
    )


@app.route('/users', methods=['GET'])
def users():
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    users = db.engine.execute('SELECT * FROM users')

    return render_template(
        'users.html',
        users=users
    )


@app.route('/delete/<int:id>/', methods=['GET'])
def delete(id):
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    db.engine.execute('DELETE FROM users WHERE id = "'+str(Markup.escape(id))+'";')
    return redirect(url_for('users'))


@app.route('/validate/<int:id>/<string:username>/<string:mdp>/<string:mail>', methods=['GET'])
def validate(id,username,mdp,mail):
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    db.engine.execute('INSERT INTO users (username, mdp, mail) VALUES ("'+username+'", "'+mdp+'", "'+mail+'")')
    db.engine.execute('DELETE FROM users_temp WHERE id = "'+str(id)+'";')
    return redirect(url_for('get_users_temp'))


@app.route('/refused/<int:id>/', methods=['GET'])
def refused(id):
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    db.engine.execute('DELETE FROM users_temp WHERE id = "'+str(Markup.escape(id))+'";')
    return redirect(url_for('get_users_temp'))