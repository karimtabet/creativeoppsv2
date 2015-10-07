from urllib import parse

from app import db
from app.models import Video


def get_videos(video_urls, project_id):
    for video_url in video_urls.split(','):
        video_url = video_url.strip()
        url_data = parse.urlparse(video_url)
        query = parse.parse_qs(url_data.query)
        video_id = query["v"][0]
        thumbnail_url = (
            'http://img.youtube.com/vi/' +
            video_id + '/default.jpg'
        )
        video = Video(video_url=video_url,
                      thumbnail_url=thumbnail_url,
                      project_id=project_id)
        db.session.add(video)
        db.session.commit()
