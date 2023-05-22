import os
import sys
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
    reviews = database.query_sql(sql)
    logger.info(f'Reading {len(reviews)} reviews.')

    for result in tqdm(reviews):
        # get fields from review
        review = {
            'review_id': result[0],
            'source_name': result[1],
            'locations_loaction': result[2],
            'category': result[3],
        }
        text = result[5] + ' ' + result[6]

        # get topics by category and fill in instructions
        sql = f'SELECT topic_name FROM topics WHERE category = {review["category"]}'
        topics = database.query_sql(sql)
        instruct = instructions.format(topics=topics)

        # query ChatGPT to read review
        try:
            results_json = get_completion(instruct, text)
        except Exception as err:
            logger.error(f'ERROR : {err}')
            break

        # update raw_review flag

        # insert reading results into cokked_reviews


def main():
    now = datetime.now()
    logfile = f'extract-log-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    log_path = os.path.join('backend', 'logs', logfile)
    logging.basicConfig(filename=log_path,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) 

    read_reviews(logger)             
        

if __name__ == '__main__':
    main()