import sys
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
try:
    from backend.setup.setup import Setup
except ModuleNotFoundError:
    from setup.setup import Setup


app = Flask(__name__)
CORS(app)
setup = None

# Setup routes
@app.route('/')
def hello():
    return 'GO AWAY'

@app.route('/api/v1.0/setup/get_topics')
def get_topics():
    results = setup.get_info('topics')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_topic', methods=['POST'])
def add_topic():
    info = {'topic': request.form.get('topic_name')}
    result = setup.add_info('topics', info)
    if result is not None:
        return jsonify(result), 400
    return jsonify('success'), 200

@app.route('/api/v1.0/setup/get_sources')
def get_sources():
    results = setup.get_info('sources')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_source', methods=['POST'])
def add_sources():
    info = {'source_name': request.form.get('source_name'),
            'source_URL': request.form.get('source_URL'),
            'template':request.form.get('template'),
            'location': request.form.get('location'),
            'api_key': request.form.get('api_key')}
    
    result = setup.add_info('sources', info)
    if result is not None:
        return jsonify(result), 400

    with open ('.env', 'a') as FILE:
        FILE.write(f"\n{request.form.get('api_key')} = \'{request.form.get('api_key_val')}\'")   
    return jsonify('success'), 200

@app.route('/api/v1.0/setup/get_locations')
def get_locations():
    results = setup.get_info('locations')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_location', methods=['POST'])
def add_location():
    info = {'source_name': request.form.get('source_name'),
            'locations_location': request.form.get('locations_location')}
    
    results = setup.get_info('sources')
    sources = [src['source_name'] for src in results]
    if not info['source_name'] in sources:
        return jsonify(f'Source_name \'{info["source_name"]}\' not found!'), 400

    result = setup.add_info('locations', info)
    if result is not None:
        return jsonify(result), 400
    return jsonify('success'), 200


def main():
    global setup
    rebuild = False
    if len(sys.argv) > 1:
        rebuild = sys.argv[1] == '--rebuild'

    setup = Setup(rebuild=rebuild)
    app.run(port=5000, debug=True)

if __name__ == '__main__':
    main()
