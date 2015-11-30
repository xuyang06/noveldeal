import os
from hashlib import sha256
from hmac import HMAC

def encrypt_password(password, salt=None):
	#"""Hash password on the fly."""
	#if salt is None:
	#	salt = os.urandom(8) # 64 bits.

	#assert 8 == len(salt)
	#assert isinstance(salt, str)

	#if isinstance(password, unicode):
	#	password = password.encode('UTF-8')

	#assert isinstance(password, str)

	#result = password
	#for i in xrange(10):
	#	result = HMAC(result, salt, sha256).digest()

	#return salt + result
	return password
	
	
def validate_password(hashed, input_password):
	return hashed == input_password
	#return hashed == encrypt_password(input_password, salt=hashed[:8])
	
if __name__ == '__main__':
	password = '1234'
	passwd = encrypt_password(password)
	print passwd
	print validate_password(passwd, password)
	
#assert validate_password(hashed, 'secret password')
