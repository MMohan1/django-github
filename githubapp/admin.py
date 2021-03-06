from django.contrib import admin
from .models import GitHub, Queries
from rangefilter.filter import DateRangeFilter
from django.db.models import Sum, Case, When, IntegerField
from datetime import datetime, timedelta

@admin.register(GitHub)
class GitHubAdmin(admin.ModelAdmin):
    list_display = ['admin_thumbnail', 'user', "email", 'created_date', "followers", "public_repos", "location"]
    search_fields = ("email",)
    ordering = ('-created_date',)
    list_filter = (('created_date', DateRangeFilter), "language__language", 'public_repos', "location", "followers")


@admin.register(Queries)
class ReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/github_report.html"
    date_hierarchy = "created_date"
    list_filter = (('created_date', DateRangeFilter),)

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super(ReportAdmin, self).changelist_view(request, extra_context=extra_context,)
        curr_time = datetime.now()
        week_start_date = curr_time - timedelta(days=curr_time.weekday())
        start = request.GET.get("created_date__gte", "1900-01-01")
        end = request.GET.get("created_date__lte", "1900-01-02")
        end_tmp = end + " 23:59:59"
        results_dict_query = Queries.objects.aggregate(today=Sum(Case(When(created_date__year=curr_time.year, created_date__month=curr_time.month,
                                                                           created_date__day=curr_time.day, then=1), output_field=IntegerField())),
                                                       month=Sum(
                                                           Case(When(created_date__year=curr_time.year, created_date__month=curr_time.month, then=1),
                                                                output_field=IntegerField())),
                                                       week=Sum(Case(When(created_date__gte=week_start_date,
                                                                          then=1), output_field=IntegerField())),
                                                       total=Sum(Case(When(created_date__year__gte=1900,
                                                                           then=1), output_field=IntegerField())),
                                                       range=Sum(
                                                           Case(When(created_date__range=[start, end_tmp], then=1), output_field=IntegerField())),
                                                       )

        results_dict_user = GitHub.objects.aggregate(today=Sum(Case(When(created_date__year=curr_time.year, created_date__month=curr_time.month,
                                                                         created_date__day=curr_time.day, then=1), output_field=IntegerField())),
                                                     month=Sum(
                                                         Case(When(created_date__year=curr_time.year, created_date__month=curr_time.month, then=1),
                                                              output_field=IntegerField())),
                                                     week=Sum(Case(When(created_date__gte=week_start_date,
                                                                        then=1), output_field=IntegerField())),
                                                     total=Sum(Case(When(created_date__year__gte=1900,
                                                                         then=1), output_field=IntegerField())),
                                                     range=Sum(
                                                         Case(When(created_date__range=[start, end_tmp], then=1), output_field=IntegerField())),
                                                     )
        results_dict_query["category"] = "API Call"
        results_dict_user["category"] = "User Created"
        if start == "1900-01-01":
            start = "select from"
            end = "select to"
        results_dict = [results_dict_query, results_dict_user]
        response.context_data['summary'] = results_dict
        response.context_data['start'] = start
        response.context_data['end'] = end
        return response
