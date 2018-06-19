from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os 
#initializing the app 
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd()+'users.db'
db = SQLAlchemy(app)

@app.route("/",methods=['GET','POST'])
def home():
	return render_template("index.html",title="Posterr")



if __name__== "__main__":
	app.run(debug=True)