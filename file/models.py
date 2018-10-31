from django.db import models
from django.urls  import reverse

# Create your models here.
class File(models.Model):
	user = models.CharField(max_length=250)
	file_name = models.CharField(max_length=250)
	org_file = models.FileField()

	#new file go to their detail view
	def get_absolute_url(self):
		return reverse('file:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return (self.file_name)



