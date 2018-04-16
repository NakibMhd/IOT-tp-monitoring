#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, g, session, url_for, redirect
import mysql.connector
from passlib.hash import argon2

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('secret_config')

#Database functions
def connect_db () :
    g.mysql_connection = mysql.connector.connect(
        host = app.config['DATABASE_HOST'],
        user = app.config['DATABASE_USER'],
        password = app.config['DATABASE_PASSWORD'],
        database = app.config['DATABASE_NAME']
    )

    g.mysql_cursor = g.mysql_connection.cursor()
    return g.mysql_cursor

def get_db () :
    if not hasattr(g, 'db') :
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db (error) :
    if hasattr(g, 'db') :
        g.db.close()

# Mes routes
@app.route('/')
def index () :
    db = get_db()
    db.execute('SELECT url, statut FROM websites')
    websites = db.fetchall()
    return render_template('accueil.html', websites = websites)

@app.route('/connexion/', methods = ['GET', 'POST'])
def connexion () :
    email = str(request.form.get('email'))
    password = str(request.form.get('password'))

    db = get_db()
    db.execute('SELECT email, password, is_admin FROM users WHERE email = %(email)s', {'email' : email})
    users = db.fetchall()

    valid_user = False
    for user in users :
        if argon2.verify(password, user[1]) :
            valid_user = user

    if valid_user :
        session['user'] = valid_user
        return redirect(url_for('admin'))

    return render_template('connexion.html')

@app.route('/admin/')
def admin () :
    if not session.get('user') or not session.get('user')[2] :
        return redirect(url_for('connexion'))

    db = get_db()
    db.execute('SELECT url, statut FROM websites')
    websites = db.fetchall()

    return render_template('admin.html', user = session['user'], websites = websites)


@app.route('/admin/deconnexion/')
def deconnexion () :
    session.clear()
    return redirect(url_for('connexion'))

@app.route('/admin/supprimer/')
def supprimer (id) :
	db = get_db()
	db.execute('DELETE FROM websites WHERE id=' + id)
	g.mysql_connection.commit()
	return render_template('show-entries.html', entries = entries)

@app.route('/formulaire-ajouter/')
def formulaire_ajouter () :
    formulaire_ajouter = request.args.get('formulaire_ajouter')
    return render_template('ajouter.html', formulaire_ajouter = formulaire_ajouter)

@app.route('/admin/ajouter/')
def ajouter ():
	db = get_db()
	formulaire_ajouter = request.args.get('formulaire_ajouter')
	db.execute('INSERT INTO websites (url) VALUES ' + formulaire_ajouter)
	g.mysql_connection.commit()
	return render_template('ajouter.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
