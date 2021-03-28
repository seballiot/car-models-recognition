from flask import render_template, request, redirect, url_for, Markup, session
from app import app, db
from app.models import *


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
    print('---')
    print('TODO')
    print('---')

    """
    return render_template(
        'dashboard.html',
        labels=labels,
        data=data,
        nb_client_homme=nb_client_homme,
        nb_client_femme=nb_client_femme,
        nb_client_na=nb_client_na,
        nb_age_a=nb_age_a,
        nb_age_b=nb_age_b,
        nb_age_c=nb_age_c,
        nb_age_d=nb_age_d,
        page='dashboard'
    )
    """

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