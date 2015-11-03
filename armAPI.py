from flask import Flask
from flask_restful import Resource, Api

"""
'A Python web app based on WSGI must have one central object implementing the app.
'With Flask Restful, this is an instance of the Flask class.
"""
app = Flask(__name__) # __name__ is the package name
api = Api(app)

# Resource containing all app rating data
class AppRatings(Resource):
    def get(self):
        return {"app1": {},
                "app2": {}}

# Resource containg app rating data for given app id
class AppRating(Resource):
    def get(self, app_id):
        return {"app_id": app_id,
                "rating": 0}

# The Werkzeug routing system automatically orders routes by complexity
api.add_resource(AppRatings, '/apps')
api.add_resource(AppRating, '/apps/<string:app_id>')

# Check to see if acting as main application or module
if __name__ == '__main__':
    app.run(debug=True) # Don't use debug in production environment
