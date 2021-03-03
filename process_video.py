import datetime as dt
from mongo_video import MongoVideo, VersionEntry

def save_to_db(collection, data):

    for rank, video in enumerate(data['items']):

        id = video.get('id')
        snippet = video.get('snippet')
        statistics = video.get('statistics')
        content_details = video.get('contentDetails')
        title = snippet.get('title')
        channel = snippet.get('channelTitle')
        channel_id = snippet.get('channelId')
        category = snippet.get('categoryId')
        description = snippet.get('description')
        likes = int(statistics.get('likeCount')) if statistics.get('likeCount') else None
        dislikes = int(statistics.get('dislikeCount')) if statistics.get('dislikeCount') else None
        comments = int(statistics.get('commentCount')) if statistics.get('commentCount') else None
        views = int(statistics.get('viewCount'))
        duration = parse_isoduration(content_details.get('duration'))
        audio_language = snippet.get('defaultAudioLanguage')
        text_language = snippet.get('defaultLanguage')
        caption = True if content_details.get('caption') == "true" else False
        licensed_content = content_details.get('licensedContent')
        projection = content_details.get('projection')
        published_at = snippet.get('publishedAt')
        rank = rank+1
        tags = snippet.get('tags')

        item = collection.find_one({"_id": id})

        if item is None:
            # Video ist neu und existiert noch nicht.

            new_video = MongoVideo(
                _id = id,
                created = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                published_at = published_at,
                modified_at = dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                channel = channel,
                channel_id = channel_id,
                category = category,
                description = [version_entry(value=description)],
                likes = [version_entry(value=likes)],
                dislikes = [version_entry(value=dislikes)],
                comments = [version_entry(value=comments)],
                views = [version_entry(value=views)],
                duration = duration,
                audio_language = audio_language,
                text_language = text_language,
                caption = caption,
                licensed_content = licensed_content,
                projection = projection,
                rank = [version_entry(value=rank)],
                title = [version_entry(value=title)],
                tags = [version_entry(value=tags)]
            )

            collection.insert_one(new_video.dict(by_alias=True))
        else:
            # Variables for version changes...
            values = ['tags', 'title','rank','likes','dislikes','comments','views']

            for value_name in values:
                item = changes(eval(value_name), item, value_name)

            query = { '_id': id }
            update = { '$set': item }
            collection.update_one(query, update, upsert=False)


def version_entry(value, version: int = 1, date = None):
    if date is None:
        date = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return VersionEntry(
        version = version,
        value = value,
        date = date
    )

def changes(video_value, item, value_name: str):
    lastValues = item.get(value_name)[-1]
    actualValues = video_value
    if (lastValues.get('value') != actualValues):
        item.get(value_name).append(
                version_entry(
                    version=lastValues.get('version')+1,
                    value=actualValues
                ).dict()
            )
    #return modified item
    return item

def get_isosplit(s, split):
    if split in s:
        n, s = s.split(split)
    else:
        n = 0
    return n, s


def parse_isoduration(s):
        
    # Remove prefix
    s = s.split('P')[-1]
    
    # Step through letter dividers
    days, s = get_isosplit(s, 'D')
    _, s = get_isosplit(s, 'T')
    hours, s = get_isosplit(s, 'H')
    minutes, s = get_isosplit(s, 'M')
    seconds, s = get_isosplit(s, 'S')

    # Convert all to seconds
    seconds = dt.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return int(seconds.total_seconds())