import hashlib

def md5sum(name):
	f = open(name, 'rb')
	c=f.read()
    b = hashlib.md5(c).hexdigest()
    return b
