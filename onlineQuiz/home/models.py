from django.db import models

# Create your models here.
# python manage.py migrate --run-syncdb


class Student(models.Model):
    studentid = models.CharField(max_length=10, primary_key=True)
    fullname = models.CharField(max_length=250)
    email = models.EmailField()
    password = models.CharField(max_length=15)
    semester = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    subjects = models.TextField()


class Teacher(models.Model):
    teacherid = models.CharField(max_length=10, primary_key=True)
    fullname = models.CharField(max_length=250)
    designation = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length=15)
    semesters = models.TextField()
    sections = models.TextField()
    subjects = models.TextField()


class Subject(models.Model):
    semester = models.CharField(max_length=10, primary_key=True)
    subjects = models.TextField()


class CourseReg(models.Model):
    studentid = models.CharField(max_length=10, primary_key=True)
    fullname = models.CharField(max_length=250)
    semester = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    subjects = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    quizid = models.CharField(max_length=10, primary_key=True)
    teacherid = models.CharField(max_length=10)
    semester = models.TextField()
    sections = models.TextField()
    totalqs = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    subject = models.TextField()
    questions = models.TextField()

class QuizResult(models.Model):
    quizid = models.CharField(max_length=10)
    teacherid = models.CharField(max_length=10)
    studentid = models.CharField(max_length=10)
    stdname = models.TextField()
    semester = models.TextField()
    section = models.TextField()
    subject = models.TextField()
    totalqs = models.IntegerField()
    answers = models.TextField()
    attendtime = models.DateTimeField()
    score = models.IntegerField()
    
