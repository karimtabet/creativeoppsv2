import json
import urlopen

from app.app import db
from app.models import Image


def get_pictures(album_id, project_uuid):
    thumbnail_url = ''
    image_url = ''
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
                image_url = line['source']

            if image_url and image_url != last_picture:
                last_picture = image_url
                image = Image(thumbnail_url=thumbnail_url,
                              image_url=image_url,
                              project_uuid=project_uuid)
                db.session.add(image)
    db.session.commit()
