import requests
from flask import Flask, render_template

app = Flask(__name__)

#may need to create a new npoint if this link expires, idk how it works after a while
npoint_url = "https://api.npoint.io/1db08ae469233f558695"

blog_data = requests.get(npoint_url).json()

@app.route("/")
@app.route("/home")
def home():
    page_data = {
        "image": "home",
        "title": "Dylonious the third's Blog",
        "subtitle": "One blog to rule them all"
    }
    return render_template("index.html", page_data=page_data, blogs=blog_data)

@app.route("/about")
def about():
    page_data = {
        "image": "about",
        "title": "About Me",
        "subtitle": "This is what I do."
    }
    return render_template("about.html", page_data=page_data)

@app.route("/contact")
def contact():
    page_data = {
        "image": "contact",
        "title": "Contact Me",
        "subtitle": "Have questions? I do not have answers."
    }
    return render_template("contact.html", page_data=page_data)

@app.route("/post/id<int:blog_id>")
def post(blog_id):
    item = {}
    for blog in blog_data:
        if blog["id"] == blog_id:
            item = blog
            break
    page_data = {
        "image": "post",
        "title": item["title"],
        "subtitle": item["subtitle"],
        "content" : item["body"]
    }
    return render_template("post.html", page_data=page_data)

if __name__ == "__main__":
    app.run(debug=True)
    # app.run()