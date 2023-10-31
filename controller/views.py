from django.shortcuts import redirect, render
from django.views import View


# Create your views here.
class Test(View):

    def __init__(self):
        super().__init__()

    
    def get(self, request):
        return render(request, 'controller/login.html')