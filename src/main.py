import requests
import traceback
import datetime as dt
from pymongo import collection, MongoClient
from dotenv import load_dotenv
from process_video import save_to_db
from threading import Timer
import os

load_dotenv()
had_restart = False

def load_video_data(path) -> dict:
    params = {
        'part': 'snippet,contentDetails,statistics',
        'chart': 'mostPopular',
        'regionCode': os.environ.get('COUNTRY_CODE'),
        'maxResults': 50,
        'key': os.environ.get('YOUTUBE_API_KEY')
    }
    api_url = os.environ.get('API_BASE_URL') + path
    response = requests.get(api_url, params = params, timeout=10)
    return response.json()
    

def init_db() -> collection:
    client = MongoClient(
        host=os.environ.get('MONGO_HOST'),
        port=int(os.environ.get('MONGO_PORT')),
        username=os.environ.get('MONGO_USER'),
        password=os.environ.get('MONGO_PASSWORD'),
        maxPoolSize=50)
    collection = client['youtube_mining'][os.environ.get('DB_NAME')]
    return collection

def do(had_restart):
    # Repeat it every 60 seconds or with an cronjob.
    if (int(os.environ.get('REPEAT_MINUTE')) > 0):
        Timer(int(os.environ.get('REPEAT_MINUTE'))*60, do, [had_restart]).start()
    try:
        dateTimeObj = dt.datetime.now()
        timestampStr = dateTimeObj.strftime("[%d-%b-%Y %H:%M:%S]")

        collection = init_db()
        data = load_video_data('/videos')
        save_to_db(collection, data)
        print(timestampStr, "OK")
    except Exception as err:
        if not had_restart:
            dateTimeObj = dt.datetime.now()
            timestampStr = dateTimeObj.strftime("[%d-%b-%Y %H:%M:%S]")
            print(timestampStr, "Es ist ein Fehler aufgeretetn!")
            traceback.print_exc()
            had_restart = True

if __name__ == '__main__':
    do(had_restart)