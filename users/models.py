from django.db import models
from random import randint


def random_code():
    d = randint(1000000, 100000000)
    return hex(d)[2:8]


class Institute(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=257)
    institute_code = models.CharField(
        max_length=20, default=random_code, unique=True)

    def __str__(self):
        return self.email


class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=257)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.email
