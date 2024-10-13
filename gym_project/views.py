from django.shortcuts import render

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
