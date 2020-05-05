#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify
from flaskext.mysql import MySQL
import mcfuc
import forms


app = Flask(__name__)

app.config['SECRET_KEY'] = '4bf8ccad8c649d8cd98a0215663ecd97'
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = "Users"
app.config['MYSQL_DATABASE_HOST'] = "localhost"

mysql = MySQL()
mysql.init_app(app)


@app.route("/login", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if form.validate_on_submit():
        Fusername = form.username.data
        Fpassword = form.password.data
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT nickname from f_Users where nickname = '{}'".format(Fusername))
            mysqlUsername = cursor.fetchone()
            if mysqlUsername == None:
                flash("Nie znaleziono uzytkownika o takim nicku: {}".format(Fusername), category='danger')
                return redirect(url_for('login'))
            cursor.execute("SELECT * from f_Users where passwd = MD5(CONCAT(salt, '{}'))".format(Fpassword))
            mysqPassword = cursor.fetchone()
            if mysqPassword == None:
                flash("Bledne haslo dla uzytkownika {}".format(Fusername), category='danger')
                return redirect(url_for('login'))
            connection.close()
            session['username'] = mysqlUsername[0]
            flash("Pomyslnie zalogowano jako {}".format(mysqlUsername[0]), category='success')
            return redirect(url_for('admin'))
        except Exception as e:
            flash('Wystapil nieoczekiwany blad! -> {}'.format(e), category='warning')
            return redirect(url_for('login'))
    return render_template('login.html', title='Logowanie', form=form)

@app.route("/admin", methods=['GET','POST'])
def admin():
    form1 = forms.Run()
    form2 = forms.Close()
    form3 = forms.Console()
    server_name = ''
    if 'username' in session:
        mcmgr = mcfuc.mcManage(server_name , 25575, '')
        if form1.submit1.data and form1.validate_on_submit():
            print('Starting the server')
            print(mcmgr.runServer())
            flash("Uruchamianie serwera", category="warning")
            return redirect(url_for("admin"))
        if form2.submit2.data and form2.validate_on_submit():
            print('Closing the server')
            print(mcmgr.closeServer())
            flash("Serwer zostal wlaczony", category="success")
            return redirect(url_for("admin"))
        if form3.submit3.data and form3.validate_on_submit():
            return redirect(url_for("console", server_name=server_name))
        return render_template('admin.html', title='Panel administracyjny', form1=form1, form2=form2, form3=form3)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Pomyslnie wylogowano", category='info')
    return redirect(url_for('login'))

@app.route('/refresh', methods=['POST'])
def refresh():
    if request.method == 'POST':
            mcmgr = mcfuc.mcManage('', 25575, '')
            mcmgr.stats()

            if mcmgr.status == True:
                statusInfo = "Online"
                color = 'badge-success'
            else:
                statusInfo = "Offline"
                color = "badge-secondary"
            return jsonify(online = mcmgr.online, max =mcmgr.max, status=statusInfo, color=color)

@app.route('/refreshc', methods=['POST'])
def refreshc():
    if request.method == 'POST':
       try:
            mcmgr = mcfuc.mcManage('', 25575, '')
            lastLog = mcmgr.downloadLogs()
            lastlog = str(lastLog)
            replace = lastLog.replace("<"," ").replace(">", ":").replace("[m", " ").replace(""," ")
            print(lastLog)
            return jsonify(log=replace)
       except Exception:
           pass

@app.route('/console', methods=['GET','POST'])
def console():
    server_name = request.args['server_name']
    return render_template('console.html', server_name=server_name, title="Konsola")

@app.route('/consoleForm', methods=['GET','POST'])
def consoleForm():
    if request.method == "POST":
        command = request.form['data']
        mcmgr = mcfuc.mcManage('', 25575, '')
        mcmgr.command(command)
    return jsonify(response='Success')


if __name__ == '__main__':
    app.run(debug=True)