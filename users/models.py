from django.db import models
from random import randint


def random_code():
    d = randint(1000000, 100000000)
    return hex(d)[2:8]


class Institute(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=257)
    phone_number = models.CharField(max_length=20, unique=True)
    institute_code = models.CharField(
        max_length=20, default=random_code, unique=True)

    def __str__(self):
        return self.email


class Student(models.Model):
    reg_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=257)
    puc_college = models.CharField(max_length=200, blank=True, null=True)
    preffered_branch = models.CharField(max_length=100, blank=True, null=True)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.email
