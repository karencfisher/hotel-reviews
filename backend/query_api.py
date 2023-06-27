import os
import sys
from collections import defaultdict
from flask import Flask, request, jsonify
from flask_cors import CORS
try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database
import query_utils


app = Flask(__name__)
CORS(app)
db = Database()

@app.route('/')
def hello():
    return 'You must be lost', 404

# get 'cooked' reviews by conditions
@app.route('/api/v1.0/query_reviews/')
def query_reviews():
    where_clause, limit_clause = query_utils.build_where_clause(request.args)
    sql = f'''
    SELECT r.topic_name, l.location_description, r.summary, r.sentiment
    FROM cooked_reviews AS r
    JOIN locations as l
    ON r.source_name = l.source_name AND  r.locations_location = l.locations_location
    {where_clause} {limit_clause};
    '''

    results = db.query_sql(sql)
    output = []
    for row in results:
        output.append(
            {'topic_name': row[0],
             'property': row[1],
             'summary': row[2],
             'sentiment': row[3]}
        )
    return jsonify(output)


# get a single full review by review_id
@app.route('/api/v1.0/query_review')
def query_review():
    review_id = request.args.get('review_id')
    sql = f'''
    SELECT r.title, l.location_description, r.review_text, r.rating
    FROM raw_reviews AS r
    JOIN locations as l
    ON r.source_name = l.source_name AND  r.locations_location = l.locations_location
    WHERE r.review_id = \"{review_id}\";
    '''

    result = list(db.query_sql(sql))[0]
    output = {'title': result[0],
              'property': result[1],
              'review': result[2],
              'customer_rating': result[3]}
    return jsonify(output)

@app.route('/api/v1.0/query_stats')
def query_stats():
    where_clause, limit_clause = query_utils.build_where_clause(request.args)
    sql = f'''
    SELECT rr.pub_date, cr.topic_name, cr.sentiment
    FROM cooked_reviews AS cr
    JOIN raw_reviews AS rr
    ON rr.review_id = cr.review_id AND rr.source_name = cr.source_name
    {where_clause}
    ORDER BY pub_date ASC
    {limit_clause}
    '''
    results = list(db.query_sql(sql))
    output = defaultdict(list)
    for row in results:
        output[row[1]].append(row[2])
    return jsonify(output)

# conversational agent
@app.route('/api/v1.0/ai_agent')
def ai_agent():
    pawhere_clause = query_utils.build_where_clause(request.args)


def main():
    app.run(port=5005, debug=True)

if __name__ == '__main__':
    main()
