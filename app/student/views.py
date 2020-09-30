from builtins import dict

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import q as q
from django.db.models import Q
import datetime
import json
from itertools import chain
import requests

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


# 좋은 설명 view 함수
def good_explain(request):
    context = {}
    return render(request, "student/good_explain.html", context)


# 평가연습 view 함수
def evaluate_exercise(request):
    question = Question.objects.filter(upload_check=1)
    category = Category.objects.all()

    context = {"question": question, "category": category}
    return render(request, "student/evaluate_exercise.html", context)


# 평가연습 문항 페이지 view 함수
def evaluate_exercise_question(request):
    question_id = int(request.GET["question_id"])
    question_data = Question.objects.filter(question_id=question_id).first()
    context = {"question_data": question_data}
    return render(request, "student/evaluate_exercise_question.html", context)


# 평가연습 피드백 페이지 view 함수
def evaluate_exercise_diagnosis(request):
    question_id = request.GET["question_id"]
    question_answer = request.GET["question_answer"]

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    # 학교,성별 이미지 출력
    request_school = request.GET.get("category_school")
    request_gender = request.GET.get("category_gender")

    if (request_school != None) and (request_gender != None):
        school = f"/staticfiles/student/school_gender_img/{request_school}.png"
        gender = f"/staticfiles/student/school_gender_img/{request_gender}.png"
    else:
        question_data = Question.objects.filter(question_id=question_id).first()
        context = {"question_data": question_data}
        return render(request, "student/evaluate_exercise_question.html", context)

    data = Question.objects.filter(question_id=question_id).first()

    # 문장 점수와 개념 점수 채점 api
    model_type = "ML" if data.ml_model_check == 1 else "SA"
    sentence_url = "http://sentence-analysis:5252/get-sentence-score"
    if not question_answer.strip():
        question_answer = 'NULL'
    sentence_input = {"sentence": question_answer}
    sentence = requests.post(sentence_url, data=sentence_input)
    sentence_score = json.loads(sentence.text)["data"]["score"]
    concept_url = requests.get(
        "http://scoring-api:5000/"
        + model_type
        + "?question_id="
        + question_id
        + "&answer="
        + question_answer
    )
    concept_score = json.loads(concept_url.text)["score"]
    print(sentence_score, concept_score)

    # 결과보기 안내문
    if 0 <= sentence_score < 0.046:
        standard_answer = "핵심어를 사용하여 완결된 문장으로 답안을 잘 작성해 보세요."
    elif 0.046 <= sentence_score < 0.08:
        standard_answer = (
            "잘 작성했어요. 혹시 주어, 서술어, 목적어 등 문장의 주요 성분이 빠진 것은 없는지 다시 한 번 점검해 보세요."
        )
    else:
        standard_answer = "좋은 문장으로 정말 잘 작성했어요."

    # 로고 안내문
    if concept_score == 1:
        concept_text = "참 잘 설명했어요!"
        logo_img = "student/image/logo2.png"
    else:
        concept_text = "다시 한번 설명해볼까요?"
        logo_img = "mainpage/image/logo.png"

    context = {
        "data": data,
        "question_answer": question_answer,
        "school": school,
        "gender": gender,
        "logo_img": logo_img,
        "concept_text": concept_text,
        "standard_answer": standard_answer,
    }

    # 나의 답 DB에 저장
    if question_answer != "":
        study_solve_data = StudySolveData(
            question_id=question_id,
            school=request_school,
            gender=request_gender,
            response=question_answer,
            sentence_score=sentence_score,
            answer_score=concept_score,
            submit_date=now_date,
        )
        study_solve_data.save()
    else:
        study_solve_data = None

    return render(request, "student/evaluate_exercise_diagnosis.html", context)


# 학습평가 코드 입력 페이지 view 함수
def study_evaluate(request):
    context = {}
    return render(request, "student/study_evaluate.html", context)


# 학습평가 문항 페이지 view 함수
def study_evaluate_question(request):
    # study 페이지에서 숙제 코드 가져오기
    assignment_id = request.POST.get("code_num")
    student_id = request.POST.get("ID_num")
    student_name = request.POST.get("student_name")

    join_by_assignment_id = (
        AssignmentQuestionRel.objects.select_related("question")
        .filter(assignment_id=assignment_id)
        .filter(assignment__type="학습평가")
    )
    first_data=join_by_assignment_id.first()
    # DB에 입력한 코드가 있는지 확인
    if is_in_db(first_data, student_id, student_name):
        context = {}
        return render(request, "student/study_evaluate.html", context)

    # id로 문항 불러오기
    question_info = request.POST.get("question_id")

    # 학습목록을 선택하지 않은 경우
    if question_info is None:
        question_info = str(join_by_assignment_id.first().question_id)+','+assignment_id

    question_info = question_info.split(",")

    join_by_assignment_id = get_question_by_id(question_info)[0]
    first_data = get_question_by_id(question_info)[1]
    assignment_question_id = get_question_by_id(question_info)[2]

    # 학습 완료 목록
    done_list = is_completed(join_by_assignment_id, student_id, student_name)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    solve_data = Solve.objects.filter(as_qurel_id=assignment_question_id, student_id=student_id, student_name=student_name)
    
    # 나의 답 DB에 저장
    try:
        if request.POST["question_answer"] != "" and solve_data.values_list().count()==0:
            solve_data = Solve(
                as_qurel_id=assignment_question_id,
                student_id=student_id,
                submit_date=now_date,
                response=request.POST["question_answer"],
                sentence_score=INIT_SCORE,
                answer_score=INIT_SCORE,
                student_name=student_name,
            )
            solve_data.save()
            done_list = is_completed(join_by_assignment_id, student_id, student_name)
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


# 숙제하기와 숙제조회 선택 페이지 view 함수
def select_homework(request):
    context = {}
    return render(request, "student/select_homework.html", context)


# 숙제조회 id 입력 페이지 view 함수
def check_homework_by_id(request):
    context = {}
    return render(request, "student/check_homework_by_id.html", context)


# 숙제조회 과거 숙제 리스트 출력 페이지 (숙제조회 > 숙제리스트) view 함수
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
        assignment_question_id = join_by_assignment_id.values("as_qurel_id")[0][
            "as_qurel_id"
        ]
        join_assignment = AssignmentQuestionRel.objects.prefetch_related(
            "assignment"
        ).filter(as_qurel_id=assignment_question_id)

    context = {"join_assignment": join_assignment, "student_id": student_id}

    return render(request, "student/check_homework_list.html", context)


# 숙제조회 > 숙제리스트 > 숙제 문항 페이지 view 함수
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
    for assignment_question_id in join_by_assignment_id:
        if assignment_question_id in join_by_student_id:
            values_with_question = (
                Question.objects.select_related("assignment_question_rel")
                .filter(assignmentquestionrel=assignment_question_id)
                .values("assignmentquestionrel", "question_id", "question_name")
            )
            values_with_solve = (
                Solve.objects.select_related("assignment_question_rel")
                .filter(as_qurel_id=assignment_question_id,student_id=student_id)
                .values(
                    "as_qurel_id", "solve_id", "submit_date", "answer_score", "student_name"
                )
                .order_by('-submit_date','-answer_score')
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


# 숙제하기 코드입력 페이지 view 함수
def do_homework_by_code(request):
    context = {}
    return render(request, "student/do_homework_by_code.html", context)


# 숙제하기 문항 페이지 view 함수
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

    done_list = is_completed_homework(join_by_assignment_id, student_id)

    context = {
        "student_id": student_id,
        "join_by_assignment_id": join_by_assignment_id,
        "first_data": first_data,
        "done_list": done_list,
        "student_name": student_name,
    }
    return render(request, "student/do_homework_question.html", context)


# 숙제하기 문항 피드백 페이지 view 함수
def do_homework_diagnosis(request):
    question_id = request.GET["question_id"]
    question_answer = request.GET["question_answer"]
    student_id = request.GET["student_id"]
    student_name = request.GET["student_name"]

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    join_by_question_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(question__question_id=question_id)
    data = join_by_question_id.first()
    assignment_question_id = data.as_qurel_id

    # 문장 점수와 개념 점수 채점 api
    model_type = "ML" if data.question.ml_model_check == 1 else "SA"
    sentence_url = "http://sentence-analysis:5252/get-sentence-score"
    if not question_answer.strip():
        question_answer = 'NULL'
    sentence_input = {"sentence": question_answer}
    sentence = requests.post(sentence_url, data=sentence_input)
    sentence_score = json.loads(sentence.text)["data"]["score"]
    concept_url = requests.get(
        "http://scoring-api:5000/"
        + model_type
        + "?question_id="
        + question_id
        + "&answer="
        + question_answer
    )
    concept_score = json.loads(concept_url.text)["score"]

    # 결과보기 안내문
    if 0 <= sentence_score < 0.046:
        standard_answer = "핵심어를 사용하여 완결된 문장으로 답안을 잘 작성해 보세요."
    elif 0.046 <= sentence_score < 0.08:
        standard_answer = (
            "잘 작성했어요. 혹시 주어, 서술어, 목적어 등 문장의 주요 성분이 빠진 것은 없는지 다시 한 번 점검해 보세요."
        )
    else:
        standard_answer = "좋은 문장으로 정말 잘 작성했어요."

    # 로고 안내문
    if concept_score == 1:
        concept_text = "참 잘 설명했어요!"
        logo_img = "student/image/logo2.png"
    else:
        concept_text = "다시 한번 설명해볼까요?"
        logo_img = "mainpage/image/logo.png"

    context = {
        "student_id": student_id,
        "question_answer": question_answer,
        "data": data,
        "student_name": student_name,
        "logo_img": logo_img,
        "concept_text": concept_text,
        "standard_answer": standard_answer,
    }

    # 나의 답 DB에 저장
    if question_answer != "":
        solve_data = Solve(
            as_qurel_id=assignment_question_id,
            student_id=student_id,
            submit_date=now_date,
            response=question_answer,
            sentence_score=sentence_score,
            answer_score=concept_score,
            student_name=student_name,
        )
        solve_data.save()
    else:
        solve_data = None

    return render(request, "student/do_homework_diagnosis.html", context)


# 스스로 평가하기 페이지 view 함수
def evaluate_by_self(request):
    make_question = MakeQuestion.objects.filter(upload_check=1)

    context = {
        "make_question": make_question,
    }
    return render(request, "student/evaluate_by_self.html", context)


# 스스로 평가하기 문항 페이지 view 함수
def evaluate_by_self_question(request):
    make_question_id = int(request.GET["make_question_id"])
    data = MakeQuestion.objects.filter(make_question_id=make_question_id)[0]

    context = {"data": data}
    return render(request, "student/evaluate_by_self_question.html", context)


# 스스로 평가하기 문항 피드백 및 자가채점 계산 페이지 view 함수
def evaluate_by_self_diagnosis(request):
    make_question_id = int(request.GET["question"])
    question_answer = request.GET["question_answer"]

    # 채점 준거 출력
    mark = Mark.objects.select_related("make_question").filter(
        make_question_id=make_question_id
    )
    data = mark.first()

    # '만족했어요' 체크 리스트
    score_list = request.GET.getlist("score")

    context = {
        "data": data,
        "question_answer": question_answer,
        "mark": mark,
        "score_list": score_list,
    }
    return render(request, "student/evaluate_by_self_diagnosis.html", context)


# 스스로 평가하기 자가채점 결과 페이지 view 함수
def evaluate_by_self_score(request):
    make_question_id = request.GET["question_id"]
    question_answer = request.GET["question_answer"]
    score_list = request.GET.getlist("score")

    # 점수 합산
    sum_score = 0
    for i in score_list:
        sum_score += int(i)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")

    context = {"sum_score": sum_score}

    # 나의 답 DB에 저장
    try:
        self_solve_data = SelfSolveData(
            make_question_id=make_question_id,
            response=question_answer,
            score=sum_score,
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


# 학생 ID가 DB에 존재하는지 확인 함수
def is_student_id(student_id):
    # 학생 ID를 숫자로 받았는지 판별
    if not student_id.isdigit():
        return ""
    result = (
        Solve.objects.select_related("as_qurel")
        .filter(student_id=student_id)
        .values("student_id")
        .first()
    )
    # 학생 ID가 DB에 없는 경우
    if result is None:
        return ""
    # 학생 ID가 DB에 있는 경우
    else:
        return student_id


# 코드가 db에 있는지 없는지 판단, 학번,이름 기입 여부 함수
def is_in_db(first_data, student_id, student_name):
    return (first_data == None) or (student_id == "") or (student_name == "")


# 문항 학습 완료여부 판단 함수 - 학습평가
def is_completed(join_by_assignment_id,student_id,student_name):
    result_list = []
    done_list = []

    for join_data in join_by_assignment_id:
        assignment_question_id = join_data.as_qurel_id
        solve_data = Solve.objects.filter(as_qurel_id=assignment_question_id, student_id=student_id, student_name=student_name)
        result_list.append(solve_data)
    for result_data in result_list:
        if result_data.values("as_qurel_id"):
            done = "O"
        else:
            done = "X"
        done_list.append(done)
    return done_list


# 문항 학습 완료여부 판단 함수 - 숙제하기
def is_completed_homework(join_by_assignment_id,student_id):
    result_list = []
    done_list = []

    for join_data in join_by_assignment_id:
        assignment_question_id = join_data.as_qurel_id
        solve_data = Solve.objects.filter(as_qurel_id=assignment_question_id, student_id=student_id, answer_score=1.00)
        result_list.append(solve_data)
    for result_data in result_list:
        if result_data.values("as_qurel_id"):
            done = "O"
        else:
            done = "X"
        done_list.append(done)
    return done_list


# id로 문항 불러오기 함수
def get_question_by_id(question_info):
    question_id = int(question_info[0])
    assignment_id = question_info[1]

    join_by_assignment_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(assignment_id=assignment_id)
    join_by_question_id = AssignmentQuestionRel.objects.select_related(
        "question"
    ).filter(question__question_id=question_id)
    join_by_assignment_id_question_id = (
        AssignmentQuestionRel.objects.select_related("question")
        .filter(question__question_id=question_id, assignment_id=assignment_id)
        .values("as_qurel_id")[0]["as_qurel_id"]
    )
    first_data = join_by_question_id[0]
    return join_by_assignment_id, first_data, join_by_assignment_id_question_id


# 평가연습의 문항 검색하기 함수
def search_keyword(request):
    user_input = request.GET["user_input"]

    # 키워드로 검색
    key_data = (
        Keyword.objects.select_related("question")
        .filter(keyword_name__icontains=user_input, question__upload_check=1)
        .values_list("question_id", flat=True)
        .distinct()
    )

    # 문항명으로 검색
    name_data = (
        Question.objects.filter(question_name__icontains=user_input, upload_check=1)
        .values_list("question_id", flat=True)
        .distinct()
    )

    # 키워드와 문항명 검색 결과
    result = list(chain(key_data, name_data))

    keys_of_question = Question.objects.filter(pk__in=result)

    search_data = search_card_result(keys_of_question)

    context = {"search_data": search_data}
    return JsonResponse(context)


# 스스로 평가하기의 문항명으로 문항 검색하기 함수
def search_name(request):
    name_input = request.GET["name_input"]
    name_data = (
        MakeQuestion.objects.filter(question_name__icontains=name_input, upload_check=1)
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


# 평가연습의 카테고리 선택 함수
def change_category_evaluate_exercise(request):
    category_option = request.GET["option"]

    if category_option == "select":
        options_of_question = Question.objects.filter(upload_check=1)
    else:
        options_of_question = Question.objects.select_related("category").filter(
            category__category_name=category_option, upload_check=1
        )

    option_data = search_card_result(options_of_question)

    context = {"option_data": option_data}
    return JsonResponse(context)


# 검색 결과 반환 함수
def search_card_result(data):
    list_data = []
    for result in data:
        data_dict = dict()
        data_dict["question_id"] = result.question_id
        data_dict["question_name"] = result.question_name
        data_dict["question_image"] = result.image.name
        list_data.append(data_dict)
    return list_data
