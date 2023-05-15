import logging
import os
import sys

sys.path.append('..')
try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database

import sources as src


def fetch_reviews(logger):
    database = Database()

    # get sources
    sources = database.query('sources')
    for source in sources:
        language = source['source_language']
        source_info = src.sources[source['source_name']]
        extractor_class = source_info['extractor']

        # get locations
        results = database.query('locations')

        for result in results:
            extractor = extractor_class(logger, 
                                        result['locations_location'], 
                                        result['category'],
                                        result['source_name'], 
                                        language)
            reviews = extractor.query()

            if reviews[0] != 200:
                continue

            for review in reviews[1]:
                insert_result = database.insert('raw_reviews', review)
                if insert_result is None or insert_result == 'duplicate':
                    continue
                else:
                    logger.error(f'ERROR\n{insert_result}')
                        

def main():
    log_path = os.path.join('backend', 'logs', 'extract.log')
    logging.basicConfig(filename=log_path,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) 

    fetch_reviews(logger)             
        

if __name__ == '__main__':
    main()







