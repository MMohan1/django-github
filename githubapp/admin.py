from django.contrib import admin
from .models import GitHub

@admin.register(GitHub)
class GitHubAdmin(admin.ModelAdmin):
    fields = ('user', 'github_id', 'followers')
    list_display = ['admin_thumbnail', 'user', 'creation_date', "followers", "repos", "user_location"]
    search_fields = ['user']
    list_filter = ('user', 'repos')
    list_max_show_all = 5

    def user_location(self, obj):
        if obj.location:
            return obj.location.location
    
