import json
import urlopen

from app import db
from app.models import Picture


def get_pictures(album_id, project_id):
    thumbnail_url = ''
    picture_url = ''
    last_picture = ''
    response = urlopen(
        "https://api.flickr.com/services/rest/" +
        "?method=flickr.photosets.getPhotos" +
        "&api_key=c5abbe4d732f631c72a743855fc5b47c&photoset_id=" +
        album_id + "&format=json&nojsoncallback=1"
      ).read()
    response_json = json.loads(response)
    for line in response_json['photoset']['photo']:
        photo_id = line['id']
        response = urlopen(
            "https://api.flickr.com/services/rest/" +
            "?method=flickr.photos.getSizes&" +
            "api_key=c5abbe4d732f631c72a743855fc5b47c&photo_id=" + photo_id +
            "&format=json&nojsoncallback=1"
        ).read()
        response_json = json.loads(response)
        for line in response_json['sizes']['size']:
            if line['label'] == 'Medium':
                thumbnail_url = line['source']
            if line['label'] == 'Original':
                picture_url = line['source']

            if picture_url and picture_url != last_picture:
                last_picture = picture_url
                picture = Picture(thumbnail_url=thumbnail_url,
                                  image_url=picture_url,
                                  project_id=project_id)
                db.session.add(picture)
    db.session.commit()
