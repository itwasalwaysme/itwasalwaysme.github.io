from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import login_manager, UserMixin, login_required, login_user, LoginManager
from models import Usuarios
from db import db
import hashlib
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"
db.init_app(app)
app.secret_key = 'macrudo'

def encrypt(txt):
    encrypt = hashlib.sha256(txt.encode('utf-8'))
    return encrypt.hexdigest()

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        verify = db.session.query(Usuarios).filter_by(username=user, password=encrypt(password)).first()
        if not verify:
            flash("Incorrect user or password")
            return redirect(url_for('login'))
        else:
            time.sleep(1)
            return render_template("success.html")

@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if request.method == "GET":
        return render_template("registrar.html")
    elif request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        verify = db.session.query(Usuarios).filter_by(username=user).first()
        if verify:
            flash("user not available")
            return redirect(url_for('registrar'))
        else:
            newUser = Usuarios(username=user, password=encrypt(password))
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('login'))
            
    return render_template("registrar.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)