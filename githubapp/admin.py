from django.contrib import admin
from .models import GitHub

@admin.register(GitHub)
class GitHubAdmin(admin.ModelAdmin):
    fields = ('user', 'github_id', 'followers')
    list_display = ['admin_thumbnail','avatar_url', 'user', 'creation_date', "followers", "repos", "location"]
    github_id = 'github_id'
    empty_value_display = '-empty-'

# Register your models here.
