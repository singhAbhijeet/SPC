from django.conf.urls import url
from . import views



app_name = 'file'

urlpatterns = [
	# /music/


	url(r'^home/(?P<pk>[0-9]+)/$',views.indexview, name='index'),
	# /music/(some id)
	# the int is saved as single int in album_id
	# url(r'^(?P<pk>[0-9]+)/$' , views.DetailView.as_view(), name='detail'),
    #
	# #for create view
	url(r'add/(?P<pk>[0-9]+)/$', views.upload_file , name='file-add'),

	url(r'add-folder/(?P<pk>[0-9]+)/$', views.upload_folder , name='folder-add'),
	# #file/add/2/
	# url(r'update/(?P<pk>[0-9]+)/$', views.FileUpdate.as_view(), name='file-update'),
    #
	 url(r'delete/(?P<pk>[0-9]+)/$', views.FileDelete.as_view(), name='file-delete'),
    #
	 url(r'register/$',views.UserFormView.as_view(), name='register'),
	 url(r'^$', views.login_user, name='login_user'),
	url(r'^logout_user/$', views.logout_user, name='logout_user'),
	]