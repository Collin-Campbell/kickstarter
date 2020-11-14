import requests
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Database instance
DB = SQLAlchemy(app)

kickstarter_data = "TrBQfgao6YB9BKJFQ"

# request access to public API
URL = f"https://api.apify.com/v2/datasets/{kickstarter_data}/items"
request = requests.get(URL)
data = request.json()

# root endpoint
@app.route('/')
def root():
    success = Record.query.filter(Record.pledged >= Record.goal).all()
    return str(success)
# successful if pledged amount >= goal amount

@app.route('/refresh')
def refresh():
    """Pull fresh data from Apify and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # Get data from Apify, make Record objects with it, and add to db
    for i in range (0, len(data)):
        record = Record()
        record.id = i
        record.blurb = data[i]['blurb']
        record.link = data[i]['link']
        record.category_name = data[i]['categoryName']
        record.launch_date = datetime.fromtimestamp(data[i]['launched_at'])
        record.deadline_date = datetime.fromtimestamp(data[i]['deadline'])
        record.pledged = data[i]['pledged']
        record.goal = data[i]['goal']
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'


# Database table "Record"
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    blurb = DB.Column(DB.String, nullable=False)
    link = DB.Column(DB.String, nullable=False)
    category_name = DB.Column(DB.String, nullable=False)
    launch_date = DB.Column(DB.String, nullable=False)
    deadline_date = DB.Column(DB.String, nullable=False)
    pledged = DB.Column(DB.Integer, nullable=False)
    goal = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        dictionary = {"id": self.id,
                        "blurb": self.blurb,
                        "link": self.link,
                        "category_name": self.category_name,
                        "launch_date": self.launch_date,
                        "deadline_date": self.deadline_date,
                        "pledged": self.pledged,
                        "goal": self.goal,
                        }
        return str(dictionary)