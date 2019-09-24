from app import ma, db
from flask_login import UserMixin

# Member Activity Week Class/Model
class Member_activity_week(db.Model):
    __tablename__ = 'member_activity_week'

    member_id = db.Column(db.Integer, primary_key=True)
    activity_league_id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(80), primary_key=True)
    week_season_id = db.Column(db.Integer, primary_key=True)
    week_index = db.Column(db.Integer, primary_key=True)
    completed_activity_count = db.Column(db.Float)
    member = db.relationship('Member', back_populates="member_activity_week")
    activity = db.relationship('Activity', back_populates="member_activity_week")
    week = db.relationship('Week', back_populates="member_activity_week")

    __table_args__ = (
        db.ForeignKeyConstraint(['activity_league_id', 'activity_name'], ['activities.league_id', 'activities.name']),
        db.ForeignKeyConstraint(['week_season_id', 'week_index'], ['weeks.season_id', 'weeks.index']),
        db.ForeignKeyConstraint(['member_id'], ['members.id'])
    )

class MemberActivityWeekSchema(ma.Schema):
    class Meta:
        fields = ('member_id', 'activity_id', 'week_id', 'completed_activity_count')

# Init schema
member_activity_week_schema = MemberActivityWeekSchema()
member_activity_weeks_schema = MemberActivityWeekSchema(many=True)

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

    def __init__(self, league_id, member_id, privilege):
        self.league_id = league_id
        self.member_id = member_id
        self.privilege = privilege

class MemberLeagueSchema(ma.Schema):
    class Meta:
        fields = ('league_id', 'member_id', 'privilege')

# Init schema
member_league_schema = MemberLeagueSchema()
member_leagues_schema = MemberLeagueSchema(many=True)

# Member Class/Model
class Member(UserMixin, db.Model):
  __tablename__ = 'members'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(80))
  last_name = db.Column(db.String(80))
  email = db.Column(db.String(80), unique=True)
  password = db.Column(db.String(80))
  leagues = db.relationship('Member_league', back_populates='member')
  member_activity_week = db.relationship('Member_activity_week', back_populates='member')

  def __init__(self, first_name, last_name, email, password):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password

# Member Schema


class MemberSchema(ma.Schema):
  class Meta:
      fields = ('id', 'first_name', 'last_name', 'email', 'password', 'leagues', 'member_activity_week')
  leagues = ma.List(ma.Nested(MemberLeagueSchema))
  member_activity_week = ma.List(ma.Nested(MemberActivityWeekSchema))

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

    def __init__(self, name, type):
        self.name = name
        self.type = type

# League Schema

class LeagueSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type', 'members')
    members = ma.List(ma.Nested(MemberLeagueSchema))

# Init schema
league_schema = LeagueSchema()
leagues_schema = LeagueSchema(many=True)

# Activity Class/Model


class Activity(db.Model):
    __tablename__ = 'activities'

    league_id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    name = db.Column(db.String(80), primary_key=True)
    bonus = db.Column(db.Boolean)
    limit = db.Column(db.Integer)
    member_activity_week = db.relationship('Member_activity_week', back_populates='activity')

    def __init__(self, league_id, points, name, bonus):
        self.league_id = league_id
        self.points = points
        self.name = name
        self.bonus = bonus

# Activity Schema


class ActivitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'league_id', 'points', 'name', 'bonus', 'limit', 'member_activity_week')
    member_activity_week = ma.List(ma.Nested(MemberActivityWeekSchema))

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

# Week Class/Model

class Week(db.Model):
    __tablename__ = 'weeks'

    id = db.Column(db.Integer)
    season_id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, primary_key=True)
    disabled = db.Column(db.Boolean)
    member_activity_week = db.relationship('Member_activity_week', back_populates='week')

# Week Schema

class WeekSchema(ma.Schema):
    class Meta:
        fields = ('id', 'season_id', 'index', 'disabled', 'member_activity_week')
    member_activity_week = ma.List(ma.Nested(MemberActivityWeekSchema))


# Init schema
week_schema = WeekSchema()
weeks_schema = WeekSchema(many=True)