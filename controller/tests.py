from django.test import TestCase
from django.shortcuts import resolve_url, get_object_or_404
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.education = Education.objects.create(
            user=self.user,
            school='Test School',
            degree='Test Degree',
            field_of_study='Test Field of Study',
            start_date='2022-01-01',
            end_date='2022-12-31',
            grade='A+',
            description='Test description',
        )
        self.work = Work.objects.create(
            user=self.user,
            title='Test Title',
            employment_type='Full-Time',
            company_name='Test Company',
            start_date='2022-01-01',
            end_date='2022-12-31',
            location='Test Location',
            industry='Test Industry',
            description='Test Description',
            skills='Python,Django,JavaScript'
        )
        self.portfolio = Portfolio.objects.create(
            user=self.user,
            name='Test Portfolio',
            start_date='2022-01-01',
            end_date='2022-12-31',
            company_name='Test Company',
            description='Test Description',
            thumbnail=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )
        self.website = Website(
                id=12,
                user=self.user,
            )
        self.website.save()
        # Create test components
        self.intro_component = IntroComponent.objects.create(html='Intro HTML', theme='Intro Theme', preview=SimpleUploadedFile("test_image_intro.jpg", b"file_content", content_type="image/jpeg"))
        self.edu_component = EducationComponent.objects.create(html='Education HTML', theme='Education Theme', iterable_html='Education Iterable HTML', preview=SimpleUploadedFile("test_image_edu.jpg", b"file_content", content_type="image/jpeg"))
        self.work_component = WorkComponent.objects.create(html='Work HTML', theme='Work Theme', iterable_html='Work Iterable HTML', preview=SimpleUploadedFile("test_image_work.jpg", b"file_content", content_type="image/jpeg"))
        self.portfolio_component = PortfolioComponent.objects.create(html='Portfolio HTML', theme='Portfolio Theme', iterable_html='Portfolio Iterable HTML', preview=SimpleUploadedFile("test_image_port.jpg", b"file_content", content_type="image/jpeg"))
        self.skills_component = SkillsComponent.objects.create(html='Skills HTML', theme='Skills Theme', iterable_html='Skills Iterable HTML', preview=SimpleUploadedFile("test_image_skill.jpg", b"file_content", content_type="image/jpeg"))
        

    # landing page tests

    def test_landing_view_unauthenticated(self):
        response = self.client.get(resolve_url("/"))
        self.assertEqual(response.status_code, 200)

    def test_landing_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url("/"))
        self.assertEqual(response.status_code, 200)

    # test login

    def test_login_view_unauthenticated(self):
        response = self.client.get(resolve_url('/login/'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/login/'))
        self.assertEqual(response.status_code, 200)


    def test_login_correct(self):
        response = self.client.post(resolve_url('/login/'),{'username': 'testuser','password':'testpassword'})
        self.assertRedirects(response, '/dashboard/')
        response = self.client.get(resolve_url('/dashboard/'))
        self.assertEqual(response.status_code, 200)

    def test_login_wrong(self):
        response = self.client.post(resolve_url('/login/'),{'username': 'wrong@testuser.com','password':'wrong'})
        self.assertContains(response,"The credentials are not matching")

    # test register

    def test_register_view_unauthenticated(self):
        response = self.client.get(resolve_url('/register/'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/register/'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(resolve_url('/register/'), {'email': 'test@example.com', 'firstname': 'John', 'lastname': 'Doe', 'password': 'testpassword', 'linkedinurl': 'https://www.linkedin.com/in/testuser/'})
        self.assertRedirects(response, '/dashboard/')
        response = self.client.get(resolve_url('/dashboard/'))
        self.assertContains(response,'John')
        self.assertIsNotNone(User.objects.filter(username="test@example.com").first())

    # test dashboard

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/dashboard/'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)  # Assuming 'firstname' is displayed in the dashboard for an authenticated user

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(resolve_url('/dashboard/'))
        self.assertRedirects(response, '/login/')

    
    # test information

    def test_information_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/information/'))
        self.assertEqual(response.status_code, 200)

    def test_information_view_unauthenticated(self):
        response = self.client.get(resolve_url('/information/'))
        self.assertRedirects(response, '/login/')

    def test_authenticated_user_update_information(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@example.com',
            'linkedinurl': 'https://www.linkedin.com/in/johndoe/'
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url('/information/'), data)

        # Check that the user profile has been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'john.doe@example.com')
        self.assertEqual(self.user.username, 'john.doe@example.com')
        self.assertEqual(self.user.linkedin_url, 'https://www.linkedin.com/in/johndoe/')
        self.assertContains(response, "Changes has been submitted!")

    def test_authenticated_user_change_password(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'password': 'newpassword',
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url('/changepass/'), data)

        # Check that the user's password has been updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))
        self.assertContains(response, "Changes has been submitted!")

    def test_unauthenticated_user_change_password(self):
        # Make a POST request to the view without logging in
        response = self.client.post(resolve_url('/changepass/'))
        # Check that the response is a redirect to the login page
        self.assertRedirects(response, '/login/')


    # test education

    def test_education_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/education/'))
        self.assertEqual(response.status_code, 200)
    
    def test_education_view_unauthenticated(self):
        response = self.client.get(resolve_url('/education/'))
        self.assertRedirects(response, '/login/')

    def test_authenticated_user_get_add_education(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the view
        response = self.client.get(resolve_url('/education/a/add/'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'controller/add-education.html')

    def test_authenticated_user_post_add_education(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'school': 'Test School1',
            'degree': 'Test Degree',
            'field_of_study': 'Test Field of Study',
            'startdate': '2022-01-01',
            'enddate': '2022-12-31',
            'grade': 'A+',
            'description': 'Test description',
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url('/education/a/add/'), data)

        # Check that the new education record is created
        self.assertTrue(Education.objects.filter(user=self.user,school='Test School1').exists())

        # Check that the response is a successful redirect
        self.assertContains(response, "Changes has been submitted!")
        response = self.client.get(resolve_url('/education/'))
        self.assertContains(response, "Test School")

    def test_authenticated_user_get_delete_education(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # delete
        response = self.client.get(resolve_url(f'/education/a/delete/{self.education.pk}/'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'controller/confirm.html')

        # Check that the education record is deleted
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())

    def test_authenticated_user_post_edit_education(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'school': 'Updated School',
            'degree': 'Updated Degree',
            'field_of_study': 'Updated Field of Study',
            'startdate': '2022-02-01',
            'enddate': '2022-12-31',
            'grade': 'A',
            'description': 'Updated description',
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url(f'/education/{self.education.pk}/'), data)

        # Check that the education record is updated
        self.education.refresh_from_db()
        self.assertEqual(self.education.school, 'Updated School')
        self.assertEqual(self.education.degree, 'Updated Degree')
        self.assertEqual(self.education.field_of_study, 'Updated Field of Study')
        self.assertEqual(str(self.education.start_date), '2022-02-01')
        self.assertEqual(str(self.education.end_date), '2022-12-31')
        self.assertEqual(self.education.grade, 'A')
        self.assertEqual(self.education.description, 'Updated description')

        # Check that the response is a successful redirect
        self.assertTemplateUsed(response, 'controller/confirm.html')

    # test works

    def test_work_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/work/'))
        self.assertEqual(response.status_code, 200)

    def test_work_view_unauthenticated(self):
        response = self.client.get(resolve_url('/work/'))
        self.assertRedirects(response, '/login/')

    def test_authenticated_user_get_add_work(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the view
        response = self.client.get(resolve_url('/work/a/add/'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'controller/add-WorkExperience.html')

    def test_authenticated_user_post_add_work(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'title': 'New Title',
            'employment_type': 'Part-Time',
            'company_name': 'New Company',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'location': 'New Location',
            'industry': 'New Industry',
            'description': 'New Description',
            'skills': 'New Skill 1,New Skill 2',
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url('/work/a/add/'), data)

        # Check that the new work record is created
        self.assertTrue(Work.objects.filter(user=self.user, title='New Title').exists())

        # Check that the response is a successful redirect
        self.assertTemplateUsed(response, 'controller/confirm.html')
        response = self.client.get(resolve_url('/work/'))
        self.assertContains(response, "New Title")

    def test_authenticated_user_get_delete_work(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # delete
        response = self.client.get(resolve_url(f'/work/a/delete/{self.work.pk}/'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'controller/confirm.html')

        # Check that the work record is deleted
        self.assertFalse(Work.objects.filter(pk=self.work.pk).exists())

    def test_authenticated_user_post_edit_work(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'title': 'Updated Title',
            'employment_type': 'Updated Type',
            'company_name': 'Updated Company',
            'start_date': '2022-02-01',
            'end_date': '2022-12-31',
            'location': 'Updated Location',
            'industry': 'Updated Industry',
            'description': 'Updated Description',
            'skills': 'Updated Skill 1, Updated Skill 2',
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url(f'/work/{self.work.pk}/'), data)

        # Check that the work record is updated
        self.work.refresh_from_db()
        self.assertEqual(self.work.title, 'Updated Title')
        self.assertEqual(self.work.employment_type, 'Updated Type')
        self.assertEqual(self.work.company_name, 'Updated Company')
        self.assertEqual(str(self.work.start_date), '2022-02-01')
        self.assertEqual(str(self.work.end_date), '2022-12-31')
        self.assertEqual(self.work.location, 'Updated Location')
        self.assertEqual(self.work.industry, 'Updated Industry')
        self.assertEqual(self.work.description, 'Updated Description')
        self.assertEqual(self.work.skills, 'Updated Skill 1, Updated Skill 2')
        self.assertTemplateUsed(response, 'controller/confirm.html')

    # test portfolio

    def test_portfolio_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/portfolio/'))
        self.assertEqual(response.status_code, 200)

    def test_portfolio_view_unauthenticated(self):
        response = self.client.get(resolve_url('/portfolio/'))
        self.assertRedirects(response, '/login/')

    def test_authenticated_user_get_add_portfolio(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the view
        response = self.client.get(resolve_url('/portfolio/a/add/'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'controller/add-portfolio.html')

    def test_authenticated_user_post_add_portfolio(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'name': 'New Portfolio',
            'startdate': '2023-01-01',
            'enddate': '2023-12-31',
            'companyname': 'New Company',
            'description': 'New Description',
            'image': SimpleUploadedFile("new_image.jpg", b"new_file_content", content_type="image/jpeg"),
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url('/portfolio/a/add/'), data)

        # Check that the new portfolio record is created
        self.assertTrue(Portfolio.objects.filter(user=self.user, name='New Portfolio').exists())

        # Check that the response is a successful redirect
        self.assertTemplateUsed(response, 'controller/confirm.html')
        response = self.client.get(resolve_url('/portfolio/'))
        self.assertContains(response, "New Portfolio")

    def test_authenticated_user_get_delete_portfolio(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # delete
        response = self.client.get(resolve_url(f'/portfolio/a/delete/{self.portfolio.pk}/'))

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'controller/confirm.html')

        # Check that the portfolio record is deleted
        self.assertFalse(Portfolio.objects.filter(pk=self.portfolio.pk).exists())

    def test_authenticated_user_post_edit_portfolio(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'name': 'Updated Portfolio',
            'startdate': '2022-02-01',
            'enddate': '2022-12-31',
            'companyname': 'Updated Company',
            'description': 'Updated Description',
            'image': SimpleUploadedFile("updated_image.jpg", b"updated_file_content", content_type="image/jpeg"),
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url(f'/portfolio/{self.portfolio.pk}/'), data)

        # Check that the portfolio record is updated
        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.name, 'Updated Portfolio')
        self.assertEqual(str(self.portfolio.start_date), '2022-02-01')
        self.assertEqual(str(self.portfolio.end_date), '2022-12-31')
        self.assertEqual(self.portfolio.company_name, 'Updated Company')
        self.assertEqual(self.portfolio.description, 'Updated Description')
        self.assertTemplateUsed(response, 'controller/confirm.html')

    # test design

    def test_design_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/design/'))
        self.assertEqual(response.status_code, 200)

    def test_design_view_unauthenticated(self):
        response = self.client.get(resolve_url('/design/'))
        self.assertRedirects(response, '/login/')

    def test_design_view_authenticated_post(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Data for the POST request
        data = {
            'radio_intro': self.intro_component.pk,
            'radio_edu': self.edu_component.pk,
            'radio_work': self.work_component.pk,
            'radio_port': self.portfolio_component.pk,
            'radio_skill': self.skills_component.pk,
        }

        # Make a POST request to the view
        response = self.client.post(resolve_url('/design/'), data)

        # Check that the response is a successful redirect
        self.assertRedirects(response, '/design/')

        # Check that the WebsiteComponentOrder objects are imported
        self.assertTrue(WebsiteComponentOrder.objects.filter(
                    website=self.website,
                    component=self.intro_component,
                    order=1
                ).exists())
        self.assertTrue(WebsiteComponentOrder.objects.filter(
                    website=self.website,
                    component=self.edu_component,
                    order=1
                ).exists())
        self.assertTrue(WebsiteComponentOrder.objects.filter(
                    website=self.website,
                    component=self.portfolio_component,
                    order=1
                ).exists())
        self.assertTrue(WebsiteComponentOrder.objects.filter(
                    website=self.website,
                    component=self.skills_component,
                    order=1
                ).exists())
        self.assertTrue(WebsiteComponentOrder.objects.filter(
                    website=self.website,
                    component=self.work_component,
                    order=1
                ).exists())

    def tearDown(self):
        # Clean up any test data
        self.user.delete()
        self.website.delete()