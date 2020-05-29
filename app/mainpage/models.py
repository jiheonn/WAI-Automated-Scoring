from django.db import models

# Create your models here.
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True, auto_created=True)
    teacher_name = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    approve = models.IntegerField()

class Assignment(models.Model):
    assignment_id = models.CharField(primary_key=True, max_length=50)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    assignment_title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    made_date = models.DateField()
    grade = models.IntegerField()
    school_class = models.IntegerField()

class MakeQuestion(models.Model):
    make_question_id = models.AutoField(primary_key=True, auto_created=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    question_name = models.CharField(max_length=200)
    discription = models.TextField()
    answer = models.TextField()
    image = models.CharField(max_length=200)
    hint = models.TextField()
    made_date = models.DateField()
    upload_check = models.IntegerField()

class SelfSolveData(models.Model):
    self_id = models.AutoField(primary_key=True, auto_created=True)
    make_question = models.ForeignKey(MakeQuestion, models.DO_NOTHING)
    response = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    submit_date = models.DateField()

class Mark(models.Model):
    mark_id = models.AutoField(primary_key=True, auto_created=True)
    make_question = models.ForeignKey(MakeQuestion, models.DO_NOTHING)
    mark_text = models.TextField()

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, auto_created=True)
    category_name = models.CharField(max_length=50)

class Question(models.Model):
    question_id = models.AutoField(primary_key=True, auto_created=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    model_id = models.CharField(max_length=50)
    question_name = models.CharField(max_length=100)
    discription = models.TextField()
    answer = models.TextField()
    image = models.CharField(max_length=200)
    hint = models.TextField()
    made_date = models.DateField()
    qr_code = models.CharField(max_length=100)  # Field name made lowercase.
    ques_concept = models.CharField(max_length=255)

class StudySolveData(models.Model):
    study_id = models.AutoField(primary_key=True, auto_created=True)
    question = models.ForeignKey(Question, models.DO_NOTHING)
    school = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    response = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    submit_date = models.DateField()

class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True, auto_created=True)
    question = models.ForeignKey('Question', models.DO_NOTHING)
    keyword_name = models.CharField(max_length=50)

class AssignmentQuestionRel(models.Model):
    as_qurel_id = models.AutoField(primary_key=True, auto_created=True)
    assignment = models.ForeignKey(Assignment, models.DO_NOTHING)
    question = models.ForeignKey('Question', models.DO_NOTHING)

class Solve(models.Model):
    solve_id = models.AutoField(primary_key=True, auto_created=True)
    as_qurel = models.ForeignKey(AssignmentQuestionRel, models.DO_NOTHING)
    student_id = models.IntegerField()
    submit_date = models.DateField()
    response = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    student_name = models.CharField(max_length=50)