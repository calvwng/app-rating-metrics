from flask import Flask, g, request
from flask_restful import Resource, Api

import sqlite3

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

#import sqllite

"""
'A Python web app based on WSGI must have one central object implementing the app.
'With Flask Restful, this is an instance of the Flask class.
"""
app = Flask(__name__) # __name__ is the package name
api = Api(app)

# Resource containing all app data
class AppRatings(Resource):
    def get(self):
        db_conn = get_db()
        c = db_conn.cursor()
        c.execute("SELECT DISTINCT product FROM REVIEW")
        result = c.fetchall()
        db_conn.close()
        return result

# Resource containg app rating data for given app id
class AppRating(Resource):
    def get(self, app_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_rating = request.args.get('min_rating')
        max_rating = request.args.get('max_rating')

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
        c = db_conn.cursor()
        c.execute(qryStr, subst_tuple)
        result = c.fetchall()
        db_conn.close()
        return result

# The Werkzeug routing system automatically orders routes by complexity
api.add_resource(AppRatings, '/apps')
api.add_resource(AppRating, '/apps/<string:app_id>')

# Check to see if acting as main application or module
if __name__ == '__main__':
    app.run(debug=True) # Don't use debug in production environment
