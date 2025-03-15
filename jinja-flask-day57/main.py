from flask import Flask, render_template
from urllib3.util.util import to_str

import post

app = Flask(__name__)

blogs = post.Post()
blog_data = blogs.get_blogs()

@app.route('/')
def home():
    return render_template("index.html", blogs=blog_data)

@app.route('/post/<int:blog_id>')
def post(blog_id):
    blog = {}
    for item in blog_data:
        if item["id"] == blog_id:
            blog = item
            break
    return render_template("post.html", blog=blog)

if __name__ == "__main__":
    app.run(debug=True)
