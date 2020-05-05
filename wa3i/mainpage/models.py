# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Assignment(models.Model):
    assignment_id = models.CharField(primary_key=True, max_length=50)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING, blank=True, null=True)
    assignment_title = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    made_date = models.DateField(blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    class_field = models.IntegerField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'assignment'


class AssignmentQuestionRel(models.Model):
    as_qurel_id = models.IntegerField(primary_key=True)
    assignment = models.ForeignKey(Assignment, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assignment_question_rel'


class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class CategoryQuestionRel(models.Model):
    cate_qurel_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_question_rel'


class Keyword(models.Model):
    keyword_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)
    keyword_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keyword'


class MakeQuestion(models.Model):
    make_question_id = models.IntegerField(primary_key=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING, blank=True, null=True)
    question_name = models.CharField(max_length=50, blank=True, null=True)
    discription = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    hint = models.CharField(max_length=200, blank=True, null=True)
    ques_concept = models.CharField(max_length=255, blank=True, null=True)
    check = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'make_question'


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    model_id = models.CharField(max_length=50, blank=True, null=True)
    question_name = models.CharField(max_length=50, blank=True, null=True)
    discription = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=50, blank=True, null=True)
    hint = models.CharField(max_length=200, blank=True, null=True)
    made_date = models.DateField(blank=True, null=True)
    qr_code = models.CharField(db_column='QR_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ques_concept = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question'


class SelfSolveData(models.Model):
    self_id = models.IntegerField(primary_key=True)
    make_question = models.ForeignKey(MakeQuestion, models.DO_NOTHING, blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    submit_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'self_solve_data'


class Solve(models.Model):
    solve_id = models.IntegerField(primary_key=True)
    student_id = models.IntegerField(blank=True, null=True)
    assignment = models.ForeignKey(AssignmentQuestionRel, models.DO_NOTHING, blank=True, null=True)
    modified_date = models.DateField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    student_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solve'


class StudySolveData(models.Model):
    study_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(Question, models.DO_NOTHING, blank=True, null=True)
    school = models.CharField(max_length=30, blank=True, null=True)
    sex = models.CharField(max_length=30, blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    submit_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'study_solve_data'


class Teacher(models.Model):
    teacher_id = models.IntegerField(primary_key=True)
    teacher_name = models.CharField(max_length=50, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    approve = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher'
