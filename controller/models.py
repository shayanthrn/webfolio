from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)
    linkedin_info = models.TextField()
    linkedin_url = models.URLField()
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Education - {self.school}"
    
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='static/portfolio_thumbnails/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Portfolio - {self.name}"
    
class Work(models.Model):
    class EmploymentType(models.TextChoices):
        SELF_EMPLOYED = 'Self-employed', 'Self-employed'
        FREELANCE = 'Freelance', 'Freelance'
        INTERNSHIP = 'Internship', 'Internship'
        FULL_TIME = 'Full time', 'Full time'
        PART_TIME = 'Part time', 'Part time'
        CONTRACT = 'Contract', 'Contract'
        CO_OP = 'Co op', 'Co op'
        SEASONAL = 'Seasonal', 'Seasonal'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
    )
    company_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField()  # Assuming a comma-separated list of skills

    def __str__(self):
        return f"{self.user.username}'s Work - {self.title}"
    
class Component(models.Model):
    html = models.TextField()
    theme = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='static/component_previews/', null=True, blank=True)

    def __str__(self):
        return f"{self.__class__.__name__} Component"


class IntroComponent(Component):
    description = models.TextField()


class IterableComponent(Component):
    # Additional fields specific to iterable components can be added here
    iterable_html = models.TextField()


class EducationComponent(IterableComponent):
    pass


class WorkComponent(IterableComponent):
    pass


class PortfolioComponent(IterableComponent):
    pass


class SkillsComponent(IterableComponent):
    pass

class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    components = models.ManyToManyField(Component, through='WebsiteComponentOrder')

    def __str__(self):
        return f"Website - {self.pk} for {self.user.username}"

class WebsiteComponentOrder(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Order {self.order}: {self.component}"