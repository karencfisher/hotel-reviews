import json


def extractTripadvisor(raw_data):
    pass


sources = {"tripadvisor": {
        "URL": "https://api.content.tripadvisor.com/api/v1/",
        "template": "location/{location_no}/reviews?key={api_key}&language={language}",
        "api_key": "TRIPADVISOR_KEY",
        "extractor": extractTripadvisor
        }
    }

names = [key for key in sources.keys()]



