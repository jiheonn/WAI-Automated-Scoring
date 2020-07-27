from builtins import dict

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import q as q
from django.db.models import Q
import datetime
import json

# TODO : import 세분화하
from mainpage.models import Question, SelfSolveData, AssignmentQuestionRel, Keyword, Solve, Assignment, MakeQuestion, \
    Category, StudySolveData, Mark

INIT_SCORE = 0


# TODO : 함수명 구체적으로 바꾸기
# 좋은 설명
def good_ex(request):
    context = {
    }
    return render(request, 'student/index.html', context)


# 평가연습
def evaluate_exercise(request):
    qs = Question.objects.all()
    category = Category.objects.all()

    context = {
        'qs': qs,
        'category': category
    }
    return render(request, 'student/evaluate_exercise.html', context)


# 평가연습 문항 페이지
def evaluate_exercise_question(request):
    question_id = int(request.GET['question_id'])
    data = Question.objects.filter(question_id=question_id).first()
    context = {
        'data': data
    }
    return render(request, 'student/evaluate_exercise_question.html', context)


# 평가연습 피드백 페이지
def evaluate_exercise_diagnosis(request):
    question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    # 학교,성별 이미지 출력
    re_school = request.GET.get('category_school')
    re_gender = request.GET.get('category_gender')

    if (re_school != "") and (re_gender != ""):
        school = f'/staticfiles/student/school_gender_img/{re_school}.png'
        gender = f'/staticfiles/student/school_gender_img/{re_gender}.png'
    else:
        school = ""
        gender = ""

    # TODO : 변수명 바꾸기
    join_aqr_q = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    data = join_aqr_q.first()

    context = {
        'data': data,
        'ques_ans': ques_ans,
        'school': school,
        'gender': gender,
    }

    # 나의 답 DB에 저장
    try:
        study_solve_data = StudySolveData(
            question_id=question_id,
            school=re_school,
            gender=re_gender,
            response=ques_ans,
            score=INIT_SCORE,
            submit_date=now_date
        )
        study_solve_data.save()

    except:
        study_solve_data = None

    return render(request, 'student/evaluate_exercise_diagnosis.html', context)


# 학습평가 코드 입력 페이지
def study_evaluate(request):
    context = {
    }
    return render(request, 'student/Study.html', context)


# 학습평가 문항 페이지
def study_evaluate_question(request):
    # study 페이지에서 숙제 코드 가져오기
    assignment_id = request.GET.get('code_num')
    student_id = request.GET.get('ID_num')
    student_name = request.GET.get('student_name')

    join_aqr_q = AssignmentQuestionRel.objects.select_related('question').filter(
        assignment_id=assignment_id).filter(
        assignment__type="학습평가")

    # id로 문항 불러오기
    question_info = request.GET.get('question_id')

    # 학습목록을 선택한 경우
    if question_info is not None:
        question_info = question_info.split(',')
        join_aqr_q = get_question_by_id(question_info)[0]
        first_data = get_question_by_id(question_info)[1]
    # 학습목록을 선택하지 않은 경우
    else:
        first_data = join_aqr_q.first()

    # 코드가 db에 없으면 원상복귀
    if is_in_db(first_data, student_id, student_name):
        context = {
        }
        return render(request, 'student/Study.html', context)

    # 학습 완료 목록
    done_list = is_completed(join_aqr_q)

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    # 나의 답 DB에 저장
    try:
        solve_data = Solve(
            student_id=student_id,
            submit_date=now_date,
            response=request.GET['ques_ans'],
            score=INIT_SCORE,
            as_querl_id=as_qurel_id,
            student_name=student_name
        )
        solve_data.save()

    except:
        solve_data = None

    context = {
        'student_id': student_id,
        'student_name': student_name,
        'join_aqr_q': join_aqr_q,
        'first_data': first_data,
        'done_list': done_list
    }
    return render(request, 'student/Studyques.html', context)

    # data => join_aqr_q
    # f => first_data


# 코드가 db에 있는지 없는지 판단, 학번,이름 기입 여부
def is_in_db(first_data, student_id, student_name):
    return (first_data == None) or (student_id == "") or (student_name == "")


# 문항 학습 완료여부 판단
def is_completed(join_aqr_q):
    test_list = []
    done_list = []

    for join_data in join_aqr_q:
        as_qurel_id = join_data.as_qurel_id
        join_aq_id = Solve.objects.filter(as_qurel_id=as_qurel_id)
        test_list.append(join_aq_id)
    for test_data in test_list:
        if test_data.values('as_qurel_id'):
            done = "O"
        else:
            done = "X"
        done_list.append(done)
    return done_list


# id로 문항 불러오기
def get_question_by_id(question_info):
    question_id = int(question_info[0])
    assignment_id = question_info[1]

    join_aqr_q = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
    join_aqr_q_id = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    first_data = join_aqr_q_id[0]
    return join_aqr_q, first_data


# 숙제하기와 숙제조회 선택 페이지
def homework_do_check_select(request):
    context = {
    }
    return render(request, 'student/Homeworkselect.html', context)


# 숙제조회 id 입력 페이지
def homework_check_id(request):
    context = {
    }
    return render(request, 'student/Homework.html', context)


# 숙제조회 과거 숙제 리스트 출력 페이지 (숙제조회 > 숙제리스트)
def homework_check_list(request):
    # question_info = request.GET['question_name'].split(',')
    # question_name = question_info[0]
    # assignment_id = question_info[1]
    # data = AssignmentQuestionRel.objects.select_related('question').filter(assignment_id=assignment_id)
    # f = AssignmentQuestionRel.objects.select_related('question').filter(question__question_name=question_name)[0]
    student_id = int(request.GET['ID_num'])
    # rel = AssignmentQuestionRel.objects.select_related('assignment', 'solve').filter(solve__student_id=student_id)

    # 테스트
    re = Solve.objects.prefetch_related('assignment_question_rel').filter(student_id=student_id)
    d = re.values('as_qurel_id')[0]['as_qurel_id']
    print(d)
    rel = AssignmentQuestionRel.objects.prefetch_related('assignment').filter(as_qurel_id=d)

    context = {
        'rel': rel,
        # 'da':da,
        're': re
    }
    return render(request, 'student/Homeworklist.html', context)


# 숙제조회 > 숙제리스트 > 숙제 문항 페이지
def homework_check_homework(request):
    student_id = int(request.GET['student_id'])
    # assignment_title = request.GET['assignment_id']
    # print(assignment_title.values())
    # data = AssignmentQuestionRel.objects.select_related('assignment', 'question', 'solve').filter(solve__student_id=student_id)

    # 테스트
    re = Solve.objects.prefetch_related('assignment_question_rel').filter(student_id=student_id)
    d = re.values('as_qurel_id')[0]['as_qurel_id']
    print(d)
    data = AssignmentQuestionRel.objects.prefetch_related('assignment', 'question').filter(as_qurel_id=d)

    context = {
        'data': data
    }
    return render(request, 'student/Homeworkcheck.html', context)


# 숙제하기 코드입력 페이지
def homework_do_code(request):
    context = {
    }
    return render(request, 'student/Homeworkcode.html', context)


# 숙제하기 문항 페이지
def homework_do_question(request):
    # try:
    #     # Homeworkques 페이지에서 숙제 코드 가져오기
    #     assignment_id = request.GET['code_num']
    #     student_id = request.GET['ID_num']
    #     student_name = request.GET['student_name']
    #
    #     join_aqr_q = AssignmentQuestionRel.objects.select_related('question').filter(
    #         assignment_id=assignment_id).filter(
    #         assignment__type="숙제하기")
    #     first_data = join_aqr_q.first()
    #
    #     # 코드가 db에 없으면 원상복귀
    #     if is_in_db(first_data, student_id, student_name):
    #         context = {
    #         }
    #         return render(request, 'student/Homeworkcode.html', context)
    #
    # except:
    #     # id로 문항 불러오기
    #     question_info = request.GET.get('question_id').split(',')
    #
    #     join_aqr_q = get_question_by_id(question_info)[0]
    #     first_data = get_question_by_id(question_info)[1]

    # Homeworkques 페이지에서 숙제 코드 가져오기
    assignment_id = request.GET['code_num']
    student_id = request.GET['ID_num']
    student_name = request.GET['student_name']

    join_aqr_q = AssignmentQuestionRel.objects.select_related('question').filter(
        assignment_id=assignment_id).filter(
        assignment__type="숙제하기")

    # id로 문항 불러오기
    question_info = request.GET.get('question_id')

    # 학습목록을 선택한 경우
    if question_info is not None:
        question_info = question_info.split(',')
        join_aqr_q = get_question_by_id(question_info)[0]
        first_data = get_question_by_id(question_info)[1]
    # 학습목록을 선택하지 않은 경우
    else:
        first_data = join_aqr_q.first()

    # 코드가 db에 없으면 원상복귀
    if is_in_db(first_data, student_id, student_name):
        context = {
        }
        return render(request, 'student/Homeworkcode.html', context)

    done_list = is_completed(join_aqr_q)

    context = {
        'student_id': student_id,
        'join_aqr_q': join_aqr_q,
        'first_data': first_data,
        'done_list': done_list,
        'student_name': student_name
    }
    return render(request, 'student/Homeworkques.html', context)


# 숙제하기 문항 피드백 페이지
def homework_do_diagnosis(request):
    question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']
    student_id = request.GET['student_id']

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    join_aqr_q = AssignmentQuestionRel.objects.select_related('question').filter(question__question_id=question_id)
    data = join_aqr_q.first

    context = {
        'student_id': student_id,
        'ques_ans': ques_ans,
        'data': data,
    }

    # 나의 답 DB에 저장
    try:
        solve_data = Solve(
            student_id=student_id,
            submit_date=now_date,
            response=ques_ans,
            score=INIT_SCORE,
            as_querl_id=as_qurel_id,
            student_name=request.GET['student_name']
        )
        solve_data.save()

    except:
        solve_data = None

    return render(request, 'student/Homeworkdiag.html', context)


# 스스로 평가하기 페이지
def self(request):
    qs = MakeQuestion.objects.all()
    # category = Category.objects.all()

    context = {
        'qs': qs,
        # 'category': category,
    }
    return render(request, 'student/Self.html', context)


# 스스로 평가하기 문항 페이지
def self_question(request):
    make_question_id = int(request.GET['make_question_id'])
    data = MakeQuestion.objects.filter(make_question_id=make_question_id)[0]

    context = {
        'data': data
    }
    return render(request, 'student/Selfques.html', context)


# 스스로 평가하기 문항 피드백 및 자가채점 계산 페이지
def self_diagnosis(request):
    make_question_id = int(request.GET['question'])
    ques_ans = request.GET['ques_ans']

    # 채점 준거 출력
    mark = Mark.objects.select_related('make_question').filter(make_question_id=make_question_id)
    data = mark.first()

    # '만족했어요' 체크 리스트
    score_list = request.GET.getlist('score')

    context = {
        'data': data,
        'ques_ans': ques_ans,
        'mark': mark,
        'score_list': score_list
    }
    return render(request, 'student/Selfdiag.html', context)


# 스스로 평가하기 자가채점 결과 페이지
def self_grade_score(request):
    make_question_id = request.GET['question_id']
    ques_ans = request.GET['ques_ans']
    score_list = request.GET.getlist('score')

    # 점수 합산
    sum_s = 0
    for i in score_list:
        sum_s += int(i)

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    context = {
        'sum_s': sum_s
    }

    # 나의 답 DB에 저장
    try:
        self_solve_data = SelfSolveData(
            make_question_id=make_question_id,
            response=ques_ans,
            score=sum_s,
            submit_date=now_date
        )
        self_solve_data.save()

    except:
        self_solve_data = None

    return render(request, 'student/Selfgrade.html', context)


# 게시판 페이지
def notice(request):
    context = {
    }
    return render(request, 'student/Notice.html', context)


# 평가연습의 키워드로 문항 검색하기
def search_keyword(request):
    user_input = request.GET['user_input']
    key_data = Keyword.objects.select_related('question').filter(keyword_name__icontains=user_input).values_list(
        'question_id', flat=True).distinct()
    k_datas = Question.objects.filter(pk__in=key_data)

    search_data = search_card_result(k_datas)

    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


# 스스로 평가하기의 문항명으로 문항 검색하기
def search_name(request):
    name_input = request.GET['name_input']
    name_data = MakeQuestion.objects.filter(question_name__icontains=name_input).values_list('make_question_id',
                                                                                             flat=True).distinct()
    n_datas = MakeQuestion.objects.filter(pk__in=name_data)

    search_data = []
    for n_data in n_datas:
        search_data_dict = dict()
        search_data_dict['make_question_id'] = n_data.make_question_id
        search_data_dict['question_name'] = n_data.question_name
        search_data_dict['question_image'] = n_data.image.name
        search_data.append(search_data_dict)

    context = {
        'search_data': search_data
    }
    return JsonResponse(context)


# 평가연습의 카테고리 선택
def change_category_ai(request):
    category_option = request.GET['option']

    if category_option == 'select':
        opt_datas = Question.objects.all()
    else:
        opt_datas = Question.objects.select_related('category').filter(category__category_name=category_option)

    option_data = search_card_result(opt_datas)

    context = {
        'option_data': option_data
    }
    return JsonResponse(context)


# 검색 결과 반환
def search_card_result(datas):
    list_data = []
    for data in datas:
        data_dict = dict()
        data_dict['question_id'] = data.question_id
        data_dict['question_name'] = data.question_name
        data_dict['question_image'] = data.image.name
        list_data.append(data_dict)
    return list_data

# def change_category_self(request):
#     category_option = request.GET['option']
#
#     if category_option == 'select':
#         opt_datas = Question.objects.all()
#     else:
#         opt_datas = Question.objects.select_related('category').filter(category__category_name=category_option)
#
#     option_data = search_card_result(opt_datas)
#
#     context = {
#         'option_data': option_data
#     }
#     return JsonResponse(context)

### 테스트
# solve테이블과 question테이블 조인
# as_qurel_id = join_aqr_q.values('as_qurel_id')[0]['as_qurel_id']
# da = Solve.objects.prefetch_related('assignment_question_rel').filter(as_qurel_id=as_qurel_id)