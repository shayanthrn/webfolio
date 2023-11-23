from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)


class LoginArea(admin.AdminSite):
    site_header = 'Login'
    login_template = 'controller/login.html'

Login_site = LoginArea(name='Login')

Login_site.register(User)

admin.site.register(Education)
admin.site.register(Portfolio)
admin.site.register(Work)
admin.site.register(IntroComponent)
admin.site.register(EducationComponent)
admin.site.register(WorkComponent)
admin.site.register(PortfolioComponent)
admin.site.register(SkillsComponent)