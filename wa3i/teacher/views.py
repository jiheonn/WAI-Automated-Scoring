from django.shortcuts import render, get_object_or_404
from mainpage.models import Question, Assignment, AssignmentQuestionRel, Solve, Keyword, Category, Teacher
from django.http import JsonResponse
from django.db.models import Q
import datetime

# Create your views here.
# from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    context = {

    }
    return render(request, 'teacher/index.html', context)


def question_selection(request):
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    question_data = Question.objects.all()
    context = {
        'question_data': question_data
    }
    try:
        test = request.GET.getlist('question')
        print(test)
        assignment_data = Assignment(assignment_id=request.GET['code_num'],
                                     teacher=Teacher.objects.get(teacher_id=2),
                                     assignment_title=request.GET['question-title'],
                                     type=request.GET['evaluation_type'],
                                     start_date=datetime.datetime.strptime(request.GET['start-date'],
                                                                           '%Y-%m-%d').date(),
                                     end_date=datetime.datetime.strptime(request.GET['end-date'], '%Y-%m-%d').date(),
                                     made_date=now_date,
                                     grade=int(request.GET['grade']),
                                     class_field=int(request.GET['class']))
        assignment_data.save()
    except:
        assignment_data = None

    return render(request, 'teacher/question_selection.html', context)


def view_result(request):
    assignment_data = Assignment.objects.all()
    context = {
        'assignment_data': assignment_data
    }
    return render(request, 'teacher/view_result.html', context)


def make_question(request):
    context = {
    }
    return render(request, 'teacher/make_question.html', context)


def bigram_tree(request):
    context = {
    }
    return render(request, 'teacher/bigram_tree.html', context)


def topic_analysis(request):
    context = {
    }
    return render(request, 'teacher/topic_analysis.html', context)


def response_analysis(request):
    context = {
    }
    return render(request, 'teacher/response_analysis.html', context)


def qr_code(request):
    question_data = Question.objects.all()
    context = {
        'question_data': question_data
    }
    return render(request, 'teacher/QR_code.html', context)


def teacher_notice(request):
    context = {
    }
    return render(request, 'teacher/teacher_notice.html', context)


def view_result_detail(request):
    select_code = request.GET['select_code']
    assignment_data = AssignmentQuestionRel.objects.select_related('solve', 'assignment').filter(
        assignment_id=select_code).order_by('solve__student_id')
    question_count = assignment_data.values('question_id').distinct().count()

    sum = 0
    avg = []
    test = {}
    for i in assignment_data:
        if i.solve.student_id in test:
            test[i.solve.student_id].append(i.solve.score)
        else:
            test[i.solve.student_id] = []
            test[i.solve.student_id].append(i.solve.score)
    for key in test.keys():
        test[key] = sum(test[key])/len(test[key])

    print(assignment_data)

    print(avg)

    context = {
        'assignment_data': assignment_data,
        'question_count': question_count
    }
    return render(request, 'teacher/view_result_detail.html', context)


def ex_response_analysis(request):
    context = {
    }
    return render(request, 'teacher/ex_response_analysis.html', context)


def change_qr_code(request):
    question_name = request.GET['question_name']
    qst_data = Question.objects.all().filter(question_name=question_name)

    question_data = []
    for i in qst_data:
        question_data_dict = dict()
        question_data_dict['QR_code'] = i.qr_code
        question_data.append(question_data_dict)

    context = {
        'question_data': question_data
    }
    return JsonResponse(context)


def question_search(request):
    user_input = request.GET['user_input']

    # sah_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input)
    sah_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input).values_list('question_id', flat=True).distinct()
    data = Question.objects.filter(pk__in=sah_data)
    search_data = []
    for i in data:
        search_data_dict = dict()
        search_data_dict['question_id'] = i.question_id
        search_data_dict['question_name'] = i.question_name
        search_data_dict['question_image'] = i.image
        search_data.append(search_data_dict)
    print(search_data)
    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


def view_search(request):
    user_input = request.GET['user_input']
    asi_data = Assignment.objects.all().filter(assignment_title__icontains=user_input)

    assignment_data = []
    for i in asi_data:
        assignment_data_dict = dict()
        assignment_data_dict['assignment_id'] = i.assignment_id
        assignment_data_dict['assignment_title'] = i.assignment_title
        assignment_data_dict['assignment_type'] = i.type
        assignment_data_dict['start_date'] = i.start_date
        assignment_data_dict['end_date'] = i.end_date
        assignment_data_dict['student_grade'] = i.grade
        assignment_data_dict['student_class'] = i.class_field
        assignment_data.append(assignment_data_dict)

    context = {
        'assignment_data': assignment_data
    }
    return JsonResponse(context)


def assignment_copy(request):
    copy_code = request.GET['copy_code']
    print(copy_code)
    cp_data = AssignmentQuestionRel.objects.select_related('assignment', 'question').filter(assignment_id=copy_code)

    copy_data = []
    for i in cp_data:
        copy_data_dict = dict()
        copy_data_dict['question_id'] = i.question.question_id
        copy_data_dict['assignment_type'] = i.assignment.type
        copy_data_dict['assignment_title'] = i.assignment.assignment_title
        copy_data.append(copy_data_dict)

    context = {
        'copy_data': copy_data
    }
    return JsonResponse(context)


def change_category(request):
    category_option = request.GET['option']
    if category_option == 'select':
        opt_data = Question.objects.all()
    else:
        opt_data = Question.objects.select_related('category').filter(category__category_name=category_option)

    option_data = []
    for i in opt_data:
        option_data_dict = dict()
        option_data_dict['question_id'] = i.question_id
        option_data_dict['question_name'] = i.question_name
        option_data_dict['question_image'] = i.image
        option_data.append(option_data_dict)

    context = {
        'option_data': option_data
    }
    return JsonResponse(context)
