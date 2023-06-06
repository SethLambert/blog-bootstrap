from flask import Flask, render_template, request
import requests
from post import Post
import smtplib
from dotenv import load_dotenv
import os

env_path = os.path.join('H:/repos/blog-bootstrap/','keys.env')
load_dotenv(env_path)

#CONSTANTS
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')

#npoint_api
npoint_api = "https://api.npoint.io/1fc4d8d436b337bbd2ff"

#posts dictionary
posts = {}

def get_posts():
    global posts
    response = requests.get(npoint_api)
    all_posts = response.json()
    #print(all_posts)
    for post in all_posts:
        post_to_add = Post(post["title"],post["subtitle"],post["body"], post["id"], post["author"], post["publication_date"], post["image_url"])
        posts[post["id"]] = post_to_add
        
def send_email(name, email, phone_number, message_text):
    email_body = f"Subject:Blog Contact Form\n\nFrom:{name}\nPhone:{phone_number}\nemail:{email}\nMessage:{message_text}"
    to_email = TO_EMAIL
    with smtplib.SMTP('64.233.184.108', 587) as connection: #'64.233.184.108' is smtp.gmail.com
        connection.starttls()
        connection.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_USERNAME, 
            to_addrs=to_email, 
            msg=email_body)
        connection.close()

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    print(EMAIL_USERNAME)
    global posts
    if len(posts) == 0:
        get_posts()
    # for post in posts.values():
    #     print(post)
    return render_template("index.html", all_posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.get('/contact')
def contact():
    return render_template("contact.html", message="Have questions? I have answers.")

@app.post("/contact")
def receive_data():
    name = request.form["name"]
    email = request.form["email"]
    phone_number = request.form["phone-number"]
    message_text =  request.form["message-text"]
    send_email(name, email, phone_number, message_text)
    return render_template("contact.html", message="Email Submitted")

@app.route("/blog/<int:num>")
def get_post(num):
    global posts
    if len(posts) == 0:
        get_posts()
    return render_template("post.html", post=posts[num])

if __name__ == "__main__":
    app.run(debug=True)