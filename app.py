from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, UserMixin, login_user
from flask_cors import CORS

# Init app
app = Flask(__name__)
CORS(app)

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

app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

#################################################################

# Member Class/Model


class Member(UserMixin, db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    # leagues = db.relationship('Member_league', back_populates='member')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

# Member Schema


class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


# Init schema
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Create a Member
@app.route('/signup', methods=['POST'])
def add_member():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    member = Member.query.filter_by(email=email).first()

    if member:
        return 'Email address already exists'

    new_member = Member(first_name, last_name, email, password)

    db.session.add(new_member)
    db.session.commit()

    return member_schema.jsonify(new_member)

# Login as Member
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    remember = True if request.json['remember'] else False

    member = Member.query.filter_by(email=email).first()

    if not member:
        return 'Could not find email/password. Please check your login details and try again'

    login_user(member, remember=remember)
    return member_schema.jsonify(member)

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
    __tablename__ = 'leagues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    type = db.Column(db.String(80))
    # members = db.relationship('Member_league', back_populates='league')

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

#################################################s################

# Member League Class/Model


# class Member_league(db.Model):
#     __tablename__ = 'member_league'

#     league_id = db.Column(db.Integer, db.ForeignKey(
#         'leagues.id'), primary_key=True)
#     member_id = db.Column(db.Integer, db.ForeignKey(
#         'members.id'), primary_key=True)
#     privilege = db.Column(db.String(80))

#     def __init__(self, name, type):
#         self.league_id = league_id
#         self.member_id = member_id
#         self.privilege = privilege

#################################################################

# Activity Class/Model


class Activity(db.Model):
    __tablename__ = 'activities'

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

#################################################################

# Season Class/Model


class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer)
    weeks = db.Column(db.Integer)
    disabled = db.Column(db.Boolean)
    start_date = db.Column(db.Date)

    def __init__(self, league_id, weeks, disabled, start_date):
        self.league_id = league_id
        self.weeks = weeks
        self.disabled = disabled
        self.start_date = start_date

# Season Schema


class SeasonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'league_id', 'weeks', 'disabled', 'start_date')


# Init schema
season_schema = SeasonSchema()
seasons_schema = SeasonSchema(many=True)

# Create a Season
@app.route('/season', methods=['POST'])
def add_season():
    league_id = request.json['league_id']
    weeks = request.json['weeks']
    disabled = False
    start_date = request.json['start_date']

    new_season = Season(league_id, weeks, disabled, start_date)

    db.session.add(new_season)
    db.session.commit()

    return season_schema.jsonify(new_season)

# Get All Seasons
@app.route('/season', methods=['GET'])
def get_seasons():
    all_seasons = Season.query.all()
    result = seasons_schema.dump(all_seasons)
    return jsonify(result)

# Get Single Season
@app.route('/season/<id>', methods=['GET'])
def get_a(id):
    season = Season.query.get(id)
    return season_schema.jsonify(season)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
