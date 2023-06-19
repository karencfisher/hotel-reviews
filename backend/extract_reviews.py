import logging
import os
import sys
from tqdm import tqdm
from datetime import datetime


sys.path.append('..')
try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database

try:
    import backend.reviews_api as src
except ModuleNotFoundError:
    import reviews_api as src


def fetch_reviews(logger):
    database = Database()

    # get sources
    sources = database.query('sources')
    for source in sources:
        language = source['source_language']
        source_info = src.sources[source['source_name']]
        extractor_class = source_info['extractor']
        print(f'Calling {source["source_name"]}...')

        # get locations
        results = database.query('locations')
        print(f'Making requests for reviews for {len(results)} locations...')

        for result in tqdm(results):
            new_count, repeat_count = 0, 0
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
                if insert_result is not None and insert_result != 'duplicate':
                    logger.error(f'ERROR\n{insert_result}')
                elif insert_result == 'duplicate':
                    repeat_count += 1
                else:
                    new_count += 1
            logger.info(f'{repeat_count} duplicates {new_count} new reviews found.')
                        
def main():
    now = datetime.now()
    logfile = f'extract-log-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    log_path = os.path.join('backend', 'logs', logfile)
    logging.basicConfig(filename=log_path,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) 

    fetch_reviews(logger)             
        

if __name__ == '__main__':
    main()







