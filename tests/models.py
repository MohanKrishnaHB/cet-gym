from django.db import models
from users.models import Student
from questions.models import Question, Options


class Test(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    no_of_questions = models.IntegerField()
    total_duration = models.TimeField(auto_now=False, auto_now_add=False)
    negative_marking = models.BooleanField(default=False)
    commence_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    stop_commenceing_after = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    show_score = models.BooleanField(default=False)
    show_answers = models.BooleanField(default=False)


# class TestPartition(models.Model):
#     test = models.ForeignKey(
#         Test, on_delete=models.CASCADE, related_name="partitions")
#     title = models.CharField(max_length=50, blank=True, null=True)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     no_of_questions = models.IntegerField()


class TestQuestions(models.Model):
    # partition = models.ForeignKey(
    #     TestPartition, on_delete=models.CASCADE, related_name="questions")
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="tests")

    class Meta:
        unique_together = ['test', 'question']


class StudentTest(models.Model):
    STATUS_CHOICES = [
        ("not_attended", "not_attended"),
        ("attending", "attending"),
        ("finished", "finished")
    ]
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="tests")
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="students")
    status = models.CharField(
        max_length=20, default="not_attended", choices=STATUS_CHOICES)
    end_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    class Meta:
        unique_together = ['test', 'student']


class StudentQuestion(models.Model):
    STATUS_CHOICES = [
        ("not_attended", "not_attended"),
        ("pass", "pass"),
        ("fail", "fail")
    ]
    student_test = models.ForeignKey(
        StudentTest, on_delete=models.CASCADE, related_name="questions")
    question_test = models.ForeignKey(
        TestQuestions, on_delete=models.CASCADE, related_name="students")
    status = models.CharField(
        max_length=20, default="not_attended", choices=STATUS_CHOICES)
    points = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)
    duration = models.TimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        unique_together = ['question_test', 'student_test']


class StudentQuestionOption(models.Model):
    student_question = models.ForeignKey(
        StudentQuestion, on_delete=models.CASCADE, related_name='option')
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
