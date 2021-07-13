<img src="https://www.bit01.de/wp-content/uploads/2021/03/youtube_mining_logo.png" height="60" />

# Youtube Mining
A simple client for mining YouTube Trend data.

Systems:
* MongoDB (on host or extern)
* Mongo Express (optional)
* Python-Client

# Installation

## Docker

1. Add your API Key and Mongo credentials.
2. Install docker-compose
3. Do command:
```sudo docker-compose up -d```

If you want to shutdown the service only type:
```sudo docker-compose down```

## Local

1. Only put your MongoDB settings to sample.env and rename it to .env.
2. Install dependencies with pip ```pip install -r requirements.txt ```
3. Then run ```python src/main.py```

## On Raspberry pi

1. Clone this github repository to a folder (e.g. ```~/Programs/```)
2. Add it to crontabs for repeatly update ```crontab -e```
```*/1 * * * * python3 ~/Programs/youtube_mining/src/main.py >> ~/Programs/youtube_mining/output.log 2>&1```
3. Check output.log for output

To update the client, go to youtube_mining folder and type ```git pull```

# YouTube Trend Analysis

My finished analysis blog post comming soon!
