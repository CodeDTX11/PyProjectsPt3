from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()


app = Flask(__name__)

load_dotenv()
PASSWORD = os.environ.get("GMAIL_PASSWORD")
MY_EMAIL = "dm5messerly@gmail.com"

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["Post", "Get"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        guest_email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=guest_email,
            to_addrs=MY_EMAIL,
            msg="Subject:Blog Message\n\n"
                f"name: {name}\n"
                f"senders email: {guest_email}\n"
                f"phone: {phone}\n"
                f"message: {message}"
        )

        return render_template("contact.html", msg_sent=True)
    elif request.method == "GET":
        return render_template("contact.html")
    else:
        return "<p>error</p>"

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
