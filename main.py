from flask import Flask, url_for, redirect, render_template, request
from flask_login import current_user
from flask_login import LoginManager, UserMixin,login_user, login_required,logout_user, current_user
import forms
from flask_sqlalchemy import SQLAlchemy
import os 
#initializing the app 
app = Flask (__name__)

app.secret_key="kjasdh,mvnkasjdioarulzxcmzxcas;ldka;sd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd()+'users.db'
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route("/",methods=['GET','POST'])
def home():
	if request.method =="POST":
		return render_template('login.html',title="Login ")
	else :
		loginForm = forms.LoginForm(request.form);
		registrationForm= forms.RegisterForm(request.form)
		return render_template('home.html',title="Login",form=loginForm,form1=registrationForm)




@app.route("/demo",methods=['GET','POST'])
def loginSignUp():
	return render_template("index.html",title="Posterr")

@app.route("/login",methods=['GET','POST'])
def login():
	x = current_user.is_authenticated
	form = forms.LoginForm(request.form)
	if not x:
		if request.method == 'POST' and form.validate():
			user = User.query.filter_by(username=form.username.data).first()
			login_user(user)
			return redirect("profile/"+str(user.username))
		else:
			return render_template("login.html",form=form)
	else:
		user = User.query.filter_by(id=current_user.get_id()).first()
		username = user.username
		return redirect("profile/"+str(username))


@app.route("/resetPassword",methods=['GET','POST'])
def resetPass():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = forms.PasswordResetForm(request.form)
	if request.method == "POST" and form.validate:
		print "RESET PASSWORD "
		given_email = form.email.data
		user = User.query.filter_by(email = given_email).first()		
		if user:
			send_email(" Reset Password ", "anyone@gmail.com",given_email,user)
			flash(" Confirmation Link has been sent.")
	return render_template("forgot_pass.html",form=form)



#handling 404 error 
@app.errorhandler(404)
def error404(e):
	return render_template("404.html",error=e)





if __name__== "__main__":
	app.run(debug=True)