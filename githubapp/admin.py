from django.contrib import admin
from .models import GitHub, Queries
from rangefilter.filter import DateRangeFilter


@admin.register(GitHub)
class GitHubAdmin(admin.ModelAdmin):
    fields = ('user', 'github_id', 'followers')
    list_display = ['admin_thumbnail', 'user', "email", 'creation_date', "followers", "public_repos", "location"]
    search_fields = ("email",)
    list_filter = (('creation_date', DateRangeFilter), 'public_repos', "location", "followers")


@admin.register(Queries)
class ReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/github_report.html"
    date_hierarchy = "created_date"
    list_filter = (('created_date', DateRangeFilter),)
    
    def changelist_view(self, request, extra_context=None):
        response = super(ReportAdmin, self).changelist_view(request, extra_context=extra_context,)
        results_dict = [{"category": "User", "today": 10, "week": 20, "month": 70},
                        {"category": "Queries", "today": 10, "week": 20, "month": 70}]
        response.context_data['summary'] = results_dict
        return response
