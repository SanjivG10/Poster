from flask_bcrypt import generate_password_hash,check_password_hash

def generateHashPassword(password):
	pw_hash = generate_password_hash(password)
	return pw_hash

def matchHashPassword(pw_hash,password):
	if pw_hash and password:
		return check_password_hash(pw_hash,password)
	else:
		return False