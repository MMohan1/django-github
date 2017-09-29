# views.py 

from django.shortcuts import render, HttpResponse
from githubsearch import gitHubApi
import requests

# Create your views here.

def profile(request):
    data = {}
    if request.method == 'POST':
        gha = gitHubApi(request)
        data = gha.search_the_users()
    return render(request, 'app/profile.html', {"data":data})