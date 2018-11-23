import sys
import requests
import getpass
import pickle
import os
import wget

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

directory = str(input("Give the location of file or directory where you want to download: "))
os.chdir(directory)


def downloader(pk):
    url = "http://127.0.0.1:8000/api/v1/api-download/" + str(pk) + "/"
    r = client.get(url)
    #print(r)
    a = r.json()
    for f in a["files"]:
        url1 = "http://127.0.0.1:8000/files/download/?name=" + str(f)
        filename = wget.download(url1, out="./")
    for f in a["folders"]:
        os.mkdir(f[0])
        os.chdir(f[0])
        downloader(f[1])
        os.chdir("..")
downloader(1)

