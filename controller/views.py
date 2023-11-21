from django.views import View
import requests
from django.shortcuts import redirect, render
from django.views import View
import json
from .models import User


class dashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            if linkedin_info=="{}":
                context={}
            else:
                context=json.loads(linkedin_info)
            return render(request, 'controller/dashboard.html',context=context)
        else:
            redirect("login")
    


class importv(View):
    def get(self,request):
            if request.user.is_authenticated:
                linkedin_url = request.user.linkedin_url
                api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
                api_key = 'UMNaQcpE5z6oU-Tp9OgmbQ'
                headers = {'Authorization': 'Bearer ' + api_key}
                response = requests.get(api_endpoint,
                            params={'url': linkedin_url,'skills': 'include'},
                            headers=headers)
                # a = response.text.replace("\"", ";")
                # b = a.replace("\'","\"")
                # c = b.replace(";","\'")
                User.objects.filter(username=request.user.username).update(linkedin_info=response.text)
                return render(request, 'controller/dashboard.html',context={"imported":"1"})
            else:
                redirect("login")

class information(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/information.html')
        else:
            redirect("login")

class education(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            if linkedin_info=="{}":
                context={}
            else:
                context=json.loads(linkedin_info)
            return render(request, 'controller/education.html',context=context)
        else:
            redirect("login")

class addeducation(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-education.html')
        else:
            redirect("login")

class work(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            if linkedin_info=="{}":
                context={}
            else:
                context=json.loads(linkedin_info)
            return render(request, 'controller/WorkExperience.html',context=context)
        else:
            redirect("login")

class addwork(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-WorkExperience.html')
        else:
            redirect("login")
            
class portfolio(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
            redirect("login")

class addportfolio(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-portfolio.html')
        else:
            redirect("login")

class export(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
            redirect("login")

class feedback(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
            redirect("login")

class dashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            if linkedin_info=="{}":
                context={}
            else:
                context=json.loads(linkedin_info)
            return render(request, 'controller/dashboard.html',context=context)
        else:
            return redirect("/login/")
    


class importv(View):
    def get(self,request):
            if request.user.is_authenticated:
                linkedin_url = request.user.linkedin_url
                api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
                api_key = 'UMNaQcpE5z6oU-Tp9OgmbQ'
                headers = {'Authorization': 'Bearer ' + api_key}
                response = requests.get(api_endpoint,
                            params={'url': linkedin_url,'skills': 'include'},
                            headers=headers)
                # a = response.text.replace("\"", ";")
                # b = a.replace("\'","\"")
                # c = b.replace(";","\'")
                User.objects.filter(username=request.user.username).update(linkedin_info=response.text)
                return render(request, 'controller/dashboard.html',context={"imported":"1"})
            else:
               return redirect("/login/")

class information(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/information.html')
        else:
            return redirect("/login/")

class education(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            if linkedin_info=="{}":
                context={}
            else:
                context=json.loads(linkedin_info)
            return render(request, 'controller/education.html',context=context)
        else:
            return redirect("/login/")

class addeducation(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-education.html')
        else:
            return redirect("/login/")

class work(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            if linkedin_info=="{}":
                context={}
            else:
                context=json.loads(linkedin_info)
            return render(request, 'controller/WorkExperience.html',context=context)
        else:
            return redirect("/login/")

class addwork(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-WorkExperience.html')
        else:
            return redirect("/login/")
            
class portfolio(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
            return redirect("/login/")

class addportfolio(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-portfolio.html')
        else:
            return redirect("/login/")

class export(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
           return redirect("/login/")

class feedback(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
            return redirect("/login/")
