import requests
from models import GitHub, Queries, Language
from django.conf import settings
from .tasks import search_users


class gitHubApi():
    """
    """

    def __init__(self, request, background_process=False):
        if not background_process:
            self.request = request.POST
        else:
            self.request = request
        self.basic_search_url = "https://api.github.com/search/users"
        self.developer_instance = settings.DEVELOPER_SETUP
        self.max_search = settings.MAX_GITHUB_SEARCH

    def make_the_search_query(self):
        """
        """
        query_perms = {"location": "+location:",  "search_type": "+type:", "repos": "+repos:=>",
                       "fields": "+in:", "language": "+language:", "followers": "+followers:=>"}
        username = self.request.get('user')
        self.basic_search_url += "?q=" + username
        for key, value in self.request.iteritems():
            if value and key in query_perms:
                self.basic_search_url += query_perms[key] + value
        self.basic_search_url = self.basic_search_url+"+sort:repositories"  # Added the default sort by repos count

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
            if self.developer_instance:
                self.get_all_the_results(results_dict)
            else:
                search_users.delay(self.request, results_dict)
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
        language_obj = None
        query_obj = self.save_the_query(total)
        if self.request.get("language"):
            language_obj = self.save_the_language(self.request.get("language"))
        self.save_the_results(results_dict["items"], query_obj, language_obj)
        pagination = 100
        page = 2
        while pagination < results_dict["total_count"] and not self.developer_instance:
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
        new_user_data = self.get_the_user_details(user_data["url"])
        user_data.update(new_user_data)
        return user_data

    def save_the_results(self, results, query_obj, language_obj):
        """
        """
        saved_count = 0
        for rec in results:
            if self.developer_instance and self.max_search <= saved_count:
                return None
            rec["query"] = self.basic_search_url
            rec["github_id"] = rec.pop("id")
            rec.pop("score")
            rec["user"] = rec.pop("login")
            rec.pop("query")
            rec = self.complete_the_user_data(rec)
            github = self.save_the_github_data(rec)
            query_obj.github_set.add(github)
            if language_obj:
                language_obj.github_set.add(github)
            saved_count += 1

    def save_the_github_data(self, user_data):
        """
        """
        print "Saving user_data", user_data
        github_user, update = GitHub.objects.update_or_create(user=user_data["user"], defaults=user_data)
        return github_user

    def get_the_user_details(self, user_url):
        """
        """
        out_dict = {}
        response = requests.get(user_url)
        if response.status_code == 200:
            response_dict = response.json()
            out_dict["name"] = response_dict["name"]
            out_dict["company"] = response_dict["company"]
            out_dict["location"] = response_dict["location"]
            out_dict["public_repos"] = response_dict["public_repos"]
            out_dict["public_gists"] = response_dict["public_gists"]
            out_dict["followers"] = response_dict["followers"]
            out_dict["following"] = response_dict["following"]
            out_dict["email"] = self.get_user_email(response_dict["login"])
        return out_dict

    def get_user_email(self, user_name):
        """
        """
        url = "https://api.github.com/users/"+user_name+"/events/public"
        response = requests.get(url)
        if response.status_code == 200:
            response_dict = response.json()
            for rec in response_dict:
                if rec.get("payload", {}).get("commits"):
                    commits = rec.get("payload", {}).get("commits")
                    for record in commits:
                        if record["author"].get("name").lower() == user_name.lower():
                            return record["author"]["email"]
        return None

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
