import requests
from sqlalchemy.exc import IntegrityError

from app.app import app, db
from app.models import Image


def get_images_by_project(project_id):
    return db.session.query(Image).filter(
        Image.project_id == project_id
    ).all()


def get_flickr_images(album_id, project_id):
    flickr_api_key = app.config["FLICKR_API_KEY"]
    thumbnail_url = ''
    image_url = ''
    last_picture = ''
    album_response = requests.get(
        'https://api.flickr.com/services/rest/'
        '?method=flickr.photosets.getPhotos'
        '&api_key={api_key}'
        '&photoset_id={album_id}'
        '&format=json&nojsoncallback=1'
        .format(
            api_key=flickr_api_key,
            album_id=album_id
        )
      )
    for line in album_response.json()['photoset']['photo']:
        photo_id = line['id']
        image_response = requests.get(
            'https://api.flickr.com/services/rest/'
            '?method=flickr.photos.getSizes&'
            'api_key={api_key}'
            '&photo_id={photo_id}'
            '&format=json&nojsoncallback=1'
            .format(
                api_key=flickr_api_key,
                photo_id=photo_id
            )
        )
        for line in image_response.json()['sizes']['size']:
            if line['label'] == 'Medium':
                thumbnail_url = line['source']
            if line['label'] == 'Original':
                image_url = line['source']

            if image_url and image_url != last_picture:
                last_picture = image_url
                image = Image(thumbnail_url=thumbnail_url,
                              image_url=image_url,
                              project_id=project_id)
                try:
                    db.session.add(image)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    pass
