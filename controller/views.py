from django.views import View
import requests
from django.shortcuts import redirect, render
from django.views import View

# api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        # linkedin_profile_url = request.GET['linkedinurl']
        # api_key = 'EAqVB3VefS4ds2viuLPFzg'
        # headers = {'Authorization': 'Bearer ' + api_key}

        # response = requests.get(api_endpoint,
        #                 params={'url': linkedin_profile_url,'skills': 'include'},
        #                 headers=headers)
        # print(response.json())

class dashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            linkedin_info = request.user.linkedin_info
            print(linkedin_info==None)
            return render(request, 'controller/dashboard.html',context={})
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
            return render(request, 'controller/education.html')
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
            return render(request, 'controller/WorkExperience.html')
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

class Test(View):

    def __init__(self):
        super().__init__()

    
    def get(self, request):
        return render(request, 'controller/login.html')
