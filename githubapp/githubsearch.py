import requests
class gitHubApi():
    """
    """
    def __init__(self, request):
        self.request = request
        self.basic_search_url = "https://api.github.com/search/users"


    def make_the_search_query(self):
        """
        """
        query_perms = {"location": "+location:",  "search_type": "+type:",\
                       "fields":"+in:", "language":"+language:", "followers":"+followers:=>"}
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
        
        return return_dict

    def get_the_results(self):
        """
        """
        results = requests.get(self.basic_search_url)
        return results
        
