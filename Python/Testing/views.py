from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from models import Question, Test, User_Profile, Test_Summary, Class, Free_Radicals,Question_Summary, Test_Report
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import JsonResponse
from django.core.mail import EmailMessage
 


@csrf_exempt
def create_test_backup(request):
    test_obj = json.loads(request.body)
    test = Test()
    #import pdb; pdb.set_trace()
    if request.user.is_authenticated():
        owner = User_Profile.objects.filter(user = request.user)
        test.owner = owner[0]
        test.test_name = test_obj['PRE_TEST']['test_name']
        #test.subject = test_obj['PRE_TEST'].subject
        #test.target_exam = test_obj['PRE_TEST'].target_exam
        #test.topics = test_obj['PRE_TEST'].topics_included
        test.total_time = test_obj['PRE_TEST']['total_time']
        test.pass_criteria = test_obj['PRE_TEST']['pass_criteria']
        test.assoicated_class = Class.objects.get(pk=test_obj['CLASS_INFO'])
        test.save()
        try:
            for item in test_obj['QUESTIONS']:
                question = Question()
                question.question_text = item['question_text']
                question.explanation = item['explanation']
                question.options = json.dumps(item['options'])
                question.hint = item['hint']
                question.difficulty = item['difficulty_level']
                question.points = item['points']
                question.owner = owner[0]
                #question.target_exam = test.target_exam
                #question.subject = test.subject
                #question.topic = item.topic
                question.save()
                test.questions.add(question)
            data = {"status" : "success"}
            return JsonResponse(data)
        except Exception, e:
            raise e
    else:
        data = {"status" : "failure"}
        return JsonResponse(data)



@csrf_exempt
def get_test(request):
    #import pdb; pdb.set_trace()
    test_id = request.session['test_id']
    test = Test.objects.get(pk=test_id)
    question_set = Test.objects.get(pk=test_id).questions.all()
    questions = {};
    for item in question_set:
        questions[item.id] = {}
        questions[item.id]['question'] = item.question_text
        questions[item.id]['options'] = []
        options = json.loads(item.options)
        for opt in options:
            opt_obj = {"option" : opt['option'] , "selected" : False};
            questions[item.id]['options'].append(opt_obj)
    #import pdb; pdb.set_trace()
    ret_obj = {'test_id' : test_id, 'test_name' : test.test_name, 'total_time' : test.total_time, 'questions' : questions}
    return JsonResponse(ret_obj)


@csrf_exempt
def compute_results(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    test_summary = Test_Summary()
    user = User_Profile.objects.filter(user = request.user)
    test_summary.user = user[0]
    test_id = request.session['test_id']
    test_summary.test = Test.objects.get(pk=test_id)
    incorrect = False
    
    total_score = 0
    user_score = 0
    questions_count = 0
    unsolved_count = 0
    solved_count = 0
    correct_count = 0
    total_time = 0
    test_summary.save()
    for item in result_obj['answers']:
        question = Question.objects.get(pk=item['id'])
        total_score = total_score + question.points
        questions_count = questions_count + 1
        
        question_summary = Question_Summary()
        question_summary.user = user[0]
        question_summary.test_summary = test_summary
        question_summary.time_taken = item['time_taken']
        question_summary.attempted = True
        question_summary.correct = False
        question_summary.question = question

        if not item['selected']:
            unsolved_count = unsolved_count + 1
            question_summary.attempted = False
            continue
        else:
            solved_count = solved_count + 1
            opt_list = json.loads(question.options)
            for opt in opt_list:
                if 'correct' in opt :
                    if opt['option'] in item['selected'] :
                        incorrect = False
                        correct_count = correct_count +1
                        question_summary.correct = True
                    else:
                        incorrect = True
            if not incorrect:
                user_score = user_score + question.points
        question_summary.save()
    result = {"user_score" : user_score , "total_score" : total_score}
    test_summary.marks_scored = user_score
    test_summary.total_marks = total_score
    test_summary.user.score = test_summary.user.score + user_score
    test_summary.total_time = result_obj['total_time_taken']
    test_summary.total_questions = questions_count
    test_summary.solved_count = solved_count
    test_summary.correct_count = correct_count
    test_summary.unsolved_count = unsolved_count
    test_summary.user.save()
    test_summary.save()

    test_report = test_summary.test.Test_Report.all()
    if not test_report:
        test_report = Test_Report()
        test_report.test_summary = test_summary
        test_report.topper = user[0]
        test_report.test = test_summary.test
        test_report.save()
    else:
        if total_score > test_report[0].test_summary.marks_scored:
            test_report[0].test_summary = test_summary
            test_report[0].topper = user[0]
            test_report[0].save()
    return JsonResponse(result)
            

@csrf_exempt
def get_home(request):
    return render_to_response('index.html')

@csrf_exempt
def get_dashboard(request):
    return render_to_response('home.html')

@csrf_exempt
def test_view(request):
    return render_to_response('attempt_view.html')

@csrf_exempt
def start_test(request):
    return render_to_response('start_test.html')

@csrf_exempt
def test_create(request):
    return render_to_response('create_test.html')


def check_and_clear_free_radical(user_profile):
    #import pdb; pdb.set_trace()
    user = Free_Radicals.objects.filter(email = user_profile.user.username)
    if not user:
        return True
    else :
        for invite in user:
            class_assoc = Class.objects.get(pk=invite.class_associated.id)
            class_assoc.students.add(user_profile)
            invite.delete()
        return True

@csrf_exempt
def register_user(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    username = result_obj['email']
    email = result_obj['email']
    name = result_obj['name']
    password = result_obj['password']
    New_User = User_Profile()
    return_msg = {"msg" : "Success"}
    try:
        if User.objects.filter(username=username).exists():
            return_msg['msg'] = "Username already exists"
        else:
            user = User.objects.create_user(username, email=email, password=password, first_name= name)
            New_User.user = user
            New_User.user_type = result_obj['user_type']
            New_User.save()
            user_acc = authenticate(username=username, password=password)
            if user_acc:
                if user_acc.is_active:
                    login(request, user_acc)
                    check_and_clear_free_radical(New_User)
                    return JsonResponse(return_msg)
            else:
                return_msg['msg'] = "Error Occoured. Please Try Again"
                return JsonResponse(return_msg)
    except Exception, e:
        return_msg['msg'] = e
    return JsonResponse(return_msg)


@csrf_exempt
def login_user(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    username = result_obj['email']
    password = result_obj['password']
    return_msg = {"msg" : "Success"}
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return JsonResponse(return_msg)
        else:
            return_msg = {"msg" : "Your Tutor account is disabled."}
            return JsonResponse(return_msg)
    else:
        return_msg['msg'] =  "Invalid login details: {0}, {1}".format(username, password)
        return JsonResponse(return_msg)


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def get_user_info(request):
    #import pdb; pdb.set_trace()
    user_profile = User_Profile.objects.filter(user = request.user)
    return_user = {"username" :  request.user.username,"score" : user_profile[0].score, "user_type" : user_profile[0].user_type,"email" : request.user.email,"name" : request.user.first_name}
    return JsonResponse(return_user)

@csrf_exempt
def get_all_tests(request):
    #import pdb; pdb.set_trace()
    return_obj = []
    user = User_Profile.objects.filter(user = request.user)
    if user[0].user_type == 1:
        tests = Test.objects.all()
    else:
        tests = Test.objects.filter(owner = user[0])
    for test in tests:
        test_info = {"id" : test.id, "name_info" : test.test_name}
        return_obj.append(test_info)
    ret_obj = {"test_info" : return_obj}
    return JsonResponse(ret_obj)


@csrf_exempt
def get_user_solved_tests(request):
    #import pdb; pdb.set_trace()
    return_obj = []
    user_profile = User_Profile.objects.filter(user = request.user)
    tests = Test_Summary.objects.filter(user = user_profile[0])
    for test in tests:
        test_info = {"id" : test.test.id, "summary_id" :  test.id, "name_info" : test.test.test_name, "user_score" : test.marks_scored, "total_score" : test.total_marks}
        return_obj.append(test_info)
    ret_obj = {"test_info" : return_obj}
    return JsonResponse(ret_obj)



@csrf_exempt
def testwise_students_info(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    total_score = 0
    return_obj = []
    test_obj = Test.objects.get(pk=result_obj['test_id'])
    test_user_summary = Test_Summary.objects.filter(test = test_obj)
    for item in test_user_summary:
        item_info = {"user_id" : item.user.id , "user_name" : item.user.user.username, "score" : item.marks_scored}
        return_obj.append(item_info)
    if not test_user_summary :
        total_score = 0
    else:
        total_score = test_user_summary[0].total_marks
    ret_obj = {"user_info" : return_obj, "total_score" : total_score}
    return JsonResponse(ret_obj)


@csrf_exempt
def get_all_students_score(request):
    #import pdb; pdb.set_trace()
    return_obj = []
    users = User_Profile.objects.filter(user_type = 1)
    for user in users:
        user_info = {"id" : user.id, "name" : user.user.username, "score" : user.score}
        return_obj.append(user_info)
    ret_obj = {"user_info" : return_obj}
    return JsonResponse(ret_obj)


@csrf_exempt
def save_test_id(request):
    result_obj = json.loads(request.body)
    test_id = result_obj['id']
    request.session['test_id'] = test_id
    return HttpResponse("Success")

@csrf_exempt
def clear_test_id(request):
    request.session['test_id'] = -1
    return HttpResponse("Success")


def add_students_in_class(val, class_id):
    import pdb; pdb.set_trace()
    result_obj = val
    return_obj = {"msg" : "Success"}
    class_obj = Class.objects.get(pk=class_id)
    subject = "Instructor, " + class_obj.instructor.user.first_name + " Invited you to ToppersNotes. " 
    body = "\nPlease follow the link below and Register yourself with your email as username to access all the Tests shared by your Instructor \n Link : http://127.0.0.1:8000 \n \n See you there :-) \n ToppersNotes Team"
    for user in result_obj['users']:
        try:
            radical = Free_Radicals()
            radical.email = user
            radical.class_associated = class_obj
            radical.save()
            email = EmailMessage(subject, body, to=[user])
            email.send()
            return_obj = {"msg" : "Success"}
        except Exception, e:
            return_obj = {"msg" : e}
    return return_obj


@csrf_exempt
def add_student(request):
    import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    val = {"users" : result_obj['users']}
    obj = add_students_in_class(val, result_obj['class_id'])
    return JsonResponse(obj)

@csrf_exempt
def create_class(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    user_profile = User_Profile.objects.filter(user = request.user)
    new_class = Class()
    new_class.name = result_obj['name']
    new_class.instructor = user_profile[0]
    new_class.save()
    add_students_in_class(result_obj, new_class.id)
    return_obj = {"class_id" : new_class.id}
    return JsonResponse(return_obj)


@csrf_exempt
def get_user_classes(request):
    #import pdb; pdb.set_trace()
    return_obj = []
    user_profile = User_Profile.objects.filter(user = request.user)
    classes = user_profile[0].User_Profile_Instructor.all()
    for class_item in classes:
        item = {"class_id" : class_item.id , "class_name" : class_item.name}
        return_obj.append(item)
    ret_obj = {"classes" : return_obj}
    return JsonResponse(ret_obj)


@csrf_exempt
def send_mail_to_class(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    class_assoc = Class.objects.get(pk=result_obj['class_id'])
    free_radicals = Free_Radicals.objects.filter(class_associated = class_assoc)
    subject = "Instructor, " + class_assoc.instructor.user.first_name + " Invited you to ToppersNotes. " 
    body = "\nPlease follow the link below and Register yourself with your email as username to access all the Tests shared by your Instructor \n Link : http://127.0.0.1:8000 \n \n See you there :-) \n ToppersNotes Team"
    for user in free_radicals:
         email = EmailMessage(subject, body, to=[user.email])
         email.send()
    return HttpResponse("Success")    


@csrf_exempt
def get_all_tests_classwise(request):
    #import pdb; pdb.set_trace()
    return_obj = []
    user_profile = User_Profile.objects.filter(user = request.user)
    if user_profile[0].user_type == 1:
        all_classes = user_profile[0].User_Profile_Students.all()
    else :
        all_classes = user_profile[0].User_Profile_Instructor.all()
    for item in all_classes:
        tests = item.Class_Test.all()
        for test in tests:
            test_info = {"id" : test.id, "name_info" : test.test_name}
            return_obj.append(test_info)
    ret_obj = {"test_info" : return_obj}
    return JsonResponse(ret_obj)


#View for Analytics
@csrf_exempt
def donut_graph_view(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    user_profile = User_Profile.objects.filter(user = request.user)
    test_summary = Test_Summary.objects.get(pk=result_obj['test_summary_id'])
    incorrect = test_summary.solved_count - test_summary.correct_count
    ret_obj = {"unsolved" : test_summary.unsolved_count, "correct": test_summary.correct_count, "incorrect" : incorrect}
    return JsonResponse(ret_obj)


@csrf_exempt
def per_question_time_taken(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    ret_obj = {};
    time_taken = []
    test_summary = Test_Summary.objects.get(pk=result_obj['test_summary_id'])
    questions_summary = test_summary.Questions.all()
    for question in questions_summary:
        time_taken.append(question.time_taken)
    ret_obj = {"time_taken" : time_taken}
    return JsonResponse(ret_obj)


@csrf_exempt
def per_question_time_taken_topper(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    ret_obj = {};
    time_taken = []
    test_report = Test_Report.objects.filter(test=result_obj['test_id'])
    questions_summary = test_report.test_summary.Questions.all()
    for question in questions_summary:
        time_taken.append(question.time_taken)
    ret_obj = {"time_taken" : time_taken}
    return JsonResponse(ret_obj)


@csrf_exempt
def test_summary_students_rank(request):
    #import pdb; pdb.set_trace()
    result_obj = json.loads(request.body)
    scores = []
    ret_obj = {"scores" : [] , "min_user_rank" : 0, "max_user_rank" : 0};
    test_summary = Test_Summary.objects.get(pk=result_obj['test_summary_id'])
    user_score = test_summary.marks_scored
    test = test_summary.test
    test_instances = test.Test_Solved_Summary.all()
    for test in test_instances:
        scores.append(test.marks_scored)
    desc_score = sorted(scores, reverse=True)
    ret_obj["min_user_rank"] = desc_score.index(user_score) + 1
    ret_obj["max_user_rank"] = len(desc_score) - desc_score[-1::-1].index(user_score)
    ret_obj["scores"] = desc_score
    return JsonResponse(ret_obj)


@csrf_exempt
def overall_percentage(request):
    #import pdb; pdb.set_trace()
    user_profile = User_Profile.objects.filter(user = request.user)
    user_tests = user_profile[0].User_Test_Summary.all()
    user_score = 0.0
    total_score = 0.0
    ret_obj = {"percentage" : 0}
    for test in user_tests:
        user_score = user_score + test.marks_scored
        total_score = total_score + test.total_marks
    ret_obj['percentage'] =  (user_score/total_score) * 100.0
    return JsonResponse(ret_obj)


@csrf_exempt
def basic_user_test_stats(request):
    test_summary = Test_Summary.objects.get(pk=result_obj['test_summary_id'])
    ret_obj = {"user_score" : 0, "total_score" : 0, "total_time" : 0, "accuracy" : 0}
    ret_obj["user_score"] = test_summary.marks_scored
    ret_obj["total_score"] = test_summary.total_marks
    ret_obj["total_time"] = test_summary.total_time
    ret_obj["accuracy"] = (test_summary.correct_count * 1.0 / test_summary.solved_count) * 100.0
    return JsonResponse(ret_obj)


@csrf_exempt
def get_test_analytics(request):
    result_obj = json.loads(request.body)
    ret_obj = {"DONUT" : {}, "TIME_TAKEN_PER_QUESTION" : {"You" : [], "Topper" : []}, "STUDENT_RANKS" : {}}
    test_summary = Test_Summary.objects.get(pk=result_obj['test_summary_id'])
    result_obj = json.loads(request.body)
    test_summary = Test_Summary.objects.get(pk=result_obj['test_summary_id'])
    
    #DONUT specific:
    incorrect = test_summary.solved_count - test_summary.correct_count
    ret_obj["DONUT"] = {"unsolved" : test_summary.unsolved_count, "correct": test_summary.correct_count, "incorrect" : incorrect}
    
    #PEr question time taken 
    time_taken = ["You"]
    questions_summary = test_summary.Questions.all()
    for question in questions_summary:
        time_taken.append(question.time_taken)
    ret_obj["TIME_TAKEN_PER_QUESTION"]["You"] = time_taken
    
    # Per question time taken topper
    time_taken = ["Topper"]
    test_report = Test_Report.objects.filter(test=test_summary.test)
    questions_summary = test_report[0].test_summary.Questions.all()
    for question in questions_summary:
        time_taken.append(question.time_taken)
    ret_obj["TIME_TAKEN_PER_QUESTION"]["Topper"] = time_taken
    
    #test_summary_students_rank
    #import pdb; pdb.set_trace()
    scores = ["Score", test_summary.total_marks]
    rank_ret_obj = {"scores" : [] , "min_user_rank" : 0, "max_user_rank" : 0};
    user_score = test_summary.marks_scored
    test = test_summary.test
    test_instances = test.Test_Solved_Summary.all()
    for test in test_instances:
        scores.append(test.marks_scored)
    desc_score = sorted(scores, reverse=True)
    rank_ret_obj["min_user_rank"] = desc_score.index(user_score) - 1
    rank_ret_obj["max_user_rank"] = len(desc_score) - desc_score[-1::-1].index(user_score) -2
    rank_ret_obj["scores"] = desc_score
    ret_obj["STUDENT_RANKS"] = rank_ret_obj

    #Basic INfo of Test
    basic_ret_obj = {"user_score" : 0, "total_score" : 0, "total_time" : 0, "accuracy" : 0, "test_name" : ""}
    basic_ret_obj["test_name"] = test_summary.test.test_name
    basic_ret_obj["user_score"] = test_summary.marks_scored
    basic_ret_obj["total_score"] = test_summary.total_marks
    basic_ret_obj["total_time"] = test_summary.total_time
    basic_ret_obj["accuracy"] = (test_summary.correct_count * 1.0 / test_summary.solved_count) * 100.0
    ret_obj["BASIC_INFO"] = basic_ret_obj
    return JsonResponse(ret_obj)

