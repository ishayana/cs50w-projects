from django.shortcuts import render, redirect
from django import views
from .froms import RegistrationForm
from .models import User
from django.contrib import messages
from django.contrib.auth import logout

class RegisterationView(views.View):
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/registeration.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'registerform' : form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            messages.success(request, 'Your accounts created successfully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'registerform' : form})
    

class LogoutView(views.View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully!', 'success')
        return redirect('home:home')