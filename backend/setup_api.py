import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database

try:
    import backend.reviews_api as src
except ModuleNotFoundError:
    import reviews_api as src


app = Flask(__name__)
CORS(app)
db = None

# Setup routes
@app.route('/')
def hello():
    return 'GO AWAY'

@app.route('/api/v1.0/setup/get_topics')
def get_topics():
    results = db.query('topics')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_topic', methods=['POST'])
def add_topic():
    info = {
        'category': request.form.get('category'),
        'topic_name': request.form.get('topic_name')
    }
    result = db.insert('topics', info)
    if result is not None:
        return jsonify(result), 400
    return jsonify('success'), 200

@app.route('/api/v1.0/setup/get_sources')
def get_sources():
    results = db.query('sources')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_source', methods=['POST'])
def add_sources():
    source_name = request.form.get('source_name')
    if source_name not in src.names:
        return jsonify('No such review source'), 400
    
    info = {
        'source_name': source_name,
        'source_language':request.form.get('source_language')
    }
    result = db.insert('sources', info)
    if result is not None:
        return jsonify(result), 400
    
    api_key = src.sources[source_name]['api_key']
    key = os.getenv(api_key)
    if key is None or key != request.form.get('api_key_val'):
        with open ('.env', 'a') as FILE:
            FILE.write(f"\n{api_key} = \'{request.form.get('api_key_val')}\'")   
    return jsonify('success'), 200

@app.route('/api/v1.0/setup/get_locations')
def get_locations():
    results = db.query('locations')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_location', methods=['POST'])
def add_location():
    info = {
        'source_name': request.form.get('source_name'),
        'locations_location': request.form.get('locations_location'),
        'category': request.form.get('category'),
        'location_description': request.form.get('location_description')
    }
    
    results = db.query('sources')
    sources = [src['source_name'] for src in results]
    if not info['source_name'] in sources:
        return jsonify(f'Source_name \'{info["source_name"]}\' not found!'), 400
    
    results = db.query('topics')
    categories = [src['category'] for src in results]
    if not info['category'] in categories:
        return jsonify(f'Category \'{info["category"]}\' not found!'), 400

    result = db.insert('locations', info)
    if result is not None:
        return jsonify(result), 400
    return jsonify('success'), 200


def main():
    global db
    rebuild = False
    if len(sys.argv) > 1:
        rebuild = sys.argv[1] == '--rebuild'

    db = Database(rebuild=rebuild)
    app.run(port=5000, debug=True)

if __name__ == '__main__':
    main()
