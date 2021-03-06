from app import app
from app.models import *
from flask import Blueprint
from flask import request, jsonify
from flask_login import LoginManager, login_user
import datetime

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
mod_league = Blueprint('league', __name__, url_prefix='/leagues')
mod_activity = Blueprint('activity', __name__, url_prefix='/activities')

login_manager = LoginManager()
login_manager.init_app(app)


# Create a Member
@mod_auth.route('/signup', methods=['POST'])
def create_member():
    # add try catch for if one of these was not found correctly
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    member = Member.query.filter_by(email=email).first()

    if member:
        return jsonify(
            {'value': {}, 'status': 'error',
             'message': 'Email address already exists'})

    new_member = Member(first_name, last_name, email, password)

    db.session.add(new_member)
    db.session.commit()

    # add check for if session didn't commit correctly

    member_data = member_schema.dump(new_member)
    return jsonify({'status': 'success', 'value': member_data,
                    'message': 'Signup successful. Hello {}!'.format(member_data["first_name"])})


@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))


# Login as Member
@mod_auth.route('/login', methods=['POST'])
def login():
    # add try catch for if one of these was not found correctly
    email = request.json['email']
    password = request.json['password']
    remember = True if request.json['remember'] else False

    member = Member.query.filter_by(email=email).first()

    if not member:
        return jsonify(
            {'value': {}, 'status': 'error',
             'message': 'Could not find email/password. Please check your login details and try again'})

    login_user(member, remember=remember)
    member_data = member_schema.dump(member)
    return jsonify({'status': 'success', 'value': member_data,
                    'message': 'Login successful. Hello {}!'.format(member_data["first_name"])})


# Get All Members
@mod_auth.route('/members', methods=['GET'])
def get_members():
    all_members = Member.query.outerjoin(Member.leagues).all()
    result = members_schema.dump(all_members)
    return jsonify({'status': 'success', 'value': result,
                    'message': 'All members retrieved!'})

# Delete a Member
@mod_auth.route('/members/<id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'status': 'success', 'value': 'Deleted',
                    'message': 'Member {} {} deleted!'.format(member.first_name, member.last_name)})


# Get Single Member
@mod_auth.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    return member_schema.jsonify(member)


# Update member to League
def update_member(member_fields):
    league_id = member_fields['league_id']
    member_id = member_fields['id']
    privilege = member_fields['privilege']
    member_exists_in_league = Member.query.filter(Member.leagues.any(
        league_id=league_id, member_id=member_id)).scalar() is not None
    if not member_exists_in_league:
        new_member_in_league = Member_league(league_id, member_id, privilege)
        db.session.add(new_member_in_league)
    else:
        member = Member_league.query.filter_by(
            league_id=league_id, member_id=member_id).first()
        member.privilege = privilege
    db.session.commit()


# Delete member from League
def delete_member(member_fields):
    league_id = member_fields['league_id']
    member_id = member_fields['id']
    member = Member_league.query.filter_by(
        league_id=league_id, member_id=member_id).first()
    db.session.delete(member)
    db.session.commit()


# Add/Delete/Update members to a League
@mod_league.route('/<league_id>/members', methods=['POST'])
def edit_members_league(league_id):
    members = request.json['members']

    for member in members:
        member['league_id'] = league_id
        if member['delete']:
            delete_member(member)
        else:
            update_member(member)

    return jsonify({'status': 'success', 'value': '',
                    'message': 'Members in league updated!'})


# Create a League
@mod_league.route('', methods=['POST'])
def add_league():
    # add try catch for if one of these was not found correctly
    name = request.json['name']
    type = request.json['type']
    member_id = request.json['member_id']

    new_league = League(name, type)

    db.session.add(new_league)
    db.session.commit()

    league_data = league_schema.dump(new_league)
    if league_data:
        new_member = {
            'league_id': new_league.id,
            'id': member_id,
            'privilege': 'admin'
        }
        update_member(new_member)
        db.session.commit()

    # Add check for if league or member didn't commit correctly

    return jsonify({'status': 'success', 'value': league_data,
                    'message': 'New league {} created!'.format(league_data["name"])})


# Get All Leagues
@mod_league.route('', methods=['GET'])
def get_leagues():
    all_leagues = League.query.all()
    result = leagues_schema.dump(all_leagues)
    message = '' if len(result) > 0 else 'No leagues are currently available'
    return jsonify({'status': 'success', 'value': result, 'message': message})

# Get All Leagues for Member
@mod_league.route('/members/<member_id>', methods=['GET'])
def get_leagues_member(member_id):
    all_member_leagues = League.query.filter(
        League.members.any(member_id=member_id)).all()
    result = leagues_schema.dump(all_member_leagues)
    message = '' if len(result) > 0 else 'No leagues are currently available'
    return jsonify({'status': 'success', 'value': result, 'message': message})

# Get Single League
@mod_league.route('/<id>', methods=['GET'])
def get_league(id):
    league = League.query.get(id)
    result = league_schema.dump(league)
    message = 'Successfully received data for league {}'.format(id)
    return jsonify({'status': 'success', 'value': result, 'message': message})


# Delete Activity from League
def delete_activity(activity_fields):
    league_id = activity_fields['league_id']
    name = activity_fields['name']
    activity = Activity.query.filter_by(
        league_id=league_id, name=name).first()
    db.session.delete(activity)
    db.session.commit()

    return jsonify({'status': 'success', 'value': 'Deleted',
                    'message': 'Activity {} deleted!'.format(name)})


def update_activity(activity_fields):
    # add try catch for if one of these was not found correctly
    league_id = activity_fields['league_id']
    name = activity_fields['name']
    points = activity_fields['points']
    bonus = activity_fields['bonus']

    activity_exists = Activity.query.filter_by(
        league_id=league_id, name=name).scalar() is not None
    if not activity_exists:
        new_activity = Activity(league_id, points, name, bonus)
        db.session.add(new_activity)
    else:
        activity = Activity.query.filter_by(
            league_id=league_id, name=name).first()
        activity.points = points
        activity.bonus = bonus


# Add activities to a league
@mod_league.route('/<league_id>/activities', methods=['POST'])
def edit_activities_league(league_id):
    activities = request.json['activities']

    for activity in activities:
        activity['league_id'] = league_id
        if activity['delete']:
            delete_activity(activity)
        else:
            update_activity(activity)

    db.session.commit()
    return jsonify({'status': 'success', 'value': '',
                    'message': 'New activities created!'})


# Get activities for a league
def get_activities_league(league_id):
    return Activity.query.filter_by(league_id=league_id).all()


# Get activities for a league url
@mod_league.route('/<league_id>/activities', methods=['GET'])
def get_activities_league_url(league_id):
    all_activities_league = get_activities_league(league_id)
    result = activities_schema.dump(all_activities_league)
    message = '' if len(
        result) > 0 else 'This league does not have any activities'
    return jsonify({'status': 'success', 'value': result, 'message': message})


def get_members_league(league_id, inside_league=True):
    # members outside of selected league
    if (inside_league == 'false'):
        return Member.query.join(
            League, ~Member.leagues.any(league_id=league_id)).all()
    # members inside of selected league
    else:
        return Member.query.join(
            League, Member.leagues.any(league_id=league_id)).all()


# Get members for a league
@mod_league.route('/<league_id>/members', methods=['GET'])
def get_members_league_url(league_id):
    all_members_league = get_members_league(league_id, request.args.get('in'))
    result = members_schema.dump(all_members_league)
    message = '' if len(
        result) > 0 else 'No members found for this request'
    return jsonify({'status': 'success', 'value': result, 'message': message})


# Get Season for a League
@mod_league.route('/<league_id>/seasons', methods=['GET'])
def get_season_league(league_id):
    active_season = Season.query.filter_by(
        league_id=league_id).first()
    result = season_schema.dump(active_season)
    message = 'Successfully received season for league {}'.format(league_id)
    return jsonify({'status': 'success', 'value': result, 'message': message})

# Activate Season for a League
@mod_league.route('/<league_id>/seasons/activate', methods=['POST'])
def activate_season_league(league_id):
    season = Season.query.filter_by(league_id=league_id).first()
    if not season.disabled:
        return jsonify({'status': 'failed', 'value': '', 'message': 'Season in league {} already activated'.format(league_id)})
    season.disabled = False
    create_weeks(season.id, season.weeks_number, league_id)
    db.session.commit()
    return jsonify({'status': 'success', 'value': '', 'message': 'Season in league {} activated'.format(league_id)})


# Deactivate Season for a League
@mod_league.route('/<league_id>/seasons/deactivate', methods=['POST'])
def deactivate_season_league(league_id):
    season = Season.query.filter_by(league_id=league_id).first()
    season.disabled = True
    delete_weeks(season.id)
    db.session.commit()
    return jsonify({'status': 'success', 'value': '', 'message': 'Season in league {} deactivated'.format(league_id)})


# Update Season for a League
@mod_league.route('/<league_id>/seasons', methods=['POST'])
def update_season_league(league_id):
    weeks_number = request.json['weeks_number']
    start_date = request.json['start_date']
    disabled = True

    season_exists = Season.query.filter_by(
        league_id=league_id).scalar() is not None
    if not season_exists:
        new_season = Season(league_id, weeks_number, disabled, start_date)
        db.session.add(new_season)
    else:
        season = Season.query.filter_by(
            league_id=league_id).first()
        season.weeks_number = weeks_number
        season.start_date = start_date
        season.disabled = disabled
    db.session.commit()
    return jsonify({'status': 'success', 'value': '',
                    'message': 'Season updated!'})


# Create Weeks for a Season
def create_weeks(season_id, weeks_number, league_id):
    week_exists = Week.query.filter_by(
        season_id=season_id).scalar() is not None
    if week_exists:
        return
    for index in range(weeks_number):
        new_week = Week(season_id, index)
        db.session.add(new_week)
        # get activities for the weeks
        league_activities = get_activities_league(league_id)
        # get members for the weeks
        league_members = get_members_league(league_id)
        # add member activity week to each of the new weeks for each member
        for activity in league_activities:
            for member in league_members:
                member_activity_week = Week.query.filter(Week.member_activity_week.any(
                    member_id=member.id, activity_id=activity.id, week_id=new_week.id)).scalar() is not None
                if not member_activity_week:
                    new_member_activity_week = Member_activity_week(
                        member.id, activity.id, new_week.id)
                    db.session.add(new_member_activity_week)
    db.session.commit()


# Delete Weeks for a Seasons
def delete_weeks(season_id):
    Week.query.filter_by(season_id=season_id).delete()


# Get Activities for a Week for a Season
@mod_league.route('/<league_id>/seasons/<season_id>/weeks/<week_id>/activities', methods=['POST'])
def get_activities_week(league_id, season_id, week_id):
    member_id = request.json['member_id']
    activities_member_week = []
    # get activities from a league
    activities = Activity.query.filter_by(league_id=league_id).all()
    for activity in activities:
        # get activities for a week
        member_activity_week = Member_activity_week.query.filter_by(
            member_id=member_id, activity_id=activity.id, week_id=week_id).first()
        activity_member_week = {
            "id": activity.id,
            "name": activity.name,
            "points": activity.points,
            "count": member_activity_week.activity_count,
            "total": member_activity_week.activity_total
        }
        activities_member_week.append(activity_member_week)
    return jsonify({'status': 'success', 'value': activities_member_week,
                    'message': 'Member Activities Week list received!'})


# Update value for Member_activity_week
@mod_league.route('/<league_id>/seasons/<season_id>/weeks/<week_id>/activities/<activity_id>', methods=['POST'])
def update_activity_week(league_id, season_id, week_id, activity_id):
    member_id = request.json['member_id']
    activity_count = request.json['count']
    activity_total = request.json['total']
    member_activity_week = Member_activity_week.query.filter_by(
        member_id=member_id, activity_id=activity_id, week_id=week_id).first()
    member_activity_week.activity_count = activity_count
    member_activity_week.activity_total = activity_total
    db.session.commit()
    return jsonify({'status': 'success', 'value': '',
                    'message': 'Member Activity updated!'})
