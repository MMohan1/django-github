import requests
from django.contrib.auth.models import User
from models import GitHub, Queries, Language, Location


class gitHubApi():
    """
    """

    def __init__(self, request):
        self.request = request
        self.basic_search_url = "https://api.github.com/search/users"

    def make_the_search_query(self):
        """
        """
        query_perms = {"location": "+location:",  "search_type": "+type:",
                       "fields": "+in:", "language": "+language:", "followers": "+followers:=>"}
        username = self.request.POST.get('user')
        self.basic_search_url += "?q=" + username
        for key, value in self.request.POST.iteritems():
            if value and key in query_perms:
                self.basic_search_url += query_perms[key] + value

    def search_the_users(self):
        """
        """
        return_dict = {}
        self.make_the_search_query()
        print self.basic_search_url
        results = self.get_the_results()
        if results.status_code == 200:
            results_dict = results.json()
            return_dict["total"] = results_dict["total_count"]
            return_dict["query"] = self.basic_search_url
            return_dict["message"] = "Fatching the requests for Your given request is initiated...."
            self.get_all_the_results(results_dict)
        return return_dict

    def get_the_results(self, search_url=None):
        """
        """
        if not search_url:
            results = requests.get(self.basic_search_url)
        else:
            results = requests.get(search_url)
        return results

    def get_all_the_results(self, results_dict):
        """
        """
        total = results_dict["total_count"]
        location_obj, language_obj = None, None
        query_obj = self.save_the_query(total)
        if self.request.POST.get("location"):
            location_obj = self.save_the_location(self.request.POST.get("location"))
        if self.request.POST.get("language"):
            language_obj = self.save_the_language(self.request.POST.get("language"))
        self.save_the_results(results_dict["items"], query_obj, location_obj, language_obj)
        pagination = 100
        page = 2
        while pagination < results_dict["total_count"]:
            page_url = self.basic_search_url + "&page=" + str(page)
            results = self.get_the_results(page_url)
            if results.status_code == 200:
                results_dict = results.json()
                self.save_the_results(results_dict["items"], total)
            else:
                print "Something Went Wrong"
            pagination += 100
            page += 1

    def complete_the_user_data(self, user_data):
        """
        """
        followers = self.get_the_followers_count(user_data["followers_url"])
        if followers != None:
            user_data["followers"] = followers
        repos = self.get_the_followers_count(user_data["repos_url"])
        if repos != None:
            user_data["repos"] = repos
        return user_data

    def save_the_results(self, results, query_obj, location_obj, language_obj):
        """
        """
        for rec in results:
            rec["query"] = self.basic_search_url
            rec["github_id"] = rec.pop("id")
            rec.pop("score")
            rec["user"] = rec.pop("login")
            rec.pop("query")
            rec = self.complete_the_user_data(rec)
            github = self.save_the_github_data(rec)
            query_obj.github_set.add(github)
            if location_obj:
                location_obj.github_set.add(github)
            if language_obj:
                language_obj.github_set.add(github)

    def save_the_github_data(self, user_data):
        """
        """
        github_user, update = GitHub.objects.update_or_create(user=user_data["user"], defaults=user_data)
        return github_user

    def create_the_user(self, user_info):
        """
        """
        username = user_info.pop("login")
        user, created = User.objects.get_or_create(username=username, password=username)
        return user

    def get_the_followers_count(self, followers_url):
        """
        """
        response = requests.get(followers_url)
        if response.status_code == 200:
            return len(response.json())
        return None

    def get_the_repos_count(self, repos_url):
        """
        """
        response = requests.get(repos_url)
        if response.status_code == 200:
            return len(response.json())
        return None

    def save_the_location(self, location):
        """
        """
        location, update = Location.objects.get_or_create(location=location)
        return location

    def save_the_query(self, total):
        """
        """
        q = Queries(query=self.basic_search_url, total_results=total)
        q.save()
        return q

    def save_the_language(self, language):
        """
        """
        language, update = Language.objects.get_or_create(language=language)
        return language
