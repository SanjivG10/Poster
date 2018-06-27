from flask import Flask, url_for, redirect, render_template, request
from flask_login import current_user
from flask_login import LoginManager, UserMixin,login_user, login_required,logout_user, current_user , login_user
import forms
from flask_sqlalchemy import SQLAlchemy
import os 
from hash_password import generateHashPassword,matchHashPassword
import json

#initializing the app 
app = Flask (__name__)

app.secret_key="kjasdh,mvnkasjdioarulzxcmzxcas;ldka;sd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.getcwd()+'/users.db'
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/",methods=['GET','POST'])
def home():
	if request.method == "POST":
		print "Post ma aayo"
		usernameLogin = request.form.get("UsernameLoginHomePage")
		passwordLogin =  request.form.get("PasswordLoginHomePage")

		usernameSignUp= request.form.get("UsernameSignUpHomePage")
		emailSignUp = request.form.get("EmailSignUpHomePage")
		passwordSignUp = request.form.get("PasswordSignUpHomePage")

		if "logMeIn" in request.form:
			print usernameLogin, passwordLogin
			if signIn(usernameLogin,passwordLogin):
				return redirect(url_for('home'))
			else:
				return redirect(url_for('home'))							
		else:
			signUp(usernameSignUp,emailSignUp,passwordSignUp)
			return redirect(url_for('home'))
	else :
		if current_user.is_authenticated:
			#dosomething
			print ("User is_authenticated")
			return render_template('home.html',current_user=current_user)
		else:
			print ("User Not authenticated")			
			return render_template('home.html',current_user=None)
	




@app.route("/demo",methods=['GET','POST'])
@login_required
def loginSignUp():
	print "I was called"
	return render_template("index.html",title="Posterr")


@app.route("/SignUpCheck",methods=['POST'])
def signupCheck():
	usernameSignUp= request.form.get('username')
	user = User.query.filter_by(username=usernameSignUp).first() 
	if user:
		print user.username
		return json.dumps({
			'status':'UsernameExists'
			})
	else:
		return json.dumps({
			'status':'UsernameAvailable'
			})	

#association tables


class User(db.Model,UserMixin):
	id = db.Column(db.Integer,unique=True,primary_key=True)
	username = db.Column(db.String(20),unique=True)
	email = db.Column(db.String(50),unique=True)
	password_hash = db.Column(db.String)
	# following = db.relationship(
	# 		'User', 
	# 		#association table is specified as secondary
	# 		secondary='followers_table',
	# 		primaryjoin=lambda: User.id == followers_table.c.followers_id, #followers_following+table column name cursor named with id 
	# 		secondaryjoin=lambda: User.id == followers_table.c.following_id,
	# 		#field that is geenratd in other Model, automatically, here  followers is generated automatically in User beneath this code
	# 		backref=db.backref('followers', lazy='dynamic'), 
	# 		lazy = 'dynamic'
	# 		)
	# def follow(self,user):
	# 	if not self.is_following(user):
	# 		self.following.append(user)

	# def unfollow(self,user):
	# 	if self.is_following(user):
	# 		self.remote(user)

	# def is_following(self,user):
	# 	return self.following_filter(
	# 	followers_tale.c.following_id ==user.id).count >0

# followers_table = db.Table("followers_following_node",
# 		db.Column('followers_id',db.Integer,db.ForeignKey(User.id)),		
# 		db.Column('following_id',db.Integer,db.ForeignKey(User.id))
# 	)


def signIn(username,password):
	user = User.query.filter_by(username=username).first()
	print user 
	if user:
		actual_username = user.username
		actual_password = user.password_hash
		if username==actual_username and matchHashPassword(actual_password,password):
			db.session.add(user)
			login_user(user)
			return True 
			

def signUp(username,email,password):
	password = generateHashPassword(password)
	try:
		new_user = User(username=username,email=email,password_hash=password)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
		print "New User Added Successfully!"
	except:
		return redirect(url_for(error404("Error Occured")))
	finally:
		db.session.close()	






#handling 404 error 
@app.errorhandler(404)
def error404(e):
	return render_template("404.html",error=e)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("home"))


if __name__== "__main__":
	app.run(debug=True)