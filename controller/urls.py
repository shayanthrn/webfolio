from django.urls import path
from controller.admin import Login_site
from .views import *


urlpatterns = [
    path('',landind.as_view(),name="dashboard"),
    path('login/',Login.as_view()),
    path('changepass/',changepassword.as_view()),
    path('register/',Register.as_view()),
    path('dashboard/',dashboard.as_view()),
    path('import/',importv.as_view()),
    path('information/',information.as_view()),
    path('education/',education.as_view()),
    path('education/<str:id>/',editeducation.as_view()),
    path('education/a/add/',addeducation.as_view()),
    path('education/a/delete/<str:id>/',deleteeducation.as_view()),
    path('work/',work.as_view()),
    path('work/<str:id>/',editwork.as_view()),
    path('work/a/add/',addwork.as_view()),
    path('work/a/delete/<str:id>/',deletework.as_view()),
    path('portfolio/',portfolio.as_view()),
    path('portfolio/<str:id>/',editportfolio.as_view()),
    path('portfolio/a/add/',addportfolio.as_view()),
    path('portfolio/a/delete/<str:id>/',deleteportfolio.as_view()),
    path('design/',design.as_view()),
    path('feedback/',feedback.as_view()),
]