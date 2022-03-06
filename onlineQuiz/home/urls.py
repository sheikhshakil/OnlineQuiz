from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='Quizify Home'),
    path('stdregister/', views.stdRegister, name='Student Register'),
    path('tcRegister/', views.tcRegister, name="Teacher Register"),
    path('stdRegPost/', views.stdRegPost, name='Success'),
    path('tcRegPost/', views.tcRegPost, name="Success"),
    path('login/', views.login, name='Login'),
    path('loginPost/', views.loginPost, name="Success"),
    path('profile/', views.profile, name="Profile"),
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('verify/', views.verify, name="TeacherAuth"),
    path('seeCourseReq/', views.seeCourseReq, name="SeeReg"),
    path('acceptReg/', views.acceptReg, name="Accept"),
    path('rejectReg/', views.rejectReg, name="Reject"),
    path('filterReq/', views.filterReq, name="Filter"),
    path('stdSubjectsPost/', views.stdSubjectsPost),
    path('logout/', views.logout, name="Logout"),
    path('createQuiz/', views.createQuiz, name="Create Quiz"),
    path('viewQuiz/', views.viewQuiz, name="View Quiz"),
    path('postQuiz/', views.postQuiz, name="Post Quiz"),
    path('attendQuiz/', views.attendQuiz, name="Attend Quiz"),
    path('judgement/', views.judgement, name="Judge Quiz"),
    path('subDetails/', views.subDetails, name="Submissions")
]