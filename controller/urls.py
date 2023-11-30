from django.urls import path
from controller.admin import Login_site
from .views import *


urlpatterns = [
    path('',landing.as_view(),name="dashboard"), #tested
    path('login/',Login.as_view()), #tested
    path('changepass/',changepassword.as_view()), #tested
    path('register/',Register.as_view()), #tested
    path('dashboard/',dashboard.as_view()), #tested
    path('import/',importv.as_view()), #not used unit test due to request limit
    path('information/',information.as_view()), #tested
    path('education/',education.as_view()), #tested
    path('education/<str:id>/',editeducation.as_view()), #tested
    path('education/a/add/',addeducation.as_view()), #tested
    path('education/a/delete/<str:id>/',deleteeducation.as_view()), #tested
    path('work/',work.as_view()), #tested
    path('work/<str:id>/',editwork.as_view()), #tested
    path('work/a/add/',addwork.as_view()), #tested
    path('work/a/delete/<str:id>/',deletework.as_view()), #tested
    path('portfolio/',portfolio.as_view()), #tested
    path('portfolio/<str:id>/',editportfolio.as_view()), #tested
    path('portfolio/a/add/',addportfolio.as_view()), #tested
    path('portfolio/a/delete/<str:id>/',deleteportfolio.as_view()), #tested
    path('design/',design.as_view()), #tested
    path('design/delete/<str:id>/',deletedesign.as_view()), 
    path('design/changetheme/<str:id>/',changetheme.as_view()),
    path('website/<str:id>/',website.as_view()),
    path('export/',export.as_view()),
    path('feedback/',feedback.as_view()), #not started yet
]