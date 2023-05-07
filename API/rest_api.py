import json
from flask import Flask, request, jsonify
from setup.setup import Setup


app = Flask(__name__)
setup = Setup()

with open('sources.json', 'r') as FILE:
    sources = json.load(FILE)

# Setup routes
@app.route('/api/v1.0/setup/get_topics')
def get_topics():
    results = setup.get_info('topics')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_topic', methods=['POST'])
def add_topic():
    info = {'topic': request.form.get('topic_name')}
    setup.add_info('topics', info)
    return jsonify(message='success')

@app.route('/api/v1.0/setup/get_sources')
def get_sources():
    results = setup.get_info('sources')
    return jsonify(results)

@app.route('/api/v1.0/setup/add_source', methods=['POST'])
def add_sources():
    name = request.form.get('name')
    location = request.form.get('location')
    source = sources.get('name')
    if source is None:
        return jsonify(message='non-existent source', 
                       statusCode=400), 400
    info = {'name': name,
            'URL': source['URL'],
            'template': source['template'],
            'location': location,
            'api_key': source('api_key')}
    setup.add_info('sources', info)
    return jsonify(message='success')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()