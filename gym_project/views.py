from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.http import HttpResponse

from chatterbot import ChatBot

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


def index(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about-us.html')

def classes(request):
    return render(request, 'class-details.html')

def services(request):
    return render(request, 'services.html')

def team(request):
    return render(request, 'team.html')

def class_timetable(request):
    return render(request, 'class-timetable.html')

def bmi_calculator(request):
    return render(request, 'bmi-calculator.html')

def gallery(request):
    return render(request, 'gallery.html')

def blog(request):
    return render(request, 'blog.html')

def error_404(request):
    return render(request, '404.html')

def contact(request):
    return render(request, 'contact.html')


def profile(request):
    return render(request, 'profile.html')

def getResponse(request):
    userMessage = request.GET.get('userMessage')  # Corrected request.GET
    # For now, just echo back the user's message as a simple response
    return HttpResponse(userMessage)