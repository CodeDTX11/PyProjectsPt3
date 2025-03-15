import requests

class Post:

    def __init__(self):
        blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
        blog_response = requests.get(blog_url)
        self.blog_data = blog_response.json()

    def get_blogs(self):
        return self.blog_data