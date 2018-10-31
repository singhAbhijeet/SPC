from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import  CreateView,UpdateView,DeleteView
from .models import File
from django.urls import reverse_lazy
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login, logout
from django.views import generic
from django.views.generic import View
from .forms  import UserForm
from django.contrib.auth.decorators  import login_required


# Create your views here.
@method_decorator(login_required)
class IndexView(generic.ListView):
	template_name = 'file/index.html'
	context_object_name =  'all_files'
	def get_queryset(self):
		return File.objects.all()

class DetailView(generic.DetailView):
	#deMANDS pk
	model = File
	template_name = 'file/detail.html'


class FileCreate(CreateView):
	model = File #for what this view is for
	fields = ['user', 'file_name', 'org_file']

class FileUpdate(UpdateView):
	model = File #for what this view is for
	fields = ['user', 'file_name', 'org_file']

class FileDelete(DeleteView):
	model = File #for what this view is for
	success_url = reverse_lazy('file:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'file/registeration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            # cleaned data-normalized
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()

            #return user objects if true
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    #refer as request.user."item"
                    return redirect('/file/')

        return render(request, self.template_name, {'form' : form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                files = File.objects.filter(user=request.user)
                return render(request, 'file/index.html', {'all_files': files})
            else:
                return render(request, 'file/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'file/login.html', {'error_message': 'Invalid login'})
    return render(request, 'file/login.html')

def logout_user(request):
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     "form": form,
    #}
    return redirect('file:login_user')
