from django.shortcuts import render, redirect, HttpResponse
from users.models import Student, Institute
from .models import StudentTest, Test, TestQuestions, StudentQuestion, StudentQuestionOption
from datetime import datetime, timedelta, time
from questions.models import Options, CategoryLevel1, CategoryLevel2, Question
from django.core.files.storage import FileSystemStorage

def testList(request):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            # tests = student.tests
            tests = StudentTest.objects.filter(student=student)
            started_tests = []
            yet_to_start_tests = []
            finished_tests = []
            missed_tests = []
            attending_tests = []
            now = datetime.now() + timedelta(hours=5, minutes=30)
            now = now.isoformat()
            for test in tests:
                # print("commence at:", test.test.commence_at.isoformat())
                # print("stop commencing after:",
                #       test.test.stop_commenceing_after.isoformat())
                # print("now:", now)
                if test.test.commence_at.isoformat() > now and test.status == "not_attended":
                    yet_to_start_tests.append(test.test)
                elif test.test.stop_commenceing_after.isoformat() < now and test.status == "not_attended":
                    missed_tests.append(test.test)
                elif test.status == "finished":
                    finished_tests.append(test.test)
                elif test.test.commence_at.isoformat() < now and test.test.stop_commenceing_after.isoformat() > now and test.status == "not_attended":
                    started_tests.append(test.test)
                elif test.end_at.isoformat() < now and test.status == "attending":
                    test.status="finished"
                    test.save()
                    finished_tests.append(test.test)
                elif test.status == "attending":
                    attending_tests.append(test.test)
            return_obj = {
                "started_tests": started_tests,
                "missed_tests": missed_tests,
                "finished_tests": finished_tests,
                "yet_to_start_tests": yet_to_start_tests,
                "attending_tests": attending_tests,
                "student": student
            }
            # print(return_obj)
            return render(request, "test_list.html", return_obj)
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')


def inTestTimings(test):
    now = datetime.now() + timedelta(hours=5, minutes=30)
    now = now.isoformat()
    if test.commence_at.isoformat() < now and test.stop_commenceing_after.isoformat() > now:
        return True
    return False

def getTimeObj(dt):
    hr = dt.strftime('%H')
    min = dt.strftime('%M')
    sec = dt.strftime('%S')
    return {'hr': hr, 'min': min, 'sec': sec}

def getTimeObjTimeDelta(dt):
    total_sec = int(dt.seconds)
    sec = total_sec%60
    total_min = int(total_sec/60)
    hr = int(total_min/60)
    min = total_min%60
    return {'hr': hr, 'min': min, 'sec': sec}

def startTest(student_test):
    test = student_test.test
    duration = getTimeObj(test.total_duration)
    # if not student_test.end_at and student_test.status == "not_attended":
    if student_test.status == "not_attended":
        hr = int(test.total_duration.strftime('%H'))
        min = int(test.total_duration.strftime('%M'))
        sec = int(test.total_duration.strftime('%S'))
        now = datetime.now() + timedelta(hours=5, minutes=30)
        # now = now.isoformat()
        student_test.end_at = now + timedelta(hours=hr, minutes=min, seconds=sec+10)
        duration = getTimeObj(test.total_duration)
    elif student_test.end_at.isoformat() < now.isoformat():
        duration = False
    elif student_test.status == "attending":
        format = "%Y-%m-%d %H:%M:%S.%f"
        end_at_formated = student_test.end_at.strftime(format)
        end_at_datetime = datetime.strptime(end_at_formated, format)
        datetime_now_formated = now.strftime(format)
        datetime_now_datetime = datetime.strptime(datetime_now_formated, format)
        d = end_at_datetime - datetime_now_datetime
        duration = getTimeObjTimeDelta(d)
    student_test.status = 'attending'
    student_test.save()
    test_questions = test.questions.all()
    # questions = []
    for test_question in test_questions:
        try:
            sq = StudentQuestion(student_test=student_test, question_test=test_question)
            sq.save()
        except:
            sq = StudentQuestion.objects.filter(student_test=student_test, question_test=test_question)[0]
        # temp = {
        #     'question': test_question.question,
        #     'sq_id': sq.id,
        #     'options': test_question.question.options.all()
        # }
        # questions.append(temp)
    
    student_questions = StudentQuestion.objects.filter(student_test=student_test)
    questions = []
    for student_question in student_questions:
        # print("question:", student_question.question_test.question)
        options = []
        question_options = student_question.question_test.question.options.all()
        student_options = student_question.option.all()
        is_correct = False
        for option in question_options:
            # print("option:", option.option)
            is_marked = False
            for student_option in student_options:
                # print("student option:", student_option.option.option)
                if option.id == student_option.option.id:
                    # print("marked")
                    is_marked = True
                    # print(option.is_true)
            options.append({
                "option": option,
                "is_marked": is_marked
            })
        if is_correct:
            score += 1
        questions.append({
            "question": student_question.question_test.question,
            "sq_id": student_question.id,
            "options": options
        })
    return questions, duration

def test(request, test_id):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            test = Test.objects.get(id=test_id)
            if StudentTest.objects.filter(student=student, test=test).exists():
                student_test = StudentTest.objects.filter(student=student, test=test)[0]
                if student_test.status == "not_attended":
                    questions, duration = startTest(student_test)
                    return render(request, "test.html", {"duration": duration, "questions": questions, 'test': test, 'student_test_id':student_test.id})
                if student_test.status == "attending":
                    questions, duration = startTest(student_test)
                    if duration == False:
                        student_test.status="finished"
                        student_test.save()
                        return redirect("/test/test-list")
                    return render(request, "test.html", {"student": student, "duration": duration, "questions": questions, 'test': test, 'student_test_id':student_test.id})
                return redirect('/test/test-list')
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def setOption(request):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            student_question_id = request.GET['student_question_id']
            student_question = StudentQuestion.objects.get(id=student_question_id)
            option_id = request.GET['option_id']
            option = Options.objects.get(id=option_id)
            if request.GET['is_marked']=='true':
                is_marked = True
            else:
                is_marked = False
            if student_question.question_test.question.has_multiple_answers:
                if is_marked:
                    studentoption = StudentQuestionOption(student_question=student_question, option=option)
                    studentoption.save()
                else:
                    studentoption = StudentQuestionOption.objects.filter(student_question=student_question, option=option)[0]
                    studentoption.delete()
                return HttpResponse(True)
            else:
                try:
                    studentoption = StudentQuestionOption.objects.filter(student_question=student_question)
                    studentoption.delete()
                except:
                    pass
                studentoption = StudentQuestionOption(student_question=student_question, option=option)
                studentoption.save()
                return HttpResponse(True)
        else:
            return HttpResponse(False)
    else:
        return HttpResponse(False)

def testFinishWithId(request, student_test_id):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            # student = Student.objects.filter(phone_number=phone_number)[0]
            student_test = StudentTest.objects.get(id=student_test_id)
            student_test.status = 'finished'
            student_test.save()
            return redirect('/test/finish')
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def test_finish(request):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            return render(request, 'test_finish.html', {"student": student})
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def testListInstitute(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            tests = Test.objects.all()
            finished_tests = []
            yet_to_start_tests = []
            started_tests = []
            now = datetime.now() + timedelta(hours=5, minutes=30)
            now = now.isoformat()
            for test in tests:
                # print("commence at:", test.test.commence_at.isoformat())
                # print("stop commencing after:",
                #       test.test.stop_commenceing_after.isoformat())
                # print("now:", now)
                hr = int(test.total_duration.strftime('%H'))
                min = int(test.total_duration.strftime('%M'))
                sec = int(test.total_duration.strftime('%S'))
                finish_time = test.stop_commenceing_after + timedelta(hours=hr, minutes=min, seconds=sec+10)
                started_time = test.stop_commenceing_after + timedelta(hours=hr, minutes=min, seconds=sec+10)
                if test.commence_at.isoformat() > now:
                    temp = {
                        "test": test,
                        "total_number_of_students": len(test.students.all())
                    }
                    yet_to_start_tests.append(temp)
                elif finish_time.isoformat() < now:
                    temp = {
                        "test": test,
                        "total_number_of_students": len(test.students.all()),
                        "attended_students": len(test.students.filter(status="finished"))
                    }
                    finished_tests.append(temp)
                elif test.commence_at.isoformat() < now and started_time.isoformat() > now:
                    temp = {
                        "test": test,
                        "total_number_of_students": len(test.students.all()),
                        "started_students": len(test.students.filter(status__in=["attending", "finished"]))
                    }
                    started_tests.append(temp)
            return_obj = {"institute": institute, "finished_tests": finished_tests, "started_tests": started_tests, "yet_to_start_tests": yet_to_start_tests}
            return render(request, 'test_list_institute.html', return_obj)
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def createTestPage(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            categories = []
            category1 = CategoryLevel1.objects.all()
            for cat1 in category1:
                category2 = cat1.sub_categories.all()
                sub_categories = []
                for cat2 in category2:
                    questions = cat2.questions.all()
                    questions_response = []
                    question_ids = []
                    for question in questions:
                        options = question.options.all()
                        temp = {
                            "id": question.id,
                            "question": question.question,
                            "image": question.question_image,
                            "has_multiple_answers": question.has_multiple_answers,
                            "options": options
                        }
                        question_ids.append(str(question.id))
                        questions_response.append(temp)

                    sub_categories.append({
                        "title": cat2.title,
                        "id": cat2.id,
                        "questions": questions_response,
                        "all_questions_id": ",".join(question_ids)
                    })
                categories.append({
                    "title": cat1.title,
                    "id": cat1.id,
                    "sub_categories": sub_categories
                })
            # print(categories)
            return render(request, 'create_test_select_questions.html', {"institute": institute, "categories": categories})
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')


def createTest(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            if request.method == 'POST':
                title = request.POST['title']
                description = request.POST['description']
                total_duration = request.POST['total_duration']
                total_duration = time(hour=int(total_duration[:2]), minute=int(total_duration[3:]))
                commence_at = request.POST['commence_at']
                commence_at = datetime.strptime(commence_at, '%Y-%m-%dT%H:%M')
                stop_commencing_after = request.POST['stop_commencing_after']
                stop_commencing_after = datetime.strptime(stop_commencing_after, '%Y-%m-%dT%H:%M')
                questions = request.POST['questions']
                questions = questions.split(',')
                test = Test(title=title, description=description, no_of_questions=len(questions), total_duration=total_duration, commence_at=commence_at, stop_commenceing_after=stop_commencing_after)
                test.save()
                try:
                    for question in questions:
                        question_obj = Question.objects.get(id=int(question))
                        test_question = TestQuestions(test=test, question=question_obj)
                        test_question.save()
                except:
                    # print("Questions not selected")
                    pass
                students = Student.objects.all()
                for student in students:
                    student_test = StudentTest(test=test, student=student)
                    student_test.save()
                return redirect('/test/i/test-list')
            else:
                return redirect('/test/i/test-list')
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def resultInstitute(request, test_id):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            test = Test.objects.get(id=test_id)
            students = test.students.all()
            students_response = []
            for student in students:
                # print("---------=============---------------")
                # print("student:", student.student)
                student_questions = StudentQuestion.objects.filter(student_test=student)
                questions = []
                score = 0
                total_questions = len(student_questions)
                for student_question in student_questions:
                    # print("question:", student_question.question_test.question)
                    options = []
                    question_options = student_question.question_test.question.options.all()
                    student_options = student_question.option.all()
                    is_correct = False
                    for option in question_options:
                        # print("option:", option.option)
                        is_marked = False
                        for student_option in student_options:
                            # print("student option:", student_option.option.option)
                            if option.id == student_option.option.id:
                                # print("marked")
                                is_marked = True
                                if option.is_true:
                                    is_correct = True
                        options.append({
                            "option": option,
                            "is_marked": is_marked
                        })
                    if is_correct:
                        score += 1
                    questions.append({
                        "question": student_question.question_test.question,
                        "options": options,
                        "is_correct": is_correct
                    })
                students_response.append({
                    "student": student.student,
                    "questions": questions,
                    "score": score,
                    "total_questions": total_questions
                })
            response_obj = {"institute": institute, "students": students_response}
            return render(request, "test_results_institute.html", response_obj)
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def updateShowResults(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            # institute = Institute.objects.filter(email=email)[0]
            test_id = request.GET['test_id']
            is_true = request.GET['is_true']
            test = Test.objects.get(id=test_id)
            if is_true:
                test.show_score = True
                test.show_answers = True
            else:
                test.show_score = False
                test.show_answers = False
            test.save()
            return HttpResponse(True)
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def resultStudent(request, test_id):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            test = Test.objects.get(id=test_id)
            student_test = StudentTest.objects.filter(student=student, test__id=test_id)[0]
            student_questions = StudentQuestion.objects.filter(student_test=student_test)
            questions = []
            score = 0
            total_questions = len(student_questions)
            for student_question in student_questions:
                # print("question:", student_question.question_test.question)
                options = []
                question_options = student_question.question_test.question.options.all()
                student_options = student_question.option.all()
                is_correct = False
                for option in question_options:
                    # print("option:", option.option)
                    is_marked = False
                    for student_option in student_options:
                        # print("student option:", student_option.option.option)
                        if option.id == student_option.option.id:
                            # print("marked")
                            is_marked = True
                            # print(option.is_true)
                            if option.is_true:
                                is_correct = True
                    options.append({
                        "option": option,
                        "is_marked": is_marked
                    })
                if is_correct:
                    score += 1
                questions.append({
                    "question": student_question.question_test.question,
                    "options": options,
                    "is_correct": is_correct
                })
            return_obj = {"test": test, "student": student,"score": score, "questions": questions, "total_questions": total_questions}
            return render(request, "test_result_student.html", return_obj)
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def instructions(request, test_id):
    if request.session.get('student', False):
        phone_number = request.session['student']
        if Student.objects.filter(phone_number=phone_number).exists():
            student = Student.objects.filter(phone_number=phone_number)[0]
            test = Test.objects.get(id=test_id)
            return render(request, "instruction.html", {"test": test})
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def questionList(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            categories = []
            category1 = CategoryLevel1.objects.all()
            for cat1 in category1:
                category2 = cat1.sub_categories.all()
                sub_categories = []
                for cat2 in category2:
                    questions = cat2.questions.all()
                    questions_response = []
                    for question in questions:
                        options = question.options.all()
                        temp = {
                            "id": question.id,
                            "question": question.question,
                            "image": question.question_image,
                            "has_multiple_answers": question.has_multiple_answers,
                            "options": options
                        }
                        questions_response.append(temp)
                    sub_categories.append({
                        "title": cat2.title,
                        "id": cat2.id,
                        "questions": questions_response
                    })
                categories.append({
                    "title": cat1.title,
                    "id": cat1.id,
                    "sub_categories": sub_categories
                })
            # print(categories)
            return render(request, 'questions.html', {"institute": institute, "categories": categories})
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')

def addQuestion(request):
    if request.session.get('institute', False):
        email = request.session['institute']
        if Institute.objects.filter(email=email).exists():
            institute = Institute.objects.filter(email=email)[0]
            category = request.POST['category']
            category = CategoryLevel2.objects.get(id=category)
            question_title = request.POST['question']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            correct_option = request.POST['option']
            co1, co2, co3, co4 = False, False, False, False
            if correct_option == "option1":
                co1 = True
            elif correct_option == "option2":
                co2 = True
            elif correct_option == "option3":
                co3 = True
            elif correct_option == "option4":
                co4 = True
            try:
                question_image = request.FILES['questionimage']
                question = Question(question=question_title, category=category, question_image=question_image)
                question.save()
            except:
                question = Question(question=question_title, category=category)
                question.save()
            try:
                optionimage = request.FILES['option1image']
                option = Options(question=question, option=option1, image=optionimage, is_true=co1)
                option.save()
            except:
                option = Options(question=question, option=option1, is_true=co1)
                option.save()
            
            try:
                optionimage = request.FILES['option2image']
                option = Options(question=question, option=option2, image=optionimage, is_true=co2)
                option.save()
            except:
                option = Options(question=question, option=option2, is_true=co2)
                option.save()
            try:
                optionimage = request.FILES['option3image']
                option = Options(question=question, option=option3, image=optionimage, is_true=co3)
                option.save()
            except:
                option = Options(question=question, option=option3, is_true=co3)
                option.save()
            try:
                optionimage = request.FILES['option4image']
                option = Options(question=question, option=option4, image=optionimage, is_true=co4)
                option.save()
            except:
                option = Options(question=question, option=option4, is_true=co4)
                option.save()
            return redirect("/test/i/question-list")
        else:
            return redirect('/log-in')
    else:
        return redirect('/log-in')