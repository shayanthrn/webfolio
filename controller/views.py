from django.views import View
import requests
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.apps import apps
from .models import *
from django.contrib.contenttypes.models import ContentType
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
                api_key = 'UMNaQcpE5z6oU-Tp9OgmbQ'
                headers = {'Authorization': 'Bearer ' + api_key}
                response = requests.get(api_endpoint,
                            params={'url': linkedin_url,'skills': 'include'},
                            headers=headers)
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
                if(content_type == "controller | intro component"):
                    intro_comp = IntroComponent.objects.filter(id=website_component_order.component.id).first()
                    html = intro_comp.html
                    html = html.replace("^^firstname^^",request.user.first_name)
                    html = html.replace("^^lastname^^",request.user.last_name)
                    html = html.replace("^^description^^",request.user.description)
                    html = html.replace("^^theme^^",intro_comp.theme)
                    html = html.replace("^^email^^",request.user.email)
                    html = html.replace("^^jobtitle^^",request.user.job_title)
                    components.append(html)
                if(content_type == "controller | education component"):
                    educations = Education.objects.filter(user=request.user)
                    edu_comp = EducationComponent.objects.filter(id=website_component_order.component.id).first()
                    html = edu_comp.html
                    iterable = ""
                    for edu in educations:
                        temp = edu_comp.iterable_html
                        temp = temp.replace("^^theme^^",edu_comp.theme)
                        temp = temp.replace("^^school^^",edu.school)
                        temp = temp.replace("^^degree^^",edu.degree)
                        temp = temp.replace("^^grade^^",edu.grade)
                        temp = temp.replace("^^description^^",edu.description)
                        temp = temp.replace("^^field_of_study^^",edu.field_of_study)
                        temp = temp.replace("^^start_date^^",str(edu.start_date))
                        temp = temp.replace("^^end_date^^",str(edu.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^",iterable)
                    components.append(html)
                if(content_type == "controller | work component"):
                    works = Work.objects.filter(user=request.user)
                    work_comp = WorkComponent.objects.filter(id=website_component_order.component.id).first()
                    html = work_comp.html
                    iterable = ""
                    for work in works:
                        temp = work_comp.iterable_html
                        temp = temp.replace("^^theme^^",work_comp.theme)
                        temp = temp.replace("^^company_name^^",work.company_name)
                        temp = temp.replace("^^title^^",work.title)
                        temp = temp.replace("^^location^^",work.location)
                        temp = temp.replace("^^employment_type^^",work.employment_type)
                        temp = temp.replace("^^description^^",work.description)
                        temp = temp.replace("^^start_date^^",str(work.start_date))
                        temp = temp.replace("^^end_date^^",str(work.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^",iterable)
                    components.append(html)
                if(content_type == "controller | portfolio component"):
                    portfolios = Portfolio.objects.filter(user=request.user)
                    port_comp = PortfolioComponent.objects.filter(id=website_component_order.component.id).first()
                    html = port_comp.html
                    iterable = ""
                    for portfolio in portfolios:
                        temp = port_comp.iterable_html
                        temp = temp.replace("^^theme^^",port_comp.theme)
                        temp = temp.replace("^^company_name^^",portfolio.company_name)
                        temp = temp.replace("^^name^^",portfolio.name)
                        temp = temp.replace("^^thumbnail^^",str(portfolio.thumbnail))
                        temp = temp.replace("^^description^^",portfolio.description)
                        temp = temp.replace("^^start_date^^",str(portfolio.start_date))
                        temp = temp.replace("^^end_date^^",str(portfolio.end_date))
                        iterable += temp
                    html = html.replace("^^iterate^^",iterable)
                    components.append(html)
                if(content_type == "controller | skills component"):
                    works = Work.objects.filter(user=request.user)
                    skills = []
                    for work in works:
                        skills += work.skills.split(",")
                    skill_comp = SkillsComponent.objects.filter(id=website_component_order.component.id).first()
                    html = skill_comp.html
                    iterable = ""
                    for skill in skills:
                        temp = skill_comp.iterable_html
                        temp = temp.replace("^^skill^^",skill)
                        temp = temp.replace("^^theme^^",skill_comp.theme)
                        iterable += temp
                    html = html.replace("^^iterate^^",iterable)
                    components.append(html)
            context = {
                'intro_components': intro_components,
                'education_components': education_components,
                'work_components': work_components,
                'portfolio_components': portfolio_components,
                'skills_components': skills_components,
                'web_components' : components,
            }

            return render(request, 'controller/design.html',context=context)
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
        
class feedback(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'controller/portfolio.html')
        else:
            return redirect("/login/")
