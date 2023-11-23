from django.test import TestCase
from django.urls import reverse
from .models import User, Education, Work, Portfolio

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_landing_view(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')  # Assuming 'testuser' is displayed in the dashboard for an authenticated user

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, '/dashboard/')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {'email': 'test@example.com', 'firstname': 'John', 'lastname': 'Doe', 'password': 'testpassword', 'linkedinurl': 'https://www.linkedin.com/in/testuser/'})
        self.assertRedirects(response, '/dashboard/')

    def test_import_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('import'))
        self.assertEqual(response.status_code, 200)

    def test_information_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('information'))
        self.assertEqual(response.status_code, 200)

    def test_information_view_unauthenticated(self):
        response = self.client.get(reverse('information'))
        self.assertRedirects(response, '/login/')

    def test_change_password_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('change_password'), {'password': 'newpassword'})
        self.assertEqual(response.status_code, 200)

    def test_change_password_view_unauthenticated(self):
        response = self.client.get(reverse('change_password'))
        self.assertRedirects(response, '/login/')

    def test_education_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('education'))
        self.assertEqual(response.status_code, 200)

    def test_add_education_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_education'))
        self.assertEqual(response.status_code, 200)

    def test_add_education_view_unauthenticated(self):
        response = self.client.get(reverse('add_education'))
        self.assertRedirects(response, '/login/')

    def test_delete_education_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        education = Education.objects.create(user=self.user, school='Test School', degree='Test Degree')
        response = self.client.get(reverse('delete_education', args=[education.id]))
        self.assertRedirects(response, '/confirm/')  # Adjust the confirmation page URL

    def test_edit_education_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        education = Education.objects.create(user=self.user, school='Test School', degree='Test Degree')
        response = self.client.get(reverse('edit_education', args=[education.id]))
        self.assertEqual(response.status_code, 200)

    def test_work_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('work'))
        self.assertEqual(response.status_code, 200)

    def test_add_work_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_work'))
        self.assertEqual(response.status_code, 200)

    def test_add_work_view_unauthenticated(self):
        response = self.client.get(reverse('add_work'))
        self.assertRedirects(response, '/login/')

    def test_delete_work_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        work = Work.objects.create(user=self.user, title='Test Title', employment_type='Full Time')
        response = self.client.get(reverse('delete_work', args=[work.id]))
        self.assertRedirects(response, '/confirm/')  # Adjust the confirmation page URL

    def test_edit_work_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        work = Work.objects.create(user=self.user, title='Test Title', employment_type='Full Time')
        response = self.client.get(reverse('edit_work', args=[work.id]))
        self.assertEqual(response.status_code, 200)

    def test_portfolio_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('portfolio'))
        self.assertEqual(response.status_code, 200)

    def test_add_portfolio_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_portfolio'))
        self.assertEqual(response.status_code, 200)

    def test_add_portfolio_view_unauthenticated(self):
        response = self.client.get(reverse('add_portfolio'))
        self.assertRedirects(response, '/login/')

    def test_delete_portfolio_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        portfolio = Portfolio.objects.create(user=self.user, name='Test Portfolio')
        response = self.client.get(reverse('delete_portfolio', args=[portfolio.id]))
        self.assertRedirects(response, '/confirm/')  # Adjust the confirmation page URL

    def test_edit_portfolio_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        portfolio = Portfolio.objects.create(user=self.user, name='Test Portfolio')
        response = self.client.get(reverse('edit_portfolio', args=[portfolio.id]))
        self.assertEqual(response.status_code, 200)

    def test_design_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('design'))
        self.assertEqual(response.status_code, 200)

    def test_feedback_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)

    # Add more tests for other views...

    def tearDown(self):
        # Clean up any test data
        self.user.delete()