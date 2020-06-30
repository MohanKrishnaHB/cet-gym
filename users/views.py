from django.shortcuts import render, redirect
from .models import Student, Institute
from tests.models import StudentTest
from datetime import datetime


def logIn(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if Student.objects.filter(email=email).exists():
            student = Student.objects.filter(email=email)[0]
            if student.password == password:
                request.session['student'] = student.email
                return redirect('/test/test-list')
            else:
                return_obj = {"isPasswordInvalid": True, "email": email}
                return render(request, "login.html", return_obj)
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            if institute.password == password:
                request.session['institute'] = institute.email
                return redirect('/test/i/test-list')
            else:
                return_obj = {"isPasswordInvalid": True, "email": email}
                return render(request, "login.html", return_obj)
        else:
            return_obj = {"isEmailInvalid": True}
            return render(request, "login.html", return_obj)
        return redirect('/')


def register(request):
    try:
        del request.session['student']
        del request.session['institute']
    except KeyError:
        pass
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        # institute_code = request.POST['institute_code']
        institute_code = Institute.objects.all()[0].institute_code
        if Student.objects.filter(email=email).exists():
            return_obj = {"email_exists": True, "email": email, "name": name}
            return render(request, "register.html", return_obj)
        else:
            if Institute.objects.filter(institute_code=institute_code).exists():
                institute = Institute.objects.filter(
                    institute_code=institute_code)[0]
                student = Student(email=email, name=name,
                                  password=password, institute=institute)
                student.save()
            else:
                return_obj = {"invalid_institute": True,
                              "email": email, "name": name}
                return render(request, "register.html", return_obj)
        return redirect('/')


def logOut(request):
    try:
        del request.session['student']
        del request.session['institute']
    except KeyError:
        pass
    return redirect('/')


def hello(request):
    if request.session.get('student', False):
        email = request.session['student']
        if Student.objects.filter(email=email).exists():
            student = Student.objects.filter(email=email)[0]
            return render(request, "index.html", {"name": student.name})
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')


def formatDuration(duration):
    return duration.strftime('%H:%M:%S')
