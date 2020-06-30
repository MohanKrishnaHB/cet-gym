from django.db import models


class CategoryLevel1(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


class CategoryLevel2(models.Model):
    title = models.CharField(max_length=20, unique=True)
    category_level_1 = models.ForeignKey(CategoryLevel1, on_delete=models.SET_NULL, null=True, related_name="sub_categories")

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.TextField()
    question_image = models.ImageField(upload_to='images/question/', null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    solution_image = models.ImageField(upload_to='images/solution/', null=True, blank=True)
    category = models.ForeignKey(CategoryLevel2, on_delete=models.SET_NULL, null=True, related_name="questions")
    created_on = models.DateField(auto_now=True)
    has_multiple_answers = models.BooleanField(default=False)

    def __str__(self):
        return "Question {}".format(self.id)


class Options(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/options/', null=True, blank=True)
    is_true = models.BooleanField(default=False)

    class Meta:
        unique_together = ['question', 'option']

    def __str__(self):
        return "question {} | option {}".format(self.question.id, self.id)
