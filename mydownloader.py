import sys
import requests
import getpass
import pickle
import os
import wget
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Cipher import Salsa20
#from Crypto.Random import get_random_bytes


file = open("login.p", 'rb')
a = pickle.load(file)


userkey = a['userkey']
sch = a['scheme']

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

directory = str(input("Give the location of file or directory where you want to download: "))
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

        if sch=='1':
            nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
            cipher = AES.new(userkey, AES.MODE_EAX, nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        if sch=='2':
            json_input = file_in.read()
            b64 = json.loads(json_input)
            nonce = b64decode(b64['nonce'])
            ciphertext = b64decode(b64['ciphertext'])
            cipher = ChaCha20.new(key=userkey, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

        if sch=='3':
            msg = file_in.read()
            msg_nonce = msg[:8]
            ciphertext = msg[8:]
            cipher = Salsa20.new(key=userkey, nonce=msg_nonce)
            plaintext = cipher.decrypt(ciphertext)

        os.remove(filename)

        file_out = open(filename, 'wb')
        file_out.write(plaintext)
        



    for f in a["folders"]:
        os.mkdir(f[0])
        os.chdir(f[0])
        downloader(f[1])
        os.chdir("..")
downloader(1)

