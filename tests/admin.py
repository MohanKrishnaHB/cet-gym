from django.contrib import admin
from .models import Test, TestQuestions, StudentTest, StudentQuestion, StudentQuestionOption

admin.site.register(Test)
admin.site.register(TestQuestions)
admin.site.register(StudentQuestion)
admin.site.register(StudentQuestionOption)
admin.site.register(StudentTest)
