import sys
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database


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
    info = {'topic_name': request.form.get('topic_name')}
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
    info = {'source_name': request.form.get('source_name'),
            'source_URL': request.form.get('source_URL'),
            'template': request.form.get('template'),
            'source_language':request.form.get('source_language'),
            'location': request.form.get('location'),
            'api_key': request.form.get('api_key')}
    
    result = db.insert('sources', info)
    if result is not None:
        return jsonify(result), 400

    with open ('.env', 'a') as FILE:
        FILE.write(f"\n{request.form.get('api_key')} = \'{request.form.get('api_key_val')}\'")   
    return jsonify('success'), 200

@app.route('/api/v1.0/setup/get_locations')
def get_locations():
    results = db.query('locations')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_location', methods=['POST'])
def add_location():
    info = {'source_name': request.form.get('source_name'),
            'locations_location': request.form.get('locations_location')}
    
    results = db.query('sources')
    sources = [src['source_name'] for src in results]
    if not info['source_name'] in sources:
        return jsonify(f'Source_name \'{info["source_name"]}\' not found!'), 400

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
