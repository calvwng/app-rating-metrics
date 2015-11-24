from flask import Flask, g, request
from flask_restful import Resource, Api

import sqlite3
import collections, copy
import verbosity_agent, window_averager

DATABASE = 'reviews.db'

# Product ID -> name mapping
PID_TO_NAME = {
    "14831371782": "Textra SMS"
}


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

def arr_to_obj (arr):
    obj = collections.OrderedDict()
    obj['id'] = arr[0]
    obj['product'] = arr[1]
    obj['original_review'] = arr[2]
    obj['date'] = arr[3]
    obj['author'] = arr[4]
    obj['stars'] = arr[5]
    obj['version'] = arr[6]
    return obj

def get_words(reviews):
    all_words = []

    for result in reviews:
        all_words += result['original_review'].split()
        # set limit at 10,000 words for performance reasons
        if len(all_words) > 10000:
            return all_words
    return all_words

# Resource containing all app data
class AppRatings(Resource):


    def get(self):
        db_conn = get_db()
        c = db_conn.cursor()
        c.execute("SELECT DISTINCT product FROM REVIEW")
        db_results = c.fetchall()

        # Convert to objects with key-value pairs and return in results list
        results = []

        for row in db_results:
            obj = collections.OrderedDict()
            obj['product'] = row[0]
            # c.execute("SELECT name FROM APP WHERE id=?", (row[0],))
            # prod_name = c.fetchall()
            # obj['product_name'] = prod_name
            obj['product_name'] = PID_TO_NAME[str(row[0])]
            results.append(obj)

        db_conn.close()
        return results





class AppRating(Resource):
    def get(self, app_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_rating = request.args.get('min_rating')
        max_rating = request.args.get('max_rating')
        verbosity = request.args.get('verbosity')
        metric = request.args.get('metric')

        qry_str = "SELECT * FROM REVIEW WHERE product=? "
        ord_str = "ORDER BY date ASC "
        subst_tuple = [app_id]
        db_conn = get_db()
        c = db_conn.cursor()

        # Before anything else, must process ALL available reviews to derive verbosity scale
        if verbosity:
            c.execute(qry_str + ord_str, subst_tuple)
            objs = map(arr_to_obj, c.fetchall())
            # build histogram of ALL review word counts, regardless of other filtering parameters
            verbosity_agent.createHistogram(objs)
            # use built histogram to create verbosity scoring scale (ranges)
            verbosity_agent.createVerbosityScale()

        if start_date:
            qry_str += "AND date >= date(?) "
            subst_tuple.append(start_date)

        if end_date:
            qry_str += "AND date <= date(?) "
            subst_tuple.append(end_date)

        if min_rating:
            qry_str += "AND stars >= ? "
            subst_tuple.append(min_rating)

        if max_rating:
            qry_str += "AND stars <= ? "
            subst_tuple.append(max_rating)

        c.execute(qry_str + ord_str, subst_tuple)
        db_results = c.fetchall()

        # Convert array of arrays to dictionaries/objects with key-value pairs, and assign to 'reviews' key of results
        results = {'reviews': map(arr_to_obj, db_results)}

        # Now that results are filtered by other parameters, we can assign verbosity scores to results
        if verbosity:
            overall_verbosity_hist = copy.deepcopy(verbosity_agent.histogramlst) # Save deep copy of overall word count histogram
            verbosity_scale = copy.deepcopy(verbosity_agent.verbosityscoreslst)  # Save deep copy of overall verbosity scale
            verbosity_agent.assignVerbosityScores(results['reviews'])            # Assign the verbosity scores to results

            # Further filter results by given verbosity parameter
            verbose_objs = [obj for obj in results['reviews'] if obj['verbosity'] == int(verbosity)]

            verbosity_agent.reset()                                         # Reset verbosity agent before processing filtered results
            verbosity_agent.createHistogram(results['reviews'])                        # Create a new histogram using only filtered results
            filtered_verbosity_hist = verbosity_agent.histogramlst

            results['verbosity_scale'] = verbosity_scale                    # Include derived verbosity scale in results
            results['verbosity_hist'] = overall_verbosity_hist              # Include overall word count histogram
            results['verbosity_filtered_hist'] = filtered_verbosity_hist    # Include word count histogram for filtered results
            results['reviews'] = verbose_objs                                 # Include app review objects with verbosity scores
        elif metric == 'wordcloud':
            all_words = get_words(results['reviews'])
            all_words = all_words
            uniq_words = set(all_words)
            word_count = []
            for word in uniq_words:
                word_count.append([word, all_words.count(word)])
            results['word_count'] = word_count

        results['product_name'] = PID_TO_NAME[app_id]                       # Always include the product name
        results['win_avg_stars'] = window_averager.get_win_avgs(results['reviews'], 'stars', 0) # Windowed averages of original ratings

        db_conn.close()
        return results

# The Werkzeug routing system automatically orders routes by complexity
api.add_resource(AppRatings, '/apps/')
api.add_resource(AppRating, '/apps/<string:app_id>')

# Check to see if acting as main application or module

if __name__ == '__main__':
    app.run(debug=True) # Don't use debug in production environment
