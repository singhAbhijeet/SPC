import sys
import requests
import getpass
import pickle

user = str(input("Enter username: "))
email=str(input("Enter Email: "))
password1 = getpass.getpass("Enter Password: ")
password2 = getpass.getpass("Confirm Password: ")
if password1!=password2:
	print("Passwords do not match")
	exit()
else:
	client = requests.session()

	url = "http://127.0.0.1:8000/api/v1/rest-auth/registration/"
	reg_data = {
		'username': user,
		'password1': password1,
		'password2' : password2,
	    'email' : email
	}
	# client.get(url)
	response = client.post(url, data=reg_data)
	a = response.json()
	if "key" in a:
	 	print(" successful registration")
	else:
		print("registration failed")

# file = open("login.p", 'rb')
# a = pickle.load(file)
# print(a)
