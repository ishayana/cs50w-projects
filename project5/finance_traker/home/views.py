from django.shortcuts import render, redirect
from django import views
from accounts.froms import LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from userprofile.views import userprofile_view

def control_authentication(request):
    if not request.user.is_authenticated:
        return home_view(request)
    else:
        return userprofile_view(request)

def home_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, f'Dear {request.user.username}, you logged in succussfully!', 'success')
                return redirect('home:home')
        messages.warning(request,'The Username or password is wrong!', 'warning')
        return render(request, 'home/home.html', {'loginform' : form})
    form = LoginForm()
    return render(request, 'home/home.html', {'loginform' : form})
