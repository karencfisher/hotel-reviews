import os
import sys
import time
import json
import logging
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime
import openai

sys.path.append('..')
try:
    from backend.DB.db import Database
except ModuleNotFoundError:
    from DB.db import Database


def get_completion(instructions, review):
    prompt = f"{instructions}/n==========/nReview text: '''{review}'''"
    message = [{'role': 'user', 'content': prompt}]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0,
        messages=message
    )
    output = {'content': response.choices[0].message['content'],
              'cost': response.usage['total_tokens'] / 1000 * 0.002}
    return output

def read_reviews(logger):
    total_cost = 0
    errors = False
    total_elapsed = 0

    # get openai API key
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_KEY')

    # get instructions for GPT
    instruct_path = os.path.join('backend', 'gpt-instructions.txt')
    with open (instruct_path, 'r') as FILE:
        instructions = FILE.read()

    # Get un-read reviews
    database = Database()
    sql = f'SELECT * FROM raw_reviews WHERE reviewed = {False}'
    reviews = list(database.query_sql(sql))
    count_reviews = len(reviews)
    logger.info(f'Reading {count_reviews} reviews.')
    
    for result in tqdm(reviews):
        # get fields from review
        review = {
            'review_id': result[0],
            'source_name': result[1],
            'category': result[3],
            'locations_location': result[2]
        }
        text = result[5] + ' ' + result[6]

        # get topics by category and fill in instructions
        sql = f'''SELECT topic_name FROM topics 
                  WHERE category = \"{review["category"]}\";'''
        topics = list(database.query_sql(sql))
        topic_list = [top[0] for top in topics]
        instruct = instructions.replace('%%topic_list%%', str(topic_list))

        # query ChatGPT to read review
        logger.info(f'Calling GPT to read review {result[1]} - {result[0]}')
        start = time.time()
        try:
            results_json = get_completion(instruct, text)
        except Exception as err:
            logger.error(f'ERROR : {str(err)}')
            errors = True
            break
        elapsed = time.time() - start
        total_elapsed += elapsed
        logger.info(f'Returned, took {elapsed: .2f} seconds')
        total_cost += results_json['cost']

        # update raw_review flag
        sql = f'''UPDATE raw_reviews SET reviewed = {True} 
        WHERE review_id = \"{review["review_id"]}\" AND 
              source_name = \"{review["source_name"]}\";'''
        result_update = database.update_sql(sql)
        if result_update is not None:
            logger.error(f'ERROR : {result_update}')
            errors = True
            break

        # insert reading results into cokked_reviews
        results = json.loads(results_json['content'])
        for topic in results.keys():
            review['topic_name'] = topic
            review['angry'] = results[topic]['Angry']
            review['sentiment'] = results[topic]['Sentiment']
            review['summary'] = results[topic]['Summary']
            result_insert = database.insert('cooked_reviews', review)
            if result_insert is not None:
                logger.error(f'ERROR: {result_insert}')
        logger.info(f'Completed {result[1]} - {result[0]}')
    avg_elapsed = total_elapsed / count_reviews
    if errors:
        logger.error('Incomplete. There was an error.')
        print('Incomplete, check log file for error')
    else:
        logger.info(f'All reviews read.')
    logger.info(f'Avg. elapsed time calling API {avg_elapsed: .2f} sconds')
    logger.info(f'Total API cost: ${total_cost: .4f}')


def main():
    now = datetime.now()
    logfile = f'read-log-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    log_path = os.path.join('backend', 'logs', logfile)
    logging.basicConfig(filename=log_path,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) 

    read_reviews(logger)             
        

if __name__ == '__main__':
    main()