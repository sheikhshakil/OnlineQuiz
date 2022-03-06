"""onlineQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')), #include home.urls to get the homepage
    path('stdregister/', include('home.urls')),
    path('tcRegister/', include('home.urls')),
    path('stdRegPost/', include('home.urls')),
    path('tcRegPost/', include('home.urls')),
    path('login/', include('home.urls')),
    path('loginPost/', include('home.urls')),
    path('profile/', include('home.urls')),
    path('dashboard/', include('home.urls')),
    path('verify/', include('home.urls')),
    path('seeCourseReq/', include('home.urls')),
    path('acceptReg/', include('home.urls')),
    path('rejectReg/', include('home.urls')),
    path('filterReq/', include('home.urls')),
    path('stdSubjectsPost/', include('home.urls')),
    path('logout/', include('home.urls')),
    path('createQuiz/', include('home.urls')),
    path('viewQuiz/', include('home.urls')),
    path('postQuiz/', include('home.urls')),
    path('attendQuiz/', include('home.urls')),
    path('judgement/', include('home.urls')),
    path('subDetails/', include('home.urls')),
    path('admin/', admin.site.urls)
]
