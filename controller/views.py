from django.views import View
import requests
from django.shortcuts import redirect, render
from django.views import View
import json
from .models import User
from django.contrib.auth import login, authenticate


class dashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {"firstname":request.user.first_name}
            return render(request, 'controller/dashboard.html',context=context)
        else:
            return redirect("/login/")
        
class Login(View):
    def get(self,request):
        context={}
        return render(request, 'controller/login.html',context=context)
    
    def post(self,request):
        auser = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if auser:
            login(request, auser)
            return redirect("/dashboard/")
        else:
            context = {"fail":1}
            return render(request, 'controller/login.html',context=context)
        
class Register(View):
    def get(self,request):
        context={}
        return render(request, 'controller/register.html',context=context)
    def post(self,request):
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        linkedin_url = request.POST['linkedinurl']
        user = User.objects.create_user(username=email,
                                        first_name=firstname,
                                        last_name=lastname,
                                        linkedin_url = linkedin_url,email=email,password=password)
        auser = authenticate(request, username=user.username, password=password)
        login(request, auser)
        return redirect("/dashboard/")
    

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
