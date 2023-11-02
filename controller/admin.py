from django.contrib import admin
from .models import *
# Register your models here.



class LoginArea(admin.AdminSite):
    site_header = 'Login'
    login_template = 'controller/login.html'

Login_site = LoginArea(name='Login')

Login_site.register(User)