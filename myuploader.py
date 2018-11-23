import sys
import requests
import getpass
import pickle
import os
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Cipher import Salsa20

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

userkey = a['userkey']
sch = a['scheme']


Location = input("Give the location of file or directory to upload: ")
if(os.path.isfile(Location)):
    url="http://127.0.0.1:8000/api/v1/api-add-file/1/"
    f=open(Location,'rb')
    data = f.read()
    outfile = os.path.basename(Location)
    

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
        'file_name' : os.path.basename(Location) 
    }
    hey={
    'org_file' : f
    }
    r=client.post(url,data=hello,files=hey)
else:
    if Location[-1]=='/':
        Location=Location[0:len(Location)-1]
    print(Location)
    url = "http://127.0.0.1:8000/api/v1/api-add-folder/1/"
    apps = {
                'folder_name': os.path.basename(Location)
            }
    r = client.post(url, data=apps)
    a = r.json()
            #print(a["pkey"])
    
    os.chdir(Location)
    add_in(a["pkey"], userkey, sch)



