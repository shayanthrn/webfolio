from django.test import TestCase
from django.shortcuts import resolve_url
from .models import User, Website, Work, Portfolio

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_web = Website(
                user=self.user,
            )

    def test_landing_view(self):
        response = self.client.get(resolve_url("/"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/dashboard/'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)  # Assuming 'firstname' is displayed in the dashboard for an authenticated user

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(resolve_url('/dashboard/'))
        self.assertRedirects(response, '/login/')

    def test_login_view(self):
        response = self.client.get(resolve_url('/login/'))
        self.assertEqual(response.status_code, 200)


    def test_register_view(self):
        response = self.client.get(resolve_url('/register/'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post(self):
        response = self.client.post(resolve_url('/register/'), {'email': 'test@example.com', 'firstname': 'John', 'lastname': 'Doe', 'password': 'testpassword', 'linkedinurl': 'https://www.linkedin.com/in/testuser/'})
        self.assertRedirects(response, '/dashboard/')


    def test_information_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/information/'))
        self.assertEqual(response.status_code, 200)

    def test_information_view_unauthenticated(self):
        response = self.client.get(resolve_url('/information/'))
        self.assertRedirects(response, '/login/')


    def test_education_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/education/'))
        self.assertEqual(response.status_code, 200)


    def test_work_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/work/'))
        self.assertEqual(response.status_code, 200)


    def test_portfolio_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/portfolio/'))
        self.assertEqual(response.status_code, 200)


    def test_design_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(resolve_url('/design/'))
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        # Clean up any test data
        self.user.delete()
        self.user_web.delete()