from django import forms
from django.contrib.auth.models import User
from db_file_storage.form_widgets import DBClearableFileInput
from .models import File , Folder 


class UploadFileForm(forms.ModelForm):
    
	class Meta:
		model = File
		fields = ['file_name', 'org_file']
		exclude = []
		widgets = {
			'file': DBClearableFileInput
		}

class UploadFolderForm(forms.ModelForm):
    
	class Meta:
		model = Folder
		fields = ['folder_name']
		


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']