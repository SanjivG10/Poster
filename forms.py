from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, ValidationError

from flask_bcrypt import check_password_hash as cPass

import re


def verify_username(form, field):
	connection = db.engine.raw_connection()
	cursor = connection.cursor()
	username_check = (cursor.execute('SELECT username FROM user WHERE username = "%s" '%field.data).fetchone())
	if username_check:
		username_check =  str(username_check[0].encode("utf-8"))
		print username_check
		if str(username_check)==field.data:
		    raise ValidationError('Username must be unique')
		

def verify_email(form, field):
	connection = db.engine.raw_connection()
	cursor = connection.cursor()
	email_check = (cursor.execute('SELECT email FROM user WHERE email = "%s" '%field.data).fetchone())
	# email_check = str(cursor.execute('SELECT email FROM user ').fetchall())
	if email_check:
		email_check =  str(email_check[0].encode("utf-8"))
		if str(email_check)==field.data:
		    raise ValidationError('Email is already used. Try Another ')


def verify_name(form, field):
	name = field.data.encode('utf-8') 
	return bool(re.match("^[A-Za-z]*$", name))




class RegisterForm(Form):
    username = StringField('Username',[validators.Length(min=4, max=25),verify_username])
    email = StringField('Email',[validators.Length(min=6, max=30),validators.Email(),verify_email])
    password = PasswordField('Password',[validators.Length(min=6, max=50)])
    name = StringField('Username',[validators.Length(min=4, max=25),verify_name])

class LoginForm(Form):
	username = StringField('Username',validators=[DataRequired(message="Username cannot be empty")])#,username_login])
	email = StringField('Email',validators=[DataRequired(message="Email cannot be empty")])#,unique Email])
	password = PasswordField('Password',validators=[DataRequired(message="Password is empty")])#,password_login])