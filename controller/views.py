from django.views import View
import requests
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.apps import apps
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
import openai
import json
from django.conf import settings
from RandomForest import model


openai.api_key = settings.API_KEY


class landing(View):
    def get(self,request):
        return render(request, 'controller/LandingPage.html')

class dashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {"firstname":request.user.first_name,"userid":request.user.id}
            return render(request, 'controller/dashboard.html',context=context)
        else:
            return redirect("/login/")

class website(View):
    def get(self, request, id):
        website = Website.objects.filter(user_id=id).first()
        web_components = website.components.all()
        html_content = ""

        for comp in web_components:
            website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
            content_type = website_component_order.content_type
            theme = website_component_order.theme

            if content_type == "controller | intro component":
                intro_comp = IntroComponent.objects.filter(id=website_component_order.component.id).first()
                html = intro_comp.html
                html = html.replace("^^firstname^^", str(request.user.first_name))
                html = html.replace("^^lastname^^", str(request.user.last_name))
                html = html.replace("^^description^^", str(request.user.description))
                html = html.replace("^^theme^^", theme)
                html = html.replace("^^email^^", str(request.user.email))
                html = html.replace("^^jobtitle^^", str(request.user.job_title))
                html_content += html
        for comp in web_components:
            website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
            content_type = website_component_order.content_type
            theme = website_component_order.theme
            if content_type == "controller | education component":
                educations = Education.objects.filter(user=request.user)
                edu_comp = EducationComponent.objects.filter(id=website_component_order.component.id).first()
                html = edu_comp.html
                iterable = ""
                for edu in educations:
                    temp = edu_comp.iterable_html
                    temp = temp.replace("^^theme^^", theme)
                    temp = temp.replace("^^school^^", str(edu.school))
                    temp = temp.replace("^^degree^^", str(edu.degree))
                    temp = temp.replace("^^grade^^", str(edu.grade))
                    temp = temp.replace("^^description^^", str(edu.description))
                    temp = temp.replace("^^field_of_study^^", str(edu.field_of_study))
                    temp = temp.replace("^^start_date^^", str(edu.start_date))
                    temp = temp.replace("^^end_date^^", str(edu.end_date))
                    iterable += temp
                html = html.replace("^^iterate^^", iterable)
                html_content += html
        for comp in web_components:
            website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
            content_type = website_component_order.content_type
            theme = website_component_order.theme
            if content_type == "controller | work component":
                works = Work.objects.filter(user=request.user)
                work_comp = WorkComponent.objects.filter(id=website_component_order.component.id).first()
                html = work_comp.html
                iterable = ""
                for work in works:
                    temp = work_comp.iterable_html
                    temp = temp.replace("^^theme^^", theme)
                    temp = temp.replace("^^company_name^^", str(work.company_name))
                    temp = temp.replace("^^title^^", str(work.title))
                    temp = temp.replace("^^location^^", str(work.location))
                    temp = temp.replace("^^employment_type^^", str(work.employment_type))
                    temp = temp.replace("^^description^^", str(work.description))
                    temp = temp.replace("^^start_date^^", str(work.start_date))
                    temp = temp.replace("^^end_date^^", str(work.end_date))
                    iterable += temp
                html = html.replace("^^iterate^^", iterable)
                html_content += html
        for comp in web_components:
            website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
            content_type = website_component_order.content_type
            theme = website_component_order.theme
            if content_type == "controller | portfolio component":
                portfolios = Portfolio.objects.filter(user=request.user)
                port_comp = PortfolioComponent.objects.filter(id=website_component_order.component.id).first()
                html = port_comp.html
                iterable = ""
                for portfolio in portfolios:
                    temp = port_comp.iterable_html
                    temp = temp.replace("^^theme^^", theme)
                    temp = temp.replace("^^company_name^^", str(portfolio.company_name))
                    temp = temp.replace("^^name^^", str(portfolio.name))
                    temp = temp.replace("^^thumbnail^^", str(portfolio.thumbnail))
                    temp = temp.replace("^^description^^", str(portfolio.description))
                    temp = temp.replace("^^start_date^^", str(portfolio.start_date))
                    temp = temp.replace("^^end_date^^", str(portfolio.end_date))
                    iterable += temp
                html = html.replace("^^iterate^^", iterable)
                html_content += html
        for comp in web_components:
            website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
            content_type = website_component_order.content_type
            theme = website_component_order.theme    
            if content_type == "controller | skills component":
                works = Work.objects.filter(user=request.user)
                skills = []
                for work in works:
                    skills += work.skills.split(",")
                skill_comp = SkillsComponent.objects.filter(id=website_component_order.component.id).first()
                html = skill_comp.html
                iterable = ""
                for skill in skills:
                    temp = skill_comp.iterable_html
                    temp = temp.replace("^^skill^^", str(skill))
                    temp = temp.replace("^^theme^^", theme)
                    iterable += temp
                html = html.replace("^^iterate^^", iterable)
                html_content += html

        return render(request, 'controller/website.html', {'html_content': html_content})


class export(View):
    def get(self, request):
        if request.user.is_authenticated:
            website = Website.objects.filter(user=request.user).first()
            web_components = website.components.all()
            html_content = ""

            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme

                if content_type == "controller | intro component":
                    intro_comp = IntroComponent.objects.filter(id=website_component_order.component.id).first()
                    html = intro_comp.html
                    html = html.replace("^^firstname^^", str(request.user.first_name))
                    html = html.replace("^^lastname^^", str(request.user.last_name))
                    html = html.replace("^^description^^", str(request.user.description))
                    html = html.replace("^^theme^^", theme)
                    html = html.replace("^^email^^", str(request.user.email))
                    html = html.replace("^^jobtitle^^", str(request.user.job_title))
                    html_content += html
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme
                if content_type == "controller | education component":
                    educations = Education.objects.filter(user=request.user)
                    edu_comp = EducationComponent.objects.filter(id=website_component_order.component.id).first()
                    html = edu_comp.html
                    iterable = ""
                    for edu in educations:
                        temp = edu_comp.iterable_html
                        temp = temp.replace("^^theme^^", theme)
                        temp = temp.replace("^^school^^", str(edu.school))
                        temp = temp.replace("^^degree^^", str(edu.degree))
                        temp = temp.replace("^^grade^^", str(edu.grade))
                        temp = temp.replace("^^description^^", str(edu.description))
                        temp = temp.replace("^^field_of_study^^", str(edu.field_of_study))
                        temp = temp.replace("^^start_date^^", str(edu.start_date))
                        temp = temp.replace("^^end_date^^", str(edu.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    html_content += html
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme
                if content_type == "controller | work component":
                    works = Work.objects.filter(user=request.user)
                    work_comp = WorkComponent.objects.filter(id=website_component_order.component.id).first()
                    html = work_comp.html
                    iterable = ""
                    for work in works:
                        temp = work_comp.iterable_html
                        temp = temp.replace("^^theme^^", theme)
                        temp = temp.replace("^^company_name^^", str(work.company_name))
                        temp = temp.replace("^^title^^", str(work.title))
                        temp = temp.replace("^^location^^", str(work.location))
                        temp = temp.replace("^^employment_type^^", str(work.employment_type))
                        temp = temp.replace("^^description^^", str(work.description))
                        temp = temp.replace("^^start_date^^", str(work.start_date))
                        temp = temp.replace("^^end_date^^", str(work.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    html_content += html
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme
                if content_type == "controller | portfolio component":
                    portfolios = Portfolio.objects.filter(user=request.user)
                    port_comp = PortfolioComponent.objects.filter(id=website_component_order.component.id).first()
                    html = port_comp.html
                    iterable = ""
                    for portfolio in portfolios:
                        temp = port_comp.iterable_html
                        temp = temp.replace("^^theme^^", theme)
                        temp = temp.replace("^^company_name^^", str(portfolio.company_name))
                        temp = temp.replace("^^name^^", str(portfolio.name))
                        temp = temp.replace("^^thumbnail^^", str(portfolio.thumbnail))
                        temp = temp.replace("^^description^^", str(portfolio.description))
                        temp = temp.replace("^^start_date^^", str(portfolio.start_date))
                        temp = temp.replace("^^end_date^^", str(portfolio.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    html_content += html
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme
                if content_type == "controller | skills component":
                    works = Work.objects.filter(user=request.user)
                    skills = []
                    for work in works:
                        skills += work.skills.split(",")
                    skill_comp = SkillsComponent.objects.filter(id=website_component_order.component.id).first()
                    html = skill_comp.html
                    iterable = ""
                    for skill in skills:
                        temp = skill_comp.iterable_html
                        temp = temp.replace("^^skill^^", str(skill))
                        temp = temp.replace("^^theme^^", theme)
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    html_content += html

            rendered_html = render(request, 'controller/website.html', {'html_content': html_content}).content

            response = HttpResponse(rendered_html, content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename="website.html"'
            return response
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
        user_web = Website(
                user=user,
            )
        user_web.save()
        auser = authenticate(request, username=user.username, password=password)
        login(request, auser)
        return redirect("/dashboard/")
    

class importv(View):
    def get(self,request):
            if request.user.is_authenticated:
                linkedin_url = request.user.linkedin_url
                api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
                api_key = 'jLIQ28V6ZyX5-cUZJmas2Q'
                headers = {'Authorization': 'Bearer ' + api_key}
                response = requests.get(api_endpoint,
                            params={'url': linkedin_url,'skills': 'include'},
                            headers=headers)
                response_json =json.loads(response.text)
                User.objects.filter(username=request.user.username).update(linkedin_info=response.text, job_title=response_json['occupation'],description=response_json['summary'])
                for edu in response_json['education']:

                    school = edu['school']
                    degree = edu['degree_name']
                    field_of_study = edu['field_of_study']
                    if edu['starts_at']:
                        starts_at_data = edu['starts_at']
                        starts_at_date = date(starts_at_data['year'], starts_at_data['month'], starts_at_data['day'])
                    else:
                        starts_at_date=None
                    start_date = starts_at_date
                    if edu['ends_at']:
                        end_at_data = edu['ends_at']
                        end_at_date = date(end_at_data['year'], end_at_data['month'], end_at_data['day'])
                    else:
                        end_at_date = None
                    end_date = end_at_date
                    grade = edu['grade']
                    description = edu['activities_and_societies']

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

                for work in response_json['experiences']:

                    title = work['title']
                    if work['starts_at']:
                        starts_at_data = work['starts_at']
                        starts_at_date = date(starts_at_data['year'], starts_at_data['month'], starts_at_data['day'])
                    else:
                        starts_at_date = None
                    start_date = starts_at_date
                    if work['ends_at']:
                        end_at_data = work['ends_at']
                        end_at_date = date(end_at_data['year'], end_at_data['month'], end_at_data['day'])
                    else:
                        end_at_date = None
                    end_date = end_at_date
                    company_name = work['company']
                    location = work['location']
                    description = work['description']
                    skills = ""
                    new_work = Work(
                        user=request.user,
                        title=title,
                        company_name=company_name,
                        start_date=start_date,
                        end_date=end_date,
                        location=location,
                        description=description,
                        skills=skills
                    )
                    new_work.save()
                return render(request, 'controller/dashboard.html',context={"imported":"1"})
            else:
               return redirect("/login/")

class information(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {"firstname":request.user.first_name,"lastname":request.user.last_name,"email":request.user.email,"linkedinurl":request.user.linkedin_url,"description":request.user.description,"job_title":request.user.job_title}
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
            user.description = request.POST["description"]
            user.job_title = request.POST["job_title"]
            user.save()
            return render(request, 'controller/confirm.html')
        else:
            return redirect("/login/")

class chatGPTsummary(View):
    def get(self, request):
        if request.user.is_authenticated:
            educations = list(Education.objects.filter(user=request.user).values())
            works = list(Work.objects.filter(user=request.user).values())
            portfolios = list(Portfolio.objects.filter(user=request.user).values())
            user_info = model_to_dict(request.user, exclude=['password','is_staff','is_active','last_login','user_permissions','date_joined','linkedin_info'])
            data = {
                'user_info': user_info,
                'educations': educations,
                'workExperiences': works,
                'projects': portfolios,
                'user_message': "give me a summary about me as my point of view",
            }
            data_str = json.dumps(data, cls=CustomJSONEncoder)
            print(data_str)
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=data_str,
                max_tokens=150
            )
            summary = response.choices[0].text.strip()
            context = {"firstname":request.user.first_name,"lastname":request.user.last_name,"email":request.user.email,"linkedinurl":request.user.linkedin_url,"description":summary,"job_title":request.user.job_title}
            return render(request, 'controller/information.html',context=context)
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
    def get(self, request):
        if request.user.is_authenticated:
            intro_components = IntroComponent.objects.all()
            education_components = EducationComponent.objects.all()
            work_components = WorkComponent.objects.all()
            portfolio_components = PortfolioComponent.objects.all()
            skills_components = SkillsComponent.objects.all()
            website = Website.objects.filter(user=request.user).first()
            web_components = website.components.all()
            components = []

            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme

                if content_type == "controller | intro component":
                    intro_comp = IntroComponent.objects.filter(id=website_component_order.component.id).first()
                    html = intro_comp.html
                    html = html.replace("^^firstname^^", str(request.user.first_name))
                    html = html.replace("^^lastname^^", str(request.user.last_name))
                    html = html.replace("^^description^^", str(request.user.description))
                    html = html.replace("^^theme^^", theme)
                    html = html.replace("^^email^^", str(request.user.email))
                    html = html.replace("^^jobtitle^^", str(request.user.job_title))
                    components.append({"html": html, "id": comp.id, "theme": theme})
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme

                if content_type == "controller | education component":
                    educations = Education.objects.filter(user=request.user)
                    edu_comp = EducationComponent.objects.filter(id=website_component_order.component.id).first()
                    html = edu_comp.html
                    iterable = ""
                    for edu in educations:
                        temp = edu_comp.iterable_html
                        temp = temp.replace("^^theme^^", theme)
                        temp = temp.replace("^^school^^", str(edu.school))
                        temp = temp.replace("^^degree^^", str(edu.degree))
                        temp = temp.replace("^^grade^^", str(edu.grade))
                        temp = temp.replace("^^description^^", str(edu.description))
                        temp = temp.replace("^^field_of_study^^", str(edu.field_of_study))
                        temp = temp.replace("^^start_date^^", str(edu.start_date))
                        temp = temp.replace("^^end_date^^", str(edu.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    components.append({"html": html, "id": comp.id, "theme": theme})

            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme

                if content_type == "controller | work component":
                    works = Work.objects.filter(user=request.user)
                    work_comp = WorkComponent.objects.filter(id=website_component_order.component.id).first()
                    html = work_comp.html
                    iterable = ""
                    for work in works:
                        temp = work_comp.iterable_html
                        temp = temp.replace("^^theme^^", theme)
                        temp = temp.replace("^^company_name^^", str(work.company_name))
                        temp = temp.replace("^^title^^", str(work.title))
                        temp = temp.replace("^^location^^", str(work.location))
                        temp = temp.replace("^^employment_type^^", str(work.employment_type))
                        temp = temp.replace("^^description^^", str(work.description))
                        temp = temp.replace("^^start_date^^", str(work.start_date))
                        temp = temp.replace("^^end_date^^", str(work.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    components.append({"html": html, "id": comp.id, "theme": theme})
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme

                if content_type == "controller | portfolio component":
                    portfolios = Portfolio.objects.filter(user=request.user)
                    port_comp = PortfolioComponent.objects.filter(id=website_component_order.component.id).first()
                    html = port_comp.html
                    iterable = ""
                    for portfolio in portfolios:
                        temp = port_comp.iterable_html
                        temp = temp.replace("^^theme^^", theme)
                        temp = temp.replace("^^company_name^^", str(portfolio.company_name))
                        temp = temp.replace("^^name^^", str(portfolio.name))
                        temp = temp.replace("^^thumbnail^^", str(portfolio.thumbnail))
                        temp = temp.replace("^^description^^", str(portfolio.description))
                        temp = temp.replace("^^start_date^^", str(portfolio.start_date))
                        temp = temp.replace("^^end_date^^", str(portfolio.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    components.append({"html": html, "id": comp.id, "theme": theme})

            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                theme = website_component_order.theme

                if content_type == "controller | skills component":
                    works = Work.objects.filter(user=request.user)
                    skills = []
                    for work in works:
                        skills += work.skills.split(",")
                    skill_comp = SkillsComponent.objects.filter(id=website_component_order.component.id).first()
                    html = skill_comp.html
                    iterable = ""
                    for skill in skills:
                        temp = skill_comp.iterable_html
                        temp = temp.replace("^^skill^^", str(skill))
                        temp = temp.replace("^^theme^^", theme)
                        iterable += temp
                    html = html.replace("^^iterate^^", iterable)
                    components.append({"html": html, "id": comp.id, "theme": theme})

            context = {
                'intro_components': intro_components,
                'education_components': education_components,
                'work_components': work_components,
                'portfolio_components': portfolio_components,
                'skills_components': skills_components,
                'web_components' : components,
                'userid': request.user.id,
            }

            return render(request, 'controller/design.html', context=context)
        else:
            return redirect("/login/")
    def post(self,request):
        if request.user.is_authenticated:
            website = Website.objects.filter(user=request.user).first()
            if 'radio_intro' in request.POST:
                component = get_object_or_404(IntroComponent, pk=request.POST['radio_intro'])
                # Create or get the WebsiteComponentOrder
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )

            if 'radio_edu' in request.POST:
                component = get_object_or_404(EducationComponent, pk=request.POST['radio_edu'])
                # Create or get the WebsiteComponentOrder
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )

            if 'radio_work' in request.POST:
                component = get_object_or_404(WorkComponent, pk=request.POST['radio_work'])
                # Create or get the WebsiteComponentOrder
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )

            if 'radio_port' in request.POST:
                component = get_object_or_404(PortfolioComponent, pk=request.POST['radio_port'])
                # Create or get the WebsiteComponentOrder
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )

    
            
            if 'radio_skill' in request.POST:
                component = get_object_or_404(SkillsComponent, pk=request.POST['radio_skill'])
                # Create or get the WebsiteComponentOrder
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )

            return redirect("/design/")
        else:
           return redirect("/login/")

class deletedesign(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            website_component_order = WebsiteComponentOrder.objects.get(website__user=request.user, component_id=id)
            website_component_order.delete()
            return redirect("/design/")
        else:
            return redirect("/login/")

class changetheme(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            website_component_order = WebsiteComponentOrder.objects.get(website__user=request.user, component_id=id)
            website_component_order.theme = "#" + request.GET.get('theme')
            website_component_order.save()
            return redirect("/design/")
        else:
            return redirect("/login/")

class feedback(View):
    def get(self,request):
        if request.user.is_authenticated:
            website = Website.objects.filter(user=request.user).first()
            web_components = website.components.all()
            counter = 5
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                if(content_type == "controller | intro component"):
                    counter -= 1
                if(content_type == "controller | education component"):
                    counter -= 1
                if(content_type == "controller | work component"):
                    counter -= 1
                if(content_type == "controller | portfolio component"):
                    counter -= 1
                if(content_type == "controller | skills component"):
                    counter -= 1
            return render(request, 'controller/feedback.html',context={"counter":counter})
        else:
            return redirect("/login/")
    def post(self,request):
        rating = int(request.POST.get('rating'))
        website = Website.objects.filter(user=request.user).first()
        web_components = website.components.all()
        design = ""
        if 1 <= rating <= 10:
            for comp in web_components:
                design += str(comp.id) + ","
            design = design[:-1]
            
            feedback, created = Feedback.objects.get_or_create(user=request.user)
            feedback.rating = rating
            feedback.design = design
            feedback.save()

            return render(request, 'controller/confirm.html')  # Redirect to a success page
        else:
            return HttpResponse("Invalid rating. Please provide a rating between 1 and 10.")

class backdoor(View):
    def get(self,request):
        website = Website.objects.filter(user=request.user).first()
        web_components = website.components.all()
        design = ""
        for comp in web_components:
            design += str(comp.id) + ","
            design = design[:-1]
        return HttpResponse(design)


from datetime import date     
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class AIdesign(View):
    def get(self,request):
        if request.user.is_authenticated:
            website = Website.objects.filter(user=request.user).first()
            web_components = website.components.all()
            input_comp = {}
            introhas = 0
            eduhas = 0
            workhas = 0
            porthas = 0
            skillhas = 0
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                if(content_type == "controller | intro component"):
                    introhas = 1
                    input_comp['intro_component'] = comp.id
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                if(content_type == "controller | education component"):
                    eduhas = 1
                    input_comp['education_component'] = comp.id
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                if(content_type == "controller | work component"):
                    workhas = 1
                    input_comp['work_component'] = comp.id
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                if(content_type == "controller | portfolio component"):
                    porthas = 1
                    input_comp['portfolio_component'] = comp.id
            for comp in web_components:
                website_component_order = WebsiteComponentOrder.objects.get(website=website, component=comp)
                content_type = website_component_order.content_type
                if(content_type == "controller | skills component"):
                    skillhas = 1
                    input_comp['skills_component'] = comp.id
            if(introhas + eduhas + workhas + porthas + skillhas <5):
                WebsiteComponentOrder.objects.filter(website=website).delete()
                best_combination, max_score = model.find_optimal_combination(input_comp)
                component = get_object_or_404(IntroComponent, pk=best_combination['intro_component'])
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )
                component = get_object_or_404(EducationComponent, pk=best_combination['education_component'])
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )
                component = get_object_or_404(WorkComponent, pk=best_combination['work_component'])
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )
                component = get_object_or_404(PortfolioComponent, pk=best_combination['portfolio_component'])
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )
                component = get_object_or_404(SkillsComponent, pk=best_combination['skills_component'])
                website_component_order, created = WebsiteComponentOrder.objects.get_or_create(
                    website=website,
                    component=component,
                    content_type=ContentType.objects.get_for_model(component)
                )
                print("Best Combination:", best_combination)
                print("Maximum Predicted Score:", max_score)
                return render(request, 'controller/designai.html',context={'success':1,'score':max_score})
            else:
                return render(request, 'controller/designai.html',context={'success':0})
        else:
            return redirect("/login/")