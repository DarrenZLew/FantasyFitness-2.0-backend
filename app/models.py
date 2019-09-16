from app import ma, db
from flask_login import UserMixin


# Member Class/Model
class Member(UserMixin, db.Model):
  __tablename__ = 'members'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(80))
  last_name = db.Column(db.String(80))
  email = db.Column(db.String(80), unique=True)
  password = db.Column(db.String(80))
  leagues = db.relationship('Member_league', back_populates='member')

# Member Schema


class MemberSchema(ma.Schema):
  class Meta:
      fields = ('id', 'first_name', 'last_name', 'email', 'password', 'leagues')


# Init schema
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# League Class/Model

class League(db.Model):
    __tablename__ = 'leagues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    type = db.Column(db.String(80))
    members = db.relationship('Member_league', back_populates='league')

# League Schema

class LeagueSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type', 'members')


# Init schema
league_schema = LeagueSchema()
leagues_schema = LeagueSchema(many=True)

# Member League Class/Model


class Member_league(db.Model):
    __tablename__ = 'member_league'

    league_id = db.Column(db.Integer, db.ForeignKey(
        'leagues.id'), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), primary_key=True)
    privilege = db.Column(db.String(80))
    league = db.relationship('League', back_populates="members")
    member = db.relationship('Member', back_populates="leagues")

# Activity Class/Model


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer)
    points = db.Column(db.Integer)
    name = db.Column(db.String(80))
    bonus = db.Column(db.Boolean)
    limit = db.Column(db.Integer)


# Activity Schema


class ActivitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'league_id', 'points', 'name', 'bonus', 'limit')


# Init schema
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)


# Season Class/Model


class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer)
    weeks = db.Column(db.Integer)
    disabled = db.Column(db.Boolean)
    start_date = db.Column(db.Date)


# Season Schema


class SeasonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'league_id', 'weeks', 'disabled', 'start_date')


# Init schema
season_schema = SeasonSchema()
seasons_schema = SeasonSchema(many=True)