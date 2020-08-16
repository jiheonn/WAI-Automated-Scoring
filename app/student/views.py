from builtins import dict

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import q as q
from django.db.models import Q
import datetime
import json
from itertools import chain

from mainpage.models import Question
from mainpage.models import SelfSolveData
from mainpage.models import AssignmentQuestionRel
from mainpage.models import Keyword
from mainpage.models import Solve
from mainpage.models import Assignment
from mainpage.models import MakeQuestion
from mainpage.models import Category
from mainpage.models import StudySolveData
from mainpage.models import Mark
from mainpage.models import Notice

INIT_SCORE = 0


# 좋은 설명
def good_explain(request):
    context = {}
    return render(request, "student/good_explain.html", context)


# 평가연습
def evaluate_exercise(request):
    question = Question.objects.all()
    category = Category.objects.all()

    context = {"question": question, "category": category}
    return render(request, "student/evaluate_exercise.html", context)


# 평가연습 문항 페이지
def evaluate_exercise_question(request):
    question_id = int(request.GET["question_id"])
    question_data = Question.objects.filter(question_id=question_id).first()
    context = {"question_data": question_data}
    return render(request, "student/evaluate_exercise_question.html", context)


# 평가연습 피드백 페이지
def evaluate_exercise_diagnosis(request):
    question_id = request.GET["question_id"]
    question_answer = request.GET["question_answer"]

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    # 학교,성별 이미지 출력
    request_school = request.GET.get("category_school")
    request_gender = request.GET.get("category_gender")

    if (request_school != "") and (request_gender != ""):
        school = f"/staticfiles/student/school_gender_img/{request_school}.png"
        gender = f"/staticfiles/student/school_gender_img/{request_gender}.png"
    else:
        school = ""
        gender = ""

    join_by_question_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(question__question_id=question_id)
    data = join_by_question_id.first()

    context = {
        "data": data,
        "question_answer": question_answer,
        "school": school,
        "gender": gender,
    }

    # 나의 답 DB에 저장
    try:
        study_solve_data = StudySolveData(
            question_id=question_id,
            school=request_school,
            gender=request_gender,
            response=question_answer,
            score=INIT_SCORE,
            submit_date=now_date,
        )
        study_solve_data.save()

    except:
        study_solve_data = None

    return render(request, "student/evaluate_exercise_diagnosis.html", context)


# 학습평가 코드 입력 페이지
def study_evaluate(request):
    context = {}
    return render(request, "student/study_evaluate.html", context)


# 학습평가 문항 페이지
def study_evaluate_question(request):
    # study 페이지에서 숙제 코드 가져오기
    assignment_id = request.GET.get("code_num")
    student_id = request.GET.get("ID_num")
    student_name = request.GET.get("student_name")

    join_by_assignment_id = (
        AssignmentQuestionRel.objects.select_related("question")
        .filter(assignment_id=assignment_id)
        .filter(assignment__type="학습평가")
    )

    # id로 문항 불러오기
    question_info = request.GET.get("question_id")

    # 학습목록을 선택한 경우
    if question_info is not None:
        question_info = question_info.split(",")
        join_by_assignment_id = get_question_by_id(question_info)[0]
        first_data = get_question_by_id(question_info)[1]
        assignment_question_id = get_question_by_id(question_info)[2]
    # 학습목록을 선택하지 않은 경우
    else:
        first_data = join_by_assignment_id.first()

    # 코드가 db에 없으면 원상복귀
    if is_in_db(first_data, student_id, student_name):
        context = {}
        return render(request, "student/study_evaluate.html", context)

    assignment_question_id = first_data.as_qurel_id

    # 학습 완료 목록
    done_list = is_completed(join_by_assignment_id)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    # 나의 답 DB에 저장
    try:
        if request.GET["question_answer"] != "":
            solve_data = Solve(
                as_qurel_id=assignment_question_id,
                student_id=student_id,
                submit_date=now_date,
                response=request.GET["question_answer"],
                score=INIT_SCORE,
                student_name=student_name,
            )
            solve_data.save()
    except:
        solve_data = None

    context = {
        "student_id": student_id,
        "student_name": student_name,
        "join_by_assignment_id": join_by_assignment_id,
        "first_data": first_data,
        "done_list": done_list,
    }
    return render(request, "student/study_evaluate_question.html", context)


# 코드가 db에 있는지 없는지 판단, 학번,이름 기입 여부
def is_in_db(first_data, student_id, student_name):
    return (first_data == None) or (student_id == "") or (student_name == "")


# 문항 학습 완료여부 판단
def is_completed(join_by_assignment_id):
    test_list = []
    done_list = []

    for join_data in join_by_assignment_id:
        as_qurel_id = join_data.as_qurel_id
        solve_data = Solve.objects.filter(as_qurel_id=as_qurel_id)
        test_list.append(solve_data)
    for test_data in test_list:
        if test_data.values("as_qurel_id"):
            done = "O"
        else:
            done = "X"
        done_list.append(done)
    return done_list


# id로 문항 불러오기
def get_question_by_id(question_info):
    question_id = int(question_info[0])
    assignment_id = question_info[1]

    join_by_assignment_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(assignment_id=assignment_id)
    join_by_question_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(question__question_id=question_id)
    as_qurel_id = (
        AssignmentQuestionRel.objects.select_related("question")
        .filter(question__question_id=question_id, assignment_id=assignment_id)
        .values("as_qurel_id")[0]["as_qurel_id"]
    )
    first_data = join_by_question_id[0]
    return join_by_assignment_id, first_data, as_qurel_id


# 숙제하기와 숙제조회 선택 페이지
def select_homework(request):
    context = {}
    return render(request, "student/select_homework.html", context)


# 숙제조회 id 입력 페이지
def check_homework_by_id(request):
    context = {}
    return render(request, "student/check_homework_by_id.html", context)


# 숙제조회 과거 숙제 리스트 출력 페이지 (숙제조회 > 숙제리스트)
def check_homework_list(request):
    student_id = request.GET["ID_num"]

    # 학생 ID가 아무것도 입력되지 않음
    if student_id is "":
        context = {}
        return render(request, "student/check_homework_by_id.html", context)
    # 학생 ID가 DB에 존재하지 않음
    elif is_student_id(student_id) is "":
        result_id = is_student_id(student_id)
        if is_in_db(1, result_id, 1):
            context = {}
            return render(request, "student/check_homework_by_id.html", context)
    # 입력된 학생 ID가 DB에 존재하여 숙제 리스트 출력
    else:
        join_by_assignment_id = (
            Solve.objects.select_related("as_qurel")
            .filter(student_id=student_id)
            .values("as_qurel_id", "solve_id")
        )
        as_qurel_id = join_by_assignment_id.values("as_qurel_id")[0]["as_qurel_id"]
        join_assignment = AssignmentQuestionRel.objects.prefetch_related(
            "assignment"
        ).filter(as_qurel_id=as_qurel_id)

    context = {"join_assignment": join_assignment, "student_id": student_id}

    return render(request, "student/check_homework_list.html", context)


# 학생 ID가 DB에 존재하는지 확인
def is_student_id(student_id):
    result = (
        Solve.objects.select_related("as_qurel")
        .filter(student_id=student_id)
        .values("student_id")
        .first()
    )
    if result is None:
        return ""
    else:
        return student_id


# 숙제조회 > 숙제리스트 > 숙제 문항 페이지
def check_homework_question(request):
    student_id = int(request.GET.get("student_id"))
    assignment_id = request.GET.get("assignment_id")

    join_by_assignment_id = (
        Question.objects.select_related("assignment_question_rel")
        .filter(assignmentquestionrel__assignment_id=assignment_id)
        .values_list("assignmentquestionrel", flat=True)
    )
    join_by_student_id = (
        Solve.objects.select_related("assignment_question_rel")
        .filter(student_id=student_id)
        .values_list("as_qurel_id", flat=True)
    )

    result_list = []
    for as_qurel_id in join_by_assignment_id:
        if as_qurel_id in join_by_student_id:
            values_with_question = (
                Question.objects.select_related("assignment_question_rel")
                .filter(assignmentquestionrel=as_qurel_id)
                .values("assignmentquestionrel", "question_id", "question_name")
            )
            values_with_solve = (
                Solve.objects.select_related("assignment_question_rel")
                .filter(as_qurel_id=as_qurel_id)
                .values(
                    "as_qurel_id", "solve_id", "submit_date", "score", "student_name"
                )
            )
            result = list(chain(values_with_question, values_with_solve))

            result[0].update(result[1])
            result_list.append(result[0])

    context = {
        "result_list": result_list,
        "assignment_id": assignment_id,
        "student_id": student_id,
    }
    return render(request, "student/check_homework_question.html", context)


# 숙제하기 코드입력 페이지
def do_homework_by_code(request):
    context = {}
    return render(request, "student/do_homework_by_code.html", context)


# 숙제하기 문항 페이지
def do_homework_question(request):
    # Homeworkques 페이지에서 숙제 코드 가져오기
    assignment_id = request.GET["code_num"]
    student_id = request.GET["ID_num"]
    student_name = request.GET["student_name"]

    join_by_assignment_id = (
        AssignmentQuestionRel.objects.select_related("question")
        .filter(assignment_id=assignment_id)
        .filter(assignment__type="숙제하기")
    )

    # id로 문항 불러오기
    question_info = request.GET.get("question_id")

    # 학습목록을 선택한 경우
    if question_info is not None:
        question_info = question_info.split(",")
        join_by_assignment_id = get_question_by_id(question_info)[0]
        first_data = get_question_by_id(question_info)[1]
    # 학습목록을 선택하지 않은 경우
    else:
        first_data = join_by_assignment_id.first()

    # 코드가 db에 없으면 원상복귀
    if is_in_db(first_data, student_id, student_name):
        context = {}
        return render(request, "student/do_homework_by_code.html", context)

    done_list = is_completed(join_by_assignment_id)

    context = {
        "student_id": student_id,
        "join_by_assignment_id": join_by_assignment_id,
        "first_data": first_data,
        "done_list": done_list,
        "student_name": student_name,
    }
    return render(request, "student/do_homework_question.html", context)


# 숙제하기 문항 피드백 페이지
def do_homework_diagnosis(request):
    question_id = request.GET["question_id"]
    ques_ans = request.GET["ques_ans"]
    student_id = request.GET["student_id"]
    student_name = request.GET["student_name"]

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    join_by_question_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(question__question_id=question_id)
    data = join_by_question_id.first()
    as_qurel_id = data.as_qurel_id

    context = {
        "student_id": student_id,
        "ques_ans": ques_ans,
        "data": data,
        "student_name": student_name,
    }

    # 나의 답 DB에 저장
    if ques_ans != "":
        solve_data = Solve(
            as_qurel_id=as_qurel_id,
            student_id=student_id,
            submit_date=now_date,
            response=ques_ans,
            score=INIT_SCORE,
            student_name=student_name,
        )
        solve_data.save()
    else:
        solve_data = None

    return render(request, "student/do_homework_diagnosis.html", context)


# 스스로 평가하기 페이지
def evaluate_by_self(request):
    qs = MakeQuestion.objects.all()

    context = {
        "qs": qs,
    }
    return render(request, "student/evaluate_by_self.html", context)


# 스스로 평가하기 문항 페이지
def evaluate_by_self_question(request):
    make_question_id = int(request.GET["make_question_id"])
    data = MakeQuestion.objects.filter(make_question_id=make_question_id)[0]

    context = {"data": data}
    return render(request, "student/evaluate_by_self_question.html", context)


# 스스로 평가하기 문항 피드백 및 자가채점 계산 페이지
def evaluate_by_self_diagnosis(request):
    make_question_id = int(request.GET["question"])
    ques_ans = request.GET["ques_ans"]

    # 채점 준거 출력
    mark = Mark.objects.select_related("make_question").filter(
        make_question_id=make_question_id
    )
    data = mark.first()

    # '만족했어요' 체크 리스트
    score_list = request.GET.getlist("score")

    context = {
        "data": data,
        "ques_ans": ques_ans,
        "mark": mark,
        "score_list": score_list,
    }
    return render(request, "student/evaluate_by_self_diagnosis.html", context)


# 스스로 평가하기 자가채점 결과 페이지
def evaluate_by_self_score(request):
    make_question_id = request.GET["question_id"]
    ques_ans = request.GET["ques_ans"]
    score_list = request.GET.getlist("score")

    # 점수 합산
    sum_s = 0
    for i in score_list:
        sum_s += int(i)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    context = {"sum_s": sum_s}

    # 나의 답 DB에 저장
    try:
        self_solve_data = SelfSolveData(
            make_question_id=make_question_id,
            response=ques_ans,
            score=sum_s,
            submit_date=now_date,
        )
        self_solve_data.save()

    except:
        self_solve_data = None

    return render(request, "student/evaluate_by_self_score.html", context)


# 공지사항 화면 view 함수
def student_notice(request):
    all_notice = Notice.objects.exclude(notice_target="선생님")
    context = {"notice": all_notice}
    return render(request, "student/student_notice.html", context)


# 공지사항 자세히보기 화면 view 함수
def student_notice_detail(request):
    notice_id = request.GET["selected_notice_id"]
    notice = Notice.objects.filter(notice_id=notice_id).first()
    context = {"notice": notice}
    return render(request, "student/student_notice_detail.html", context)


# 평가연습의 키워드로 문항 검색하기
def search_keyword(request):
    user_input = request.GET["user_input"]
    key_data = (
        Keyword.objects.select_related("question")
        .filter(keyword_name__icontains=user_input)
        .values_list("question_id", flat=True)
        .distinct()
    )
    keys_of_question = Question.objects.filter(pk__in=key_data)

    search_data = search_card_result(keys_of_question)

    context = {"search_data": search_data}
    return JsonResponse(context)


# 스스로 평가하기의 문항명으로 문항 검색하기
def search_name(request):
    name_input = request.GET["name_input"]
    name_data = (
        MakeQuestion.objects.filter(question_name__icontains=name_input)
        .values_list("make_question_id", flat=True)
        .distinct()
    )
    names_of_makequestion = MakeQuestion.objects.filter(pk__in=name_data)

    search_data = []
    for name in names_of_makequestion:
        search_data_dict = dict()
        search_data_dict["make_question_id"] = name.make_question_id
        search_data_dict["question_name"] = name.question_name
        search_data_dict["question_image"] = name.image.name
        search_data.append(search_data_dict)

    context = {"search_data": search_data}
    return JsonResponse(context)


# 평가연습의 카테고리 선택
def change_category_evaluate_exercise(request):
    category_option = request.GET["option"]

    if category_option == "select":
        options_of_question = Question.objects.all()
    else:
        options_of_question = Question.objects.select_related("category").filter(
            category__category_name=category_option
        )

    option_data = search_card_result(options_of_question)

    context = {"option_data": option_data}
    return JsonResponse(context)


# 검색 결과 반환
def search_card_result(datas):
    list_data = []
    for data in datas:
        data_dict = dict()
        data_dict["question_id"] = data.question_id
        data_dict["question_name"] = data.question_name
        data_dict["question_image"] = data.image.name
        list_data.append(data_dict)
    return list_data
