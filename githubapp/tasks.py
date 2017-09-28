# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def search_users(request, results_dict):
    """
    """
    from githubapp.githubsearch import gitHubApi
    gha = gitHubApi(request, background_process=True)
    gha.get_all_the_results(results_dict)
