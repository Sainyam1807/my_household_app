from flask import Flask,render_template,request
from .models import *
from flask import current_app as app


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST":
        uname=request.form.get("username") #referencing username by name=username in base.html
        pwd=request.form.get("password")
        usr=User.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0:  #user:admin exists and role is 0
            return render_template("admin_dashboard.html")




    return render_template("base.html")

@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    return render_template("user_register.html")

@app.route('/registerprofessional')
def registerprofessional():
    return render_template("professional_register.html")