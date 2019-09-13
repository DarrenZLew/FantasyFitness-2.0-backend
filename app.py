from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

# Database
POSTGRES = {
    'user': 'postgres',
    'pw': 'admin',
    'db': 'fantasyfitness',
    'host': 'localhost',
    'port': '5433',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass123@localhost:5433/fantasy-fitness'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

#################################################################

# Member Class/Model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True)
    last_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

# Member Schema
class MemberSchema(ma.Schema):
  class Meta:
    fields = ('id', 'first_name', 'last_name', 'email')

# Init schema
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Create a Member
@app.route('/signup', methods=['POST'])
def add_member():
  first_name = request.json['first_name']
  last_name = request.json['last_name']
  email = request.json['email']

  new_member = Member(first_name, last_name, email)

  db.session.add(new_member)
  db.session.commit()

  return member_schema.jsonify(new_member)

# Get All Members
@app.route('/member', methods=['GET'])
def get_members():
  all_members = Member.query.all()
  result = members_schema.dump(all_members)
  return jsonify(result)

# Get Single Member
@app.route('/member/<id>', methods=['GET'])
def get_member(id):
  member = Member.query.get(id)
  return member_schema.jsonify(member)

#################################################################

# League Class/Model
class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    type = db.Column(db.String(80))

    def __init__(self, name, type):
        self.name = name
        self.type = type

# League Schema
class LeagueSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'type')

# Init schema
league_schema = LeagueSchema()
leagues_schema = LeagueSchema(many=True)

# Create a League
@app.route('/league', methods=['POST'])
def add_league():
  name = request.json['name']
  type = request.json['type']

  new_league = League(name, type)

  db.session.add(new_league)
  db.session.commit()

  return league_schema.jsonify(new_league)

# Get All Leagues
@app.route('/league', methods=['GET'])
def get_leagues():
  all_leagues = League.query.all()
  result = leagues_schema.dump(all_leagues)
  return jsonify(result)

# Get Single League
@app.route('/league/<id>', methods=['GET'])
def get_league(id):
  league = League.query.get(id)
  return league_schema.jsonify(league)

#################################################################

# Activity Class/Model
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer)
    points = db.Column(db.Integer)
    name = db.Column(db.String(80))
    bonus = db.Column(db.Boolean)
    limit = db.Column(db.Integer)

    def __init__(self, league_id, points, name, bonus, limit):
        self.league_id = league_id
        self.points = points
        self.name = name
        self.bonus = bonus
        self.limit = limit

# Activity Schema
class ActivitySchema(ma.Schema):
  class Meta:
    fields = ('id', 'league_id', 'points', 'name', 'bonus', 'limit')

# Init schema
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

# Create an Activity
@app.route('/activity', methods=['POST'])
def add_activity():
  league_id = request.json['league_id']
  points = request.json['points']
  name = request.json['name']
  bonus = request.json['bonus']
  limit = request.json['limit']

  new_activity = Activity(league_id, points, name, bonus, limit)

  db.session.add(new_activity)
  db.session.commit()

  return activity_schema.jsonify(new_activity)

# Get All Activities
@app.route('/activity', methods=['GET'])
def get_activities():
  all_activities = Activity.query.all()
  result = activities_schema.dump(all_activities)
  return jsonify(result)

# Get Single Activity
@app.route('/activity/<id>', methods=['GET'])
def get_activity(id):
  activity = Activity.query.get(id)
  return activity_schema.jsonify(activity)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
