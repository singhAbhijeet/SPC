from django.db import models
from django.urls  import reverse
from db_file_storage.model_utils import delete_file, delete_file_if_needed

# Create your models here.

class FileField(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class File(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE,blank=True,null=True)
	file_name = models.CharField(max_length=250)
	org_file = models.FileField(upload_to='file.FileField/bytes/filename/mimetype', blank=True, null=True)

	#new file go to their detail view
	def save(self, *args, **kwargs):
		delete_file_if_needed(self, 'org_file')
		super(File, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		super(File, self).delete(*args, **kwargs)
		delete_file(self, 'org_file')

	def get_absolute_url(self):
		return reverse('file:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return (self.file_name)



