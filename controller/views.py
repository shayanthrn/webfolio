from django.views import View
from django.http import JsonResponse
import requests

class Analyze(View):
    def get(self,request):
        
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        linkedin_profile_url = request.GET['linkedinurl']
        api_key = 'EAqVB3VefS4ds2viuLPFzg'
        headers = {'Authorization': 'Bearer ' + api_key}

        response = requests.get(api_endpoint,
                        params={'url': linkedin_profile_url,'skills': 'include'},
                        headers=headers)
        print(response.json())
        return JsonResponse({"requested":"hi"})