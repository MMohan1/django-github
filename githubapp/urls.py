# app/urls.py

from django.conf.urls import url

from githubapp import views

urlpatterns = [
	url(r'^search/$', views.profile, name='search'),
]