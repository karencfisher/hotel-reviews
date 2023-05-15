import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime as dt


class BaseExtractor:
    def __init__(self, logger, location, category, api_name, language):
        self.logger = logger
        self.source = sources[api_name]
        self.location = location
        self.language = language
        self.api_name = api_name
        self.category = category

        load_dotenv()
        self.api_key = os.getenv(self.source['api_key'])

    def query(self):
        self.logger.info(f'Begin {self.api_name} {self.location} {self.language}')
        query = self.encode(location_no=self.location, 
                            api_key=self.api_key, 
                            language=self.language)
        try:
            url = self.source['URL'] + query
            self.logger.info(f'GET request {url}')
            response = requests.get(url)
        except Exception as err:
            self.logger.error(f'ERROR \n{err}')
            return 500, None
        if response.status_code != 200:
            self.logger.error(f'Response with error {response.status_code}')
            return response.status_code, None
        else:
            self.logger.info(f'Response OK {response.status_code}')
            data = self.extract(response.json()['data'])
            return response.status_code, data
        
    def encode(self, location_no, api_key, language):
        pass
    
    def extract(self, data):
        pass


class TripadvisorExtractor(BaseExtractor):
    def __init__(self, logger, location, api_name, language):
        super(TripadvisorExtractor, self).__init__(logger, 
                                                   location, 
                                                   api_name, 
                                                   language)
        
    def encode(self, location_no, api_key, language):
        return f'location/{location_no}/reviews?key={api_key}&language={language}'
    
    def extract(self, data):
        reviews = []
        for row in data:
            review = {
                'review_id': int(row['id']),
                'source_name': self.api_name,
                'category': self.category,
                'pub_date': dt.fromisoformat(row['published_date'][:-1]),
                'title': row['title'],
                'review_text': row['text'],
                'rating': row['rating']
            }
            reviews.append(review)
        return reviews



sources = {"tripadvisor": {
        "URL": "https://api.content.tripadvisor.com/api/v1/",
        "api_key": "TRIPADVISOR_KEY",
        "extractor": TripadvisorExtractor
        }
    }

names = [key for key in sources.keys()]



