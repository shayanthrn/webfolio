from django.urls import path
from controller.forms import UserLoginForm
from .views import *


urlpatterns = [
    path('linkedInimport/', Analyze.as_view(), name='analyze'),
    # path(
    #     'login/',
    #     LoginView.as_view(
    #         template_name="login.html",
    #         authentication_form=UserLoginForm
    #         ),
    #     name='login'
    # ),
    path('test/', Test.as_view(), name='test'),
]