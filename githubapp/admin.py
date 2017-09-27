from django.contrib import admin
from .models import GitHub

from operator import or_
from django.db.models import Q

class MyAdmin(admin.ModelAdmin):
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(MyAdmin, self).get_search_results(
                                               request, queryset, search_term)
        search_words = search_term.split()
        if search_words:
            q_objects = [Q(**{field + '__icontains': word})
                                for field in self.search_fields
                                for word in search_words]
            queryset |= self.model.objects.filter(reduce(or_, q_objects))
        return queryset, use_distinct

@admin.register(GitHub)
class GitHubAdmin(admin.ModelAdmin):
    fields = ('user', 'github_id', 'followers')
    list_display = ['admin_thumbnail', 'user', "email",'creation_date', "followers", "public_repos", "location"]
    search_fields = ("email", 'created_date')
    list_filter = ('public_repos',)

    
