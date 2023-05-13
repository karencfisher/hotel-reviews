import os
import json
import requests
import logging
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from sqlalchemy import insert

try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database

import sources as src


class Extract:
    def __init__(self):
        self.database = Database()
        load_dotenv()
        logging.basicConfig(filename="exytract.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')

    def fetch_reviews(self):
        logger = logging.get_logger()
        logger.setLevel(logging.INFO)

        # get sources
        sources = self.database.query('sources')
        for source in sources:
            language = source['source_language']

            source_info = src.sources[source['source_name']]
            URL = source_info['URL']
            api_key = source_info['api_key']
            template = source_info['template']
            extract_func = source_info['extractor']

            # get locations
            sql = f'''
            SELECT locations_location FROM locations
            WHERE source_name = {source['source_name']}
            '''
            results = self.database.query_sql(sql)
            locations = [result for result in results]
            
            for location in locations:
                query = source['template'].format(location_no=location, 
                                                  api_key=os.getenv(api_key), 
                                                  language=language)
                response = requests.get(source['source_URL'] + query)
                if response.status_code != 200:
                    logger.error(f'Request {source["source_name"]}: {location} -- {response.status_code}')
                    continue
                else:
                    logger.info(f'Request {source["source_name"]}: {location} -- 200')
                    data = extract_func(response.json)
        








