from flask import Flask, url_for, redirect, render_template, request
from flask_login import current_user
from flask_login import LoginManager, UserMixin,login_user, login_required,logout_user, current_user , login_user
import forms
from flask_sqlalchemy import SQLAlchemy
import os 
from hash_password import generateHashPassword,matchHashPassword
import json
import datetime

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

		if "logMeIn" in request.form:
			if signIn(usernameLogin,passwordLogin):
				return redirect(url_for('home'))
			else:
				return redirect(url_for('home'))							
	
			
	else :
		if current_user.is_authenticated:
			print ("User is_authenticated")
			user = User.query.filter_by(id=current_user.get_id()).first()
			print user.image_url
			notification_current_user = current_user.notifications.filter(Notification.to_user_id==user.id, Notification.time > user.last_message_read_time).all()
			print notification_current_user
			notification_sender_users = []
			for notification in notification_current_user:
				notification_sender_users.append(User.query.filter_by(id=notification.sender_user_id).first())
			return render_template('home.html',current_user=current_user,username=user.username,userImage = user.image_url, notification=notification_sender_users)
		else:
			print ("User Not authenticated")			
			return render_template('home.html',current_user=None)
	




@app.route("/demo",methods=['GET','POST'])
@login_required
def loginSignUp():
	print "I was called"
	return render_template("index.html",title="Posterr")


@app.route("/follow",methods=['POST'])
def follow():
	following_user = request.form.get('userToFollow');
	followOrUnfollow = request.form.get('followOrUnFollow')
	followOrUnfollow= followOrUnfollow.replace(" ", "")
	following_user = User.query.filter_by(username=following_user).first()
	if following_user:
		print ("User Exists", following_user.username)
		current_logged_user = User.query.filter_by(id=current_user.get_id()).first()
		print current_logged_user
		print followOrUnfollow
		if current_logged_user:
			if "Follow" in followOrUnfollow:
				print "I am in follow region"
				try:
					current_logged_user.follow(following_user)
					return json.dumps({
					"status":"followed"
					})
				except Exception as e :
					print str(e)  + "This is the error"
					return json.dumps({
						"status":"not_followed" 
						})
			else:
				try:
					current_logged_user.unfollow(following_user)
					return json.dumps({
					"status":"Unfollowed"
					})
				except:
					return json.dumps({
						"status":"followed"
						})		
	return url_for("users")		


@app.route("/user/<string:username>")
@login_required
def profile(username):
	return "Hello" + username



@app.route("/updateLastSeen", methods=['POST'])
@login_required
def update():
	time = request.form.get("time")
	if time=="update":
		print time 
		current_time = datetime.datetime.utcnow()
		me = User.query.filter_by(id=current_user.get_id()).first()
		me.last_message_read_time = current_time
		print me.last_message_read_time
		db.session.commit()
	return redirect(url_for('home'))
		


@app.route("/SignUpCheck",methods=['POST'])
def signupCheck():
	usernameSignUp= request.form.get('username')
	emailSignUp = request.form.get('email')
	passwordSignUp = request.form.get("PasswordSignUpHomePage")

	if usernameSignUp:
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
	elif emailSignUp:
		user = User.query.filter_by(email=emailSignUp).first() 
		if user:
			return json.dumps({
				'status':'EmailExists'
				})
		else:
			return json.dumps({
				'status':'EmailAvailable'
				})	
#association tables
	else:
		usernameSignUp = request.form.get("UsernameSignUpHomePage")
		emailSignUp = request.form.get("EmailSignUpHomePage")
		passwordSignUp = request.form.get("PasswordSignUpHomePage")
		imageUrl = request.form.get('imageUrl')
		print imageUrl + "THIS IS IMAGE URL"
		signUp(usernameSignUp,emailSignUp,passwordSignUp,imageUrl)
		return redirect(url_for('home'))

@app.route("/users")
@login_required
def users():
	current_user_id = current_user.get_id()
	users = User.query.all()
	current_loggedUser = User.query.filter_by(id=current_user_id).first()
	if current_loggedUser:
		this_user_follows_them= current_loggedUser.current_user_following()
		current_user_username = User.query.filter_by(id=current_user_id).first().username
		print this_user_follows_them
	return render_template("users.html",users=users,current_user_username=current_user_username,ifollowthem=this_user_follows_them)


association = db.Table('FollowNode',
	db.Column('followers',db.Integer,db.ForeignKey('user.id')),
	db.Column('following',db.Integer,db.ForeignKey('user.id')),
	db.Column('date',db.DateTime,default=datetime.datetime.utcnow())
	)


class Notification(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	sender_user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
	type_notification = db.Column(db.String)
	time = db.Column(db.DateTime,default=datetime.datetime.utcnow())
	to_user_id= db.Column(db.Integer,db.ForeignKey('user.id'))



class User(db.Model,UserMixin):
	id = db.Column(db.Integer,unique=True,primary_key=True)
	username = db.Column(db.String(20),unique=True)
	email = db.Column(db.String(50),unique=True)
	password_hash = db.Column(db.String)
	total_posts= db.Column(db.Integer)
	image_url = db.Column(db.String)
	last_message_read_time = db.Column(db.DateTime)
	follows = db.relationship('User',secondary=association,
	    primaryjoin=(association.c.followers == id),
        secondaryjoin=(association.c.following == id), 
        backref=db.backref('following',lazy='dynamic'),lazy='dynamic')

	notifications = db.relationship('Notification', backref='user',
		primaryjoin = (Notification.to_user_id==id), lazy='dynamic')

	#posts = db.relationship('Post',backref='author',lazy='dynamic')

	def follow(self,this_user):
		if not self.is_following(this_user):
			self.follows.append(this_user)
			new_notification= Notification(sender_user_id= self.id,to_user_id=this_user.id,type_notification="follows")	
			db.session.add(new_notification)		
			db.session.commit()

	def unfollow(self,this_user):
		if self.is_following(this_user):
			self.follows.remove(this_user)
			db.session.commit()

	def is_following(self,user):
		print self.follows.filter(association.c.following==user.id).count()> 0
		return self.follows.filter(association.c.following==user.id).count()> 0

	def current_user_following(self):
		following_users = self.follows.filter().all()
		return following_users

	def current_user_followers(self):
		followers_user = self.following.filter().all()	
		return followers_user

	def get_following(self):
		return len(self.current_user_following())
	
	def get_followers(self):
		return len(self.current_user_followers())

####################################################### DON"T DELETE THIS ################################################################
# class Post(db.Model):                                                                                                  				#
# 	id = db.Column(db.Integer,unique=True,primary_key=True)																				#
# 	date = db.Column(db.datetime,default=datetime.datetime.now())																		#
# 	caption = db.Column(db.String)																										#
# 	post_image = db.Column(db.String)																									#
# 	likes = db.Column(db.String)																										#
# 	comments = db.Column(db.String)																										#
# 	shares = db.Column(db.String)																										#
# 	posted_by = db.Column(db.Integer,db.ForeignKey('user.id'))															 				#
#########################################################################################################################################

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
	return False 
			

def signUp(username,email,password,imageUrl="None"):
	password = generateHashPassword(password)
	try:
		new_user = User(username=username,email=email,password_hash=password,image_url = imageUrl)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
		print "New User Added Successfully!"
	except:
		return redirect(url_for('home'))
	finally:
		db.session.close()	


#handling 404 error 
@app.errorhandler(404)
def error404(error):
	return render_template("404.html",error=e)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("home"))


if __name__== "__main__":
	app.run(debug=True)
