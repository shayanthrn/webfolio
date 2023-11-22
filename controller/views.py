from django.views import View
import requests
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
import json
from .models import *
from django.contrib.auth import login, authenticate


class landing(View):
    def get(self,request):
        return render(request, 'controller/LandingPage.html')

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
            context = {"firstname":request.user.first_name,"lastname":request.user.last_name,"email":request.user.email,"linkedinurl":request.user.linkedin_url}
            return render(request, 'controller/information.html',context=context)
        else:
            return redirect("/login/")
        
    def post(self,request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            user.first_name = request.POST["firstname"]
            user.last_name = request.POST["lastname"]
            user.email = request.POST["email"]
            user.username = request.POST["email"]
            user.linkedin_url = request.POST["linkedinurl"]
            user.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")
        
class changepassword(View):
    def post(self,request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)

            # Set the new password
            new_password = request.POST["password"]
            user.set_password(new_password)
            # Save the user to update the password
            user.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")

class education(View):
    def get(self,request):
        if request.user.is_authenticated:
            educations = Education.objects.filter(user=request.user)
            context={"educations":educations}
            return render(request, 'controller/education.html',context=context)
        else:
            return redirect("/login/")

class addeducation(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-education.html')
        else:
            return redirect("/login/")
        
    def post(self,request):
        if request.user.is_authenticated:
            school = request.POST.get('school')
            degree = request.POST.get('degree')
            field_of_study = request.POST.get('field_of_study')
            start_date = request.POST.get('startdate')
            end_date = request.POST.get('enddate')
            grade = request.POST.get('grade')
            description = request.POST.get('description')

            new_education = Education(
                user=request.user,
                school=school,
                degree=degree,
                field_of_study=field_of_study,
                start_date=start_date,
                end_date=end_date,
                grade=grade,
                description=description
            )

            new_education.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")

class deleteeducation(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            education = get_object_or_404(Education, pk=id)
            education.delete()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")
        
class editeducation(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            education = get_object_or_404(Education, pk=id)
            context = {"education": education}
            return render(request, 'controller/edit-education.html',context=context)
        else:
            return redirect("/login/")
    def post(self,request,id):
        if request.user.is_authenticated:
            education = get_object_or_404(Education, id=id)
            school = request.POST.get('school')
            start_date = request.POST.get('startdate')
            end_date = request.POST.get('enddate')
            degree = request.POST.get('degree')
            description = request.POST.get('description')
            field_of_study = request.POST.get('field_of_study')
            grade = request.POST.get('grade')

            education.school = school
            education.start_date = start_date
            education.end_date = end_date
            education.degree = degree
            education.description = description
            education.field_of_study = field_of_study
            education.grade = grade
            education.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")
        
class work(View):
    def get(self,request):
        if request.user.is_authenticated:
            works = Work.objects.filter(user=request.user)
            context = {"works":works}
            return render(request, 'controller/WorkExperience.html',context=context)
        else:
            return redirect("/login/")

class deletework(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            work = get_object_or_404(Work, pk=id)
            work.delete()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")

class editwork(View):
    def get(self, request, id):
        work = get_object_or_404(Work, pk=id)
        skills = work.skills.split(',')
        context = {"work": work, "skills":skills}
        return render(request, 'controller/edit-workExperience.html', context=context)

    def post(self, request, id):
        work = get_object_or_404(Work, id=id)
        work.title = request.POST.get('title')
        work.employment_type = request.POST.get('employment_type')
        work.company_name = request.POST.get('company_name')
        work.start_date = request.POST.get('start_date')
        work.end_date = request.POST.get('end_date')
        work.location = request.POST.get('location')
        work.industry = request.POST.get('industry')
        work.description = request.POST.get('description')
        skills = ""
        for i in request.POST.getlist('skills'):
            skills += i
            skills += ","
        skills = skills[:-1]
        work.skills = skills
        work.save()

        return render(request, 'controller/confirm.html')


class addwork(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-WorkExperience.html')
        else:
            return redirect("/login/")
    def post(self,request):
        if request.user.is_authenticated:
            title = request.POST.get('title')
            employment_type = request.POST.get('employment_type')
            company_name = request.POST.get('company_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            location = request.POST.get('location')
            industry = request.POST.get('industry')
            description = request.POST.get('description')
            skills = ""
            for i in request.POST.getlist('skills'):
                skills += i
                skills += ","
            skills = skills[:-1]
            new_work = Work(
                user=request.user,
                title=title,
                employment_type=employment_type,
                company_name=company_name,
                start_date=start_date,
                end_date=end_date,
                location=location,
                industry=industry,
                description=description,
                skills=skills
            )

            new_work.save() 
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")
            
class portfolio(View):
    def get(self,request):
        if request.user.is_authenticated:
            portfolios = Portfolio.objects.filter(user=request.user)
            context = {"portfolios":portfolios}
            return render(request, 'controller/portfolio.html',context=context)
        else:
            return redirect("/login/")

class addportfolio(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/add-portfolio.html')
        else:
            return redirect("/login/")
    def post(self,request):
        if request.user.is_authenticated:
            name = request.POST.get('name')
            start_date = request.POST.get('startdate')
            end_date = request.POST.get('enddate')
            company_name = request.POST.get('companyname')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            portfolio = Portfolio(
            user= request.user,
            name=name,
            start_date=start_date,
            end_date=end_date,
            company_name=company_name,
            description=description,
            thumbnail=image)

            portfolio.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")

class deleteportfolio(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            portfolio = get_object_or_404(Portfolio, pk=id)
            portfolio.delete()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")

class editportfolio(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            portfolio = get_object_or_404(Portfolio, pk=id)
            context = {"portfolio": portfolio}
            return render(request, 'controller/edit-portfolio.html',context=context)
        else:
            return redirect("/login/")
        
    def post(self,request,id):
        if request.user.is_authenticated:
            portfolio = get_object_or_404(Portfolio, id=id)
            name = request.POST.get('name')
            start_date = request.POST.get('startdate')
            end_date = request.POST.get('enddate')
            company_name = request.POST.get('companyname')
            description = request.POST.get('description')
            if 'image' in request.FILES:
                new_image = request.FILES['image']
                portfolio.thumbnail = new_image

            portfolio.name = name
            portfolio.start_date = start_date
            portfolio.end_date = end_date
            portfolio.company_name = company_name
            portfolio.description = description
            portfolio.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")
        
class design(View):
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
