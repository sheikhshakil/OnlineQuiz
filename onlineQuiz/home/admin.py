from django.contrib import admin
from home.models import Student, Teacher, Subject, CourseReg, Quiz, QuizResult

# Register your models here.
# ekhane table name include korte hobe nahole admin e show korbe na

from django.contrib import admin
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(CourseReg)
admin.site.register(Quiz)
admin.site.register(QuizResult)