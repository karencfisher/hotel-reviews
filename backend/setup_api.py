import os
import json
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
try:
    from backend.setup.setup import Setup
except ModuleNotFoundError:
    from setup.setup import Setup


app = Flask(__name__)
CORS(app)
setup = Setup()

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
    print('Route called')
    info = {'topic': request.form.get('topic_name')}
    result = setup.add_info('topics', info)
    if result is not None:
        return jsonify(result), 500
    return jsonify('success'), 200

@app.route('/api/v1.0/setup/get_sources')
def get_sources():
    results = setup.get_info('sources')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_source', methods=['POST'])
def add_sources():
    info = {'name': request.form.get('name'),
            'URL': request.form.get('URL'),
            'template':request.form.get('template'),
            'location': request.form.get('location'),
            'api_key': request.form.get('api_key')}
    
    result = setup.add_info('sources', info)
    if result is not None:
        return jsonify(result), 500

    with open ('.env', 'a') as FILE:
        FILE.write(f"\n{request.form.get('api_key')} = \'{request.form.get('api_key_val')}\'")   
    return jsonify('success'), 200

app.run(port=5000, debug=True)

