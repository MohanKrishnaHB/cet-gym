from django.urls import path
from . import views

urlpatterns = [
    path('<int:test_id>', views.test),
    path('instructions/<int:test_id>', views.instructions),
    path('result/<int:test_id>', views.resultStudent),
    path('test-list', views.testList),
    path('set-option', views.setOption),
    path('finish/<int:student_test_id>', views.testFinishWithId),
    path('finish', views.test_finish),
    path('i/test-list', views.testListInstitute),
    path('i/create-test', views.createTestPage),
    path('i/create-test-post', views.createTest),
    path('i/result/<int:test_id>', views.resultInstitute),
    path('i/show-answers', views.updateShowResults),
    path('i/question-list', views.questionList),
    path('i/add-question', views.addQuestion),
]
