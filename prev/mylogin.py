import sys
import requests
import getpass
import pickle

user = str(input("Enter username:"))
password = getpass.getpass("Enter Password:")
client = requests.session()

url = "http://127.0.0.1:8000/api/v1/rest-auth/login/"
login_data = {
    'username': user,
    'password': password,
}
# client.get(url)
response = client.post(url, data=login_data)
a = response.json()
if "key" in a:
    dic = {'user': user, 'password': password, 'key': a["key"]}
    file = open("login.p", 'wb+')
    pickle.dump(dic, file)
    file.close()
    print("Login successful")
else:
    print("Invalid Login")

# file = open("login.p", 'rb')
# a = pickle.load(file)
# print(a)
