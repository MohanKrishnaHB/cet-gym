from django.shortcuts import render, redirect
from .models import Student, Institute
from tests.models import StudentTest
from datetime import datetime
import sendgrid
import os
from sendgrid.helpers.mail import *
import requests


def logIn(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            if student.password == password:
                request.session['student'] = student.phone_number
                return redirect('/test/test-list')
            else:
                return_obj = {"isPasswordInvalid": True, "email": phone_number}
                return render(request, "login.html", return_obj)
        if Institute.objects.filter(phone_number=phone_number).exists():
            institute = Institute.objects.filter(phone_number=phone_number)[0]
            if institute.password == password:
                request.session['institute'] = institute.email
                return redirect('/test/i/test-list')
            else:
                return_obj = {"isPasswordInvalid": True, "email": phone_number}
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
        phone_number = request.POST['phone_number']
        name = request.POST['name']
        reg_no = request.POST['reg_no']
        password = request.POST['password']
        puc_college = request.POST['puc_college']
        preffered_branch = request.POST['preffered_branch']
        # institute_code = request.POST['institute_code']
        institute_code = Institute.objects.all()[0].institute_code
        # if Student.objects.filter(email=email).exists():
        #     return_obj = {"email_exists": True, "email": email,"phone_number":phone_number, "name": name, "reg_no": reg_no, "puc_college":puc_college, "preffered_branch":preffered_branch}
        #     return render(request, "register.html", return_obj)
        if Student.objects.filter(phone_number=phone_number).exists():
            return_obj = {"phone_number_exists": True, "email": email,"phone_number":phone_number, "name": name, "reg_no": reg_no, "puc_college":puc_college, "preffered_branch":preffered_branch}
            return render(request, "register.html", return_obj)
        # if Student.objects.filter(reg_no=reg_no).exists():
        #     return_obj = {"reg_no_exists": True, "email": email,"phone_number":phone_number, "name": name, "reg_no": reg_no, "puc_college":puc_college, "preffered_branch":preffered_branch}
        #     return render(request, "register.html", return_obj)
        else:
            if Institute.objects.filter(institute_code=institute_code).exists():
                institute = Institute.objects.filter(
                    institute_code=institute_code)[0]
                student = Student(email=email, name=name, password=password, institute=institute, reg_no=reg_no, phone_number=phone_number, puc_college=puc_college, preffered_branch=preffered_branch)
                student.save()
            else:
                return_obj = {"invalid_institute": True,
                              "email": email, "name": name}
                return render(request, "register.html", return_obj)
        return redirect('/')


def logOut(request):
    try:
        del request.session['student']
    except:
        pass
    try:
        del request.session['institute']
    except KeyError:
        pass
    return redirect('/')


def hello(request):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            return redirect("/test/test-list")
        else:
            return redirect('/log-in')
    if request.session.get('institute', False):
        return redirect("/test/i/test-list")
    else:
        return redirect('/log-in')


def formatDuration(duration):
    return duration.strftime('%H:%M:%S')


def studentList(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            students = Student.objects.all()
            return render(request, "students.html", {"students": students, "institute": institute})
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def sendEmail(request):
    try:
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("support@mitmysore.in")
        subject = "Hello World from the SendGrid Python Library!"
        to_email = Email("mohankrishnahb@gmail.com")
        content = Content("text/plain", "Hello, Email!")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        requests.post(os.environ['BLOWERIO_URL'] + '/messages', data={'to': '+919066528665', 'message': 'Hello from Blower.io'})
        return redirect("/log-in")
    except:
        return redirect("/register")
    