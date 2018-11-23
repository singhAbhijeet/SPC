import os
import pickle
import sys
import requests
import getpass
import wget
import json
import urllib.request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Cipher import Salsa20
from base64 import b64decode






file = open("login.p", 'rb')
a = pickle.load(file)

client = requests.session()
try:
	url = "http://127.0.0.1:8000/api/v1/rest-auth/login/"
	login_data = {
		'username': a['user'],
		'password': a['password'],
	}
	client.get(url)
	r = client.post(url, data=login_data)
except:
	print("you are not logged in")
	exit()

userkeyo = a['userkey']
scho = a['scheme']
file.close()

print('which encryption Scheme do you wish to use')
print('AES \nCHACHA20\nSALSA20')
sch = input('1/2/3\n')


if sch=='1':
	key = get_random_bytes(16)
elif sch=='2':
	key = get_random_bytes(32)
elif sch=='3':
	key = get_random_bytes(32)
else:
	print('we have only three encryption schemes')
	exit()

if scho==sch:
	print('that is same as before')
	exit()

userkey = key
dic = {'user': a['user'], 'password': a['password'], 'key': a["key"], 'userkey' : key, 'scheme':sch }
file = open("login.p", 'wb+')
pickle.dump(dic, file)
file.close()


directory = str(input("Give the location of directory we can use temporarily: "))
os.chdir(directory)



def downloader(pk):
	url = "http://127.0.0.1:8000/api/v1/api-download/" + str(pk) + "/"
	r = client.get(url)
	#print(r)
	a = r.json()
	for f in a["files"]:
		url1 = "http://127.0.0.1:8000/files/download/?name=" + f[0]
		filename = wget.download(url1, out="./")
		print(filename)
		file_in = open(filename, "rb")
		print(str(f[3]))
		url5="http://127.0.0.1:8000/file/delete/"+str(f[3])+"/"
		client.get(url5)


		if scho=='1':
			nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
			cipher = AES.new(userkeyo, AES.MODE_EAX, nonce)
			plaintext = cipher.decrypt_and_verify(ciphertext, tag)

		if scho=='2':
			json_input = file_in.read()
			b64 = json.loads(json_input)
			nonce = b64decode(b64['nonce'])
			ciphertext = b64decode(b64['ciphertext'])
			cipher = ChaCha20.new(key=userkeyo, nonce=nonce)
			plaintext = cipher.decrypt(ciphertext)

		if scho=='3':
			msg = file_in.read()
			msg_nonce = msg[:8]
			ciphertext = msg[8:]
			cipher = Salsa20.new(key=userkeyo, nonce=msg_nonce)
			plaintext = cipher.decrypt(ciphertext)

		os.remove(filename)

		file_out = open(filename, 'wb')
		file_out.write(plaintext)
		



	for f in a["folders"]:
		os.mkdir(f[0])
		os.chdir(f[0])
		downloader(f[1])
		os.chdir("..")
		url4="http://127.0.0.1:8000/file/delete/fol/"+str(f[1])+"/"
		client.get(url4)        
downloader(1)




def add_in(pk, userkey, sch):
	myfiles = os.listdir()
	print(myfiles)
	#exit()
	for file in myfiles:
		if os.path.isdir(file):
			url = "http://127.0.0.1:8000/api/v1/api-add-folder/" + str(pk) + "/"
			apps = {
				'folder_name': file,
			}
			r = client.post(url, data=apps)
			a = r.json()
			os.chdir(file)
			#print(a["pkey"])
			add_in(a["pkey"], userkey, sch)
			os.chdir("..")
		else:
			url="http://127.0.0.1:8000/api/v1/api-add-file/"+str(pk)+"/"
			f=open(file,'rb')
			data = f.read()

			if sch == '1':
				file_out = open(file, 'wb+')
				cipher = AES.new(userkey, AES.MODE_EAX)
				ciphertext, tag = cipher.encrypt_and_digest(data)
				[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
		

			if sch == '2':
				file_out = open(file, 'w+')
				cipher = ChaCha20.new(key=userkey)
				ciphertext = cipher.encrypt(data)
				nonce = b64encode(cipher.nonce).decode('utf-8')
				ct = b64encode(ciphertext).decode('utf-8')
				result = json.dumps({'nonce':nonce, 'ciphertext':ct})
				file_out.write(result)

			if sch == '3':
				file_out = open(file, 'wb+')
				secret = get_random_bytes(32)
				cipher = Salsa20.new(key=userkey)
				msg = cipher.nonce + cipher.encrypt(data)
				file_out.write(msg)

			file_out.close()
			#os.remove(outfile)
			f = open(file, "rb+")
			#os.remove(file)
			print(file)

			hello={
				'file_name' : file
					  }
			hey={
			  'org_file' : f
				 }
			r=client.post(url,data=hello,files=hey)



# def outer(Location):
#   if(os.path.isfile(Location)):
#       url="http://127.0.0.1:8000/api/v1/api-add-file/1/"
#       f=open(Location,'rb')
#       data = f.read()
#       outfile = os.path.basename(Location)
	

#       if sch == '1':
#           file_out = open(outfile, "wb")
#           cipher = AES.new(userkey, AES.MODE_EAX)
#           ciphertext, tag = cipher.encrypt_and_digest(data)
#           [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
			

#       if sch == '2':
#           file_out = open(outfile, "w")
#           cipher = ChaCha20.new(key=userkey)
#           ciphertext = cipher.encrypt(data)
#           nonce = b64encode(cipher.nonce).decode('utf-8')
#           ct = b64encode(ciphertext).decode('utf-8')
#           result = json.dumps({'nonce':nonce, 'ciphertext':ct})
#           file_out.write(result)

#       if sch == '3':
#           plaintext = file.read()
#           secret = get_random_bytes(32)
#           cipher = Salsa20.new(key=secret)
#           msg = cipher.nonce + cipher.encrypt(plaintext)
#           file_out.write(result)


#       file_out.close()


#       f = open(outfile, "rb")
#       os.remove(outfile)

#       hello={
#           'file_name' : os.path.basename(Location) 
#       }
#       hey={
#       'org_file' : f
#       }
#       r=client.post(url,data=hello,files=hey)


#   else:
#       if Location[-1]=='/':
#           Location=Location[0:len(Location)-1]
#       print(Location)
#       url = "http://127.0.0.1:8000/api/v1/api-add-folder/1/"
#       apps = {
#                   'folder_name': os.path.basename(Location)
#               }
#       r = client.post(url, data=apps)
#       a = r.json()
#               #print(a["pkey"])
		
#       os.chdir(Location)
#       add_in(a["pkey"], userkey, sch)
	

myfiles = os.listdir()
for file in myfiles:
	print(file)
	if(os.path.isfile(file)):
		url="http://127.0.0.1:8000/api/v1/api-add-file/1/"
		f=open(Location,'rb')
		data = f.read()
		outfile = os.path.basename(file)
		

		if sch == '1':
			file_out = open(outfile, "wb")
			cipher = AES.new(userkey, AES.MODE_EAX)
			ciphertext, tag = cipher.encrypt_and_digest(data)
			[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
			

		if sch == '2':
			file_out = open(outfile, "w")
			cipher = ChaCha20.new(key=userkey)
			ciphertext = cipher.encrypt(data)
			nonce = b64encode(cipher.nonce).decode('utf-8')
			ct = b64encode(ciphertext).decode('utf-8')
			result = json.dumps({'nonce':nonce, 'ciphertext':ct})
			file_out.write(result)

		if sch == '3':
			plaintext = file.read()
			secret = get_random_bytes(32)
			cipher = Salsa20.new(key=secret)
			msg = cipher.nonce + cipher.encrypt(plaintext)
			file_out.write(result)


		file_out.close()


		f = open(outfile, "rb")
		os.remove(outfile)

		hello={
			'file_name' : os.path.basename(file) 
		}
		hey={
		'org_file' : f
		}
		r=client.post(url,data=hello,files=hey)
	else:
		if file[-1]=='/':
			file=file[0:len(file)-1]
		print(file)
		url = "http://127.0.0.1:8000/api/v1/api-add-folder/1/"
		apps = {
					'folder_name': os.path.basename(file)
				}
		r = client.post(url, data=apps)
		a = r.json()
				#print(a["pkey"])
		
		os.chdir(file)
		add_in(a["pkey"], userkey, sch)




