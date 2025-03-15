from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)


@app.route('/')
def home():
    year = datetime.datetime.now().year
    random_number = random.randint(1,10)
    name = "Dylonius the Third"
    return render_template("index.html", num=random_number, year=year, name=name)

@app.route('/guess/<name>')
def guess(name):
    agify_url = "https://api.agify.io"
    genderize_url = "https://api.genderize.io"
    param = {
        "name" : name
    }
    agify_response = requests.get(agify_url, params=param)
    genderize_response = requests.get(genderize_url, params=param)

    age_data = agify_response.json()
    gender_data = genderize_response.json()

    age = int(age_data.get("age"))
    gender = gender_data["gender"]

    return render_template("guess.html", name=name, age=age, gender=gender)

@app.route('/blog/<int:num>')
def blog(num):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    blog_response = requests.get(blog_url)
    blog_data = blog_response.json()
    # print(blog_data)
    return render_template("blog.html", blogs=blog_data, num=num)


if __name__ == "__main__":
    app.run(debug=True)


