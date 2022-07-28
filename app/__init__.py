from flask import Flask, redirect, render_template, request, flash
from dotenv import load_dotenv
from playhouse.shortcuts import model_to_dict
from peewee import *
import datetime
import os
from flask_gravatar import Gravatar

load_dotenv()

app = Flask(__name__, static_folder='static')

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)

else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        host = os.getenv("MYSQL_HOST"),
        port = 3306 )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

gravatar = Gravatar(app,
                    size=900,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


userinfo = {'name': 'Ryson Wong',
    'shortIntro': 'CS Student at OSU',
    'longIntro': 'Ryson Wong is from Ewa Beach, HI. He is currently studying Computer Science at Oregon State University. Ryson also serves as a satellite communications Staff Sergeant in the Space Force.',
    'work': [{'jobTitle': 'Satellite Maintainer', 'desc': "Hooked up wires", "year": "2018 - Present", 'link':'./static/img/space.jpg'},],
    'skills': ['./static/img/skillicons/c-.png','./static/img/skillicons/css-3.png', './static/img/skillicons/html-5.png',
    './static/img/skillicons/js.png','./static/img/skillicons/python.png'],
    'education': [{'type': 'Bachelors of Computer Science', 'from': 'Oregon State University', 'when': '2021 - Present', 'desc': 'Computers are cool!', 'link': './static/img/OSU.jpg'}],
    'email': '123fakemail@gmail.com',
    'hobbies':  [{'name': 'Basketball', 'caption': 'My Favorite Sport!', 'img': './static/img/hobbies_gallery/basketball.jpeg', 'active': 'active'},
     {'name': 'Fishing', 'caption': 'My favorite way to relax!', 'img': './static/img/hobbies_gallery/fishing.jpg', 'active': ''}, 
    {'name': 'Paddleboarding', 'caption': 'My second favorite watersport!', 'img': './static/img/hobbies_gallery/paddleboarding.jpg', 'active': ''}],
    'project_rows': [[{'name': 'Ryson Requests', 'tag': 'Loving Recreation of the popular memory game: "SIMON', 'tools': 'JavaScript, HTML, CSS', 'link': 'github.com/rysonw/Ryson_Requests', 'img': './static/img/hobbies_gallery/R.R.png'},
    {'name': 'Battleship: Text Edition', 'tag': 'A text-based edition of the popular board game; "Battleship', 'tools': 'Python', 'link': 'github.com/rysonw/Battleship-TextGame', 'img': './static/img/hobbies_gallery/R.R.png'},
    {'name': 'Pygame Card Game Collection', 'tag': 'A collection of card games using the module: PYGAME!', 'tools': 'Python', 'link': 'github.com/rysonw/Ryson-Card-Collection-and-More', 'img': './static/img/hobbies_gallery/Card Game.png'}
    ],
    ],
    'facebook': 'facebook.com',
    'github': 'github.com',
    'instagram': 'instagram.com',
    'linkedin':'linkedin.com' ,
    'twitter':'twitter.com'
 }


@app.route('/')
def index():
    return render_template('index.html', title='MLH Fellow', url=os.getenv('URL'), name=userinfo['name'],
    shortIntro=userinfo['shortIntro'], longIntro = userinfo['longIntro'], work = userinfo['work'], skills = userinfo['skills'],
    education = userinfo['education'], email=userinfo['email'], facebook = userinfo['facebook'], instagram = userinfo['instagram'],
    github=userinfo['github'], linkedin=userinfo['linkedin'], twitter = userinfo['twitter'], profilepic='./static/img/profile_pic.jpg',)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', 
    title="Hobbies", 
    url=os.getenv("URL"),
    hobbies = userinfo["hobbies"],
    email=userinfo['email'], 
    facebook = userinfo['facebook'], 
    instagram = userinfo['instagram'],
    github=userinfo['github'], 
    linkedin=userinfo['linkedin'], 
    twitter = userinfo['twitter']
    )

@app.route('/projects')
def projects():
    return render_template('projects.html', 
    title="Projects", 
    url=os.getenv("URL"),
    project_rows = userinfo['project_rows'],
    email=userinfo['email'], 
    facebook = userinfo['facebook'], 
    instagram = userinfo['instagram'],
    github=userinfo['github'], 
    linkedin=userinfo['linkedin'], 
    twitter = userinfo['twitter']
    )

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    if name == "":
        return "Invalid name", 400
    elif not "@" in email:
        return "Invalid email", 400
    elif content == "":
        return "Invalid content", 400
    else:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]
    }


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', 
    title="Timeline",
    posts = get_time_line_post(), 
    url=os.getenv("URL"),
    project_rows = userinfo['project_rows'],
    email=userinfo['email'], 
    facebook = userinfo['facebook'], 
    instagram = userinfo['instagram'],
    github=userinfo['github'], 
    linkedin=userinfo['linkedin'], 
    twitter = userinfo['twitter'])