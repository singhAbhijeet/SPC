import sys
import requests
import getpass
import pickle
import os
import json
def add_in(pk):
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
            add_in(a["pkey"])
            os.chdir("..")
        else:
            url="http://127.0.0.1:8000/api/v1/api-add-file/"+str(pk)+"/"
            f=open(file,'rb')
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



Location = input("Give the location of file or directory to upload: ")
if(os.path.isfile(Location)):
    url="http://127.0.0.1:8000/api/v1/api-add-file/1/"
    f=open(Location,'rb')
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
    add_in(a["pkey"])



