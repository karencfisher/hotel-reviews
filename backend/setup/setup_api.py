import os
import json
from flask import Flask, request, jsonify
from setup.setup import Setup


class SetupAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup = Setup()

        sources_path = os.path.join('backend', 'setup', 'sources.json')
        with open(sources_path, 'r') as FILE:
            sources = json.load(FILE)

        # Setup routes
        @self.app.route('/api/v1.0/setup/get_topics')
        def get_topics():
            results = self.setup.get_info('topics')
            return jsonify(results)

        @self.app.route('/api/v1.0/setup/add_topic', methods=['POST'])
        def add_topic():
            info = {'topic': request.form.get('topic_name')}
            self.setup.add_info('topics', info)
            return jsonify(message='success')

        @self.app.route('/api/v1.0/setup/get_sources')
        def get_sources():
            results = self.setup.get_info('sources')
            return jsonify(results)

        @self.app.route('/api/v1.0/setup/add_source', methods=['POST'])
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
            self.setup.add_info('sources', info)
            return jsonify(message='success')
        
    def start_service(self, port, url='127.0.0.1'):
        self.app.run(host=url, port=5000, debug=True)

    def stop_service(self):
        func = request.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not runnining Werkzeug Server')
        func()
