import os
import json
import requests
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert

try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database


class Extract:
    def __init__(self):
        self.database = Database()
        load_dotenv()

    def run(self):
        # get sources
        sources = self.database.query('sources')

        for source in sources:
            # get locations
            loc_obj = self.database.tables('locations')
            sql = f'''
            SELECT locations_location FROM locations
            WHERE source_name = {source['source_name']}
            '''
            results = self.database.query_sql(sql)
            locations = [result for result in results]
            
            for location in locations:
                query = source['template'].format(location_no=location, 
                                        api_key=os.getenv(source['api_key']), 
                                        language=source['source_language'])
                response = requests.get(source['source_URL'] + query)
                if response.status_code != 200:
                    pass
                else:
                    pass

            



