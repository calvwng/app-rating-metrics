from flask import Flask, g, request
from flask_restful import Resource, Api

import sqlite3
import json
import collections

DATABASE = 'reviews.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

"""
'A Python web app based on WSGI must have one central object implementing the app.
'With Flask Restful, this is an instance of the Flask class.
"""
app = Flask(__name__) # __name__ is the package name
api = Api(app)

# After each request (options) received, send back a response allowing cross origin
# This allows querying our API from any origin
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

# Resource containing all app data
class AppRatings(Resource):
    def get(self):
        db_conn = get_db()
        c = db_conn.cursor()
        c.execute("SELECT DISTINCT product FROM REVIEW")
        result = c.fetchall()

        # Convert to objects with key-value pairs
        objs = []

        for row in result:
            obj = collections.OrderedDict()
            obj['product'] = row[0]
            objs.append(obj)

        db_conn.close()
        return obj

# Resource containing app rating data for given app id
class AppRating(Resource):
    def get(self, app_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_rating = request.args.get('min_rating')
        max_rating = request.args.get('max_rating')
        verbosity = request.arg.get('verbosity')

        qryStr = "SELECT * FROM REVIEW WHERE product=? "
        subst_tuple = (app_id,)

        if (start_date):
           qryStr = qryStr + "AND date >= date(?) "
           subst_tuple = subst_tuple + (start_date,)

        if (end_date):
           qryStr = qryStr + "AND date <= date(?)"
           subst_tuple = subst_tuple + (end_date,)

        if (min_rating):
           qryStr = qryStr + "AND stars >= ? "
           subst_tuple = subst_tuple + (min_rating,)

        if (max_rating):
           qryStr = qryStr + "AND stars <= ? "
           subst_tuple = subst_tuple + (max_rating,)

        db_conn = get_db()
        # db_conn.row_factory = sqlite3.Row
        c = db_conn.cursor()
        c.execute(qryStr, subst_tuple)
        result = c.fetchall()

        # Convert to objects with key-value pairs
        objs = []

        for row in result:
            obj = collections.OrderedDict()
            obj['id'] = row[0]
            obj['product'] = row[1]
            obj['original_review'] = row[2]
            obj['date'] = row[3]
            obj['author'] = row[4]
            obj['stars'] = row[5]
            obj['version'] = row[6]
            objs.append(obj)

        if (verbosity):
            # TODO: use verbosity agent to process all reviews to build histogram of review word counts
            # TODO: use built histogram to assign verbosity scores to all reviews in result
            pass

        db_conn.close()
        return objs

# The Werkzeug routing system automatically orders routes by complexity
api.add_resource(AppRatings, '/apps')
api.add_resource(AppRating, '/apps/<string:app_id>')

# Check to see if acting as main application or module
if __name__ == '__main__':
    app.run(debug=True) # Don't use debug in production environment
