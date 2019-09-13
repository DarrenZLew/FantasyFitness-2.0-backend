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

# Run Server
if __name__ == "__main__":
    app.run(debug=True)
