from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

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

from app.controllers import mod_auth, mod_league

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_league)

# # Create an Activity
# @app.route('/activity', methods=['POST'])
# def add_activity():
#     league_id = request.json['league_id']
#     points = request.json['points']
#     name = request.json['name']
#     bonus = request.json['bonus']
#     limit = request.json['limit']

#     new_activity = Activity(league_id, points, name, bonus, limit)

#     db.session.add(new_activity)
#     db.session.commit()

#     return activity_schema.jsonify(new_activity)

# # Get All Activities
# @app.route('/activity', methods=['GET'])
# def get_activities():
#     all_activities = Activity.query.all()
#     result = activities_schema.dump(all_activities)
#     return jsonify(result)

# # Get Single Activity
# @app.route('/activity/<id>', methods=['GET'])
# def get_activity(id):
#     activity = Activity.query.get(id)
#     return activity_schema.jsonify(activity)

# #################################################################



# # Create a Season
# @app.route('/season', methods=['POST'])
# def add_season():
#     league_id = request.json['league_id']
#     weeks = request.json['weeks']
#     disabled = False
#     start_date = request.json['start_date']

#     new_season = Season(league_id, weeks, disabled, start_date)

#     db.session.add(new_season)
#     db.session.commit()

#     return season_schema.jsonify(new_season)

# # Get All Seasons
# @app.route('/season', methods=['GET'])
# def get_seasons():
#     all_seasons = Season.query.all()
#     result = seasons_schema.dump(all_seasons)
#     return jsonify(result)

# # Get Single Season
# @app.route('/season/<id>', methods=['GET'])
# def get_a(id):
#     season = Season.query.get(id)
#     return season_schema.jsonify(season)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
