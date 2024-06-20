# authenticate/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from .forms import RegisterForm

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password_conf = form.cleaned_data['password_conf']
            if password == password_conf:
                new_user = User()
                new_user.username = form.cleaned_data['username']
                new_user.set_password(password)
                new_user.save()
                # Check permissions based on user's account type
                if request.POST['account_type'] == 'poster':
                    group = Group.objects.get(name='Posters')
                    new_user.groups.add(group)
                elif request.POST['account_type'] == 'viewer':
                    group = Group.objects.get(name='Viewers')
                    new_user.groups.add(group)
                login(request, new_user)
                return redirect('index')
    # If registration fails, create a new registration form
    form = RegisterForm()
    return render(request, 'registration/register.html', context={'form':form})


def logout_user(request):
    logout(request)
    return redirect('index')

