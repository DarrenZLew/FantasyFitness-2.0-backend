from app import app
from app.models import *
from flask import Blueprint
from flask import request, jsonify
from flask_login import LoginManager, login_user

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
mod_league = Blueprint('league', __name__, url_prefix='/league')
mod_activity = Blueprint('activity', __name__, url_prefix='/activity')

login_manager = LoginManager()
login_manager.init_app(app)


# Create a Member
@mod_auth.route('/signup', methods=['POST'])
def add_member():
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
@mod_auth.route('/member', methods=['GET'])
def get_members():
    all_members = Member.query.outerjoin(Member.leagues).all()
    result = members_schema.dump(all_members)
    return jsonify(result)


# Get Single Member
@mod_auth.route('/member/<id>', methods=['GET'])
def get_member(id):
    member = Member.query.get(id)
    return member_schema.jsonify(member)


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
        new_member_league = Member_league(new_league.id, member_id, 'admin')
        db.session.add(new_member_league)
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
@mod_league.route('/member/<member_id>', methods=['GET'])
def get_leagues_member(member_id):
    all_member_leagues = League.query.filter(League.members.any(member_id=member_id)).all()
    result = leagues_schema.dump(all_member_leagues)
    message = '' if len(result) > 0 else 'No leagues are currently available'
    return jsonify({'status': 'success', 'value': result, 'message': message})

# Get Single League
@mod_league.route('/<league_id>', methods=['GET'])
def get_league(league_id):
    league = League.query.get(league_id)
    return league_schema.jsonify(league)

# @mod_league.route('/<id>', methods=["PUT"])
# def update_league(id):
#     league = League.query.get(id)



# Update a Product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#   product = Product.query.get(id)

#   name = request.json['name']
#   description = request.json['description']
#   price = request.json['price']
#   qty = request.json['qty']

#   product.name = name
#   product.description = description
#   product.price = price
#   product.qty = qty

#   db.session.commit()

#   return product_schema.jsonify(product)

# Delete Product
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id):
#   product = Product.query.get(id)
#   db.session.delete(product)
#   db.session.commit()

#   return product_schema.jsonify(product)    

# Add an activity to a league
# @mod_activity.route('', methods=['POST'])
# def add_activities():
#     activities = request.json['activities']
#     league_id = request.json['league_id']


# def add_activity(fields):
#     # add try catch for if one of these was not found correctly
#     name = fields['name']
#     points = fields['points']
#     bonus = fields['bonus']
#     league_id = fields['league_id']

#     new_activity = Activity(league_id, points, name, bonus)

#     db.session.add(new_activity)
#     db.session.commit()

    # return jsonify({'status': 'success', 'value': league_data,
    #                 'message': 'New league {} created!'.format(league_data["name"])})
