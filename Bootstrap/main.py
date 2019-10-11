# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 17:09:05 2019

@author: ankan datta

"""

from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail


local_server = True
with open('config.json', 'r') as r:
    params = json.load(r)["params"]
    
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)

mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
db = SQLAlchemy(app)


class Contacts(db.Model):
    """serial_no, name, email_id, phone_no, message, date"""
    serial_no =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email_id = db.Column(db.String(120), unique= False, nullable=False)
    phone_no = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=True, nullable = True)

@app.route("/")
def home():
    return render_template("index.html", params = params)



@app.route("/post")
def post_route():
    return render_template('post.html', params = params)

@app.route("/about")
def about():
    return render_template('about.html', params = params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    
    if(request.method == "POST"):
        """add an entry to our database"""
        name = request.form.get('Name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        """name, email_id, phone_no, message, date"""
        
        entry = Contacts(name = name, 
                         email_id = email, 
                         phone_no = phone, 
                         message = message, 
                         date = datetime.now())
        
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message + "\n" + phone
                          )
 
        
        
    
    return render_template("contact.html", params = params)

if __name__ == "__main__":
    app.run(debug = True, use_reloader=False)


