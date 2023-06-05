from flask import Flask, render_template
import requests
from post import Post

#npoint_api
npoint_api = "https://api.npoint.io/1fc4d8d436b337bbd2ff"

#posts dictionary
posts = {}

def get_posts():
    global posts
    response = requests.get(npoint_api)
    all_posts = response.json()
    print(all_posts)
    for post in all_posts:
        post_to_add = Post(post["title"],post["subtitle"],post["body"], post["id"], post["author"], post["publication_date"], post["image_url"])
        posts[post["id"]] = post_to_add

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    global posts
    if len(posts) == 0:
        get_posts()
    for post in posts.values():
        print(post)
    return render_template("index.html", all_posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/blog/<int:num>")
def get_post(num):
    global posts
    if len(posts) == 0:
        get_posts()
    return render_template("post.html", post=posts[num])

if __name__ == "__main__":
    app.run(debug=True)