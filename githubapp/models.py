# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Language(models.Model):
    language = models.CharField(primary_key=True, max_length=1000)
    created_date = models.DateTimeField(auto_now=True)


class Location(models.Model):
    location = models.CharField(primary_key=True, max_length=1000)
    created_date = models.DateTimeField(auto_now=True)


class Queries(models.Model):
    query = models.TextField(primary_key=True)
    total_results = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reports'
        verbose_name_plural = 'Reports'


class GitHub(models.Model):
    user = models.TextField()
    name = models.TextField(null=True)
    email = models.EmailField(null=True)
    github_id = models.IntegerField()
    avatar_url = models.TextField()
    gravatar_id = models.TextField()
    url = models.TextField()
    html_url = models.TextField()
    followers_url = models.TextField()
    following_url = models.TextField()
    gists_url = models.TextField()
    starred_url = models.TextField()
    subscriptions_url = models.TextField()
    organizations_url = models.TextField()
    repos_url = models.TextField()
    events_url = models.TextField()
    received_events_url = models.TextField()
    type = models.TextField()
    site_admin = models.TextField()
    location = models.TextField(null=True)
    company = models.TextField(null=True)
    language = models.ForeignKey("Language", null=True)
    following = models.IntegerField(null=True)
    followers = models.IntegerField(null=True)
    public_repos = models.IntegerField(null=True)
    public_gists = models.IntegerField(null=True)
    query = models.ForeignKey("Queries", null=True)
    created_date = models.DateTimeField(auto_now=True)

    def admin_thumbnail(self):
        return '<img src="%s" width="30" height="30" />' % (self.avatar_url) 
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


    class Meta:
        verbose_name = 'Github'
        verbose_name_plural = 'Github'