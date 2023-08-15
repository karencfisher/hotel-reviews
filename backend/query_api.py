
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

# get location descriptions
@app.route('/api/v1.0/get_places')
def get_places():
    sql = '''
    SELECT DISTINCT location_description FROM locations
    '''
    results = db.query_sql(sql)
    output = {'places': [row[0] for row in results]}
    return jsonify(output)

# get 'cooked' reviews by conditions
@app.route('/api/v1.0/query_reviews')
def query_reviews():
    where_clause, limit_clause = query_utils.build_where_clause(request.args)
    sql = f'''
    SELECT r.topic_name, l.location_description, r.summary, r.sentiment, 
    r.angry, r.review_id, raw.pub_date, r.source_name
    FROM cooked_reviews AS r
    JOIN locations as l
    ON r.source_name = l.source_name AND  r.locations_location = l.locations_location
    JOIN raw_reviews as raw
    ON raw.review_id = r.review_id
    {where_clause}
    {limit_clause};
    '''

    try:
        results = db.query_sql(sql)
        output = []
        for row in results:
            output.append(
                {'topic': row[0],
                'place': row[1],
                'summary': row[2],
                'sentiment': row[3],
                'angry': row[4],
                'review_id': row[5],
                'pub_date': row[6],
                'review_source': row[7]
                }
            )
        final_output = query_utils.make_review_report(output)
    except Exception as ERR:
        return jsonify({'response': 500, 'error': str(ERR)}), 500
    return final_output


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

    try:
        result = list(db.query_sql(sql))[0]
        output = {'title': result[0],
                'property': result[1],
                'review': result[2],
                'customer_rating': result[3]}
    except Exception as ERR:
        return jsonify({'response': 500, 'error': str(ERR)}), 500
    return jsonify(output)


# get stats on sentiments by topics in selected range
@app.route('/api/v1.0/query_stats')
def query_stats():
    where_clause, limit_clause = query_utils.build_where_clause(request.args)
    sql = f'''
    SELECT r.topic_name, r.sentiment
    FROM cooked_reviews AS r
    JOIN locations as l
    ON r.source_name = l.source_name AND  r.locations_location = l.locations_location
    JOIN raw_reviews as raw
    ON raw.review_id = r.review_id
    {where_clause} 
    {limit_clause}
    '''

    try:
        results = list(db.query_sql(sql))
        output = defaultdict(list)
        for row in results:
            output[row[0]].append(row[1])
    except Exception as ERR:
        return jsonify({'response': 500, 'error': str(ERR)}), 500
    return jsonify(output)


# conversational agent
@app.route('/api/v1.0/ai_agent')
def ai_agent():
    where_clause = query_utils.build_where_clause(request.args)


def main():
    app.run(port=5005, debug=True)

if __name__ == '__main__':
    main()
