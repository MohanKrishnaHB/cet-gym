from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('log-in', views.logIn),
    path('log-out', views.logOut),
    path('register', views.register),
    path('i/student-list', views.studentList),
    path('i/send-mail', views.sendEmail),
]
