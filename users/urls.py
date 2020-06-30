from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('log-in', views.logIn),
    path('log-out', views.logOut),
    path('register', views.register),

]
