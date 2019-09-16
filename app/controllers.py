from app import app, db
from app.models import Member, member_schema, members_schema
from flask import Blueprint
from flask import request, jsonify
from flask_login import LoginManager, login_user

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.init_app(app)

# Create a Member
@mod_auth.route('/signup', methods=['POST'])
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

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

# Login as Member
@mod_auth.route('/login', methods=['POST'])
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
