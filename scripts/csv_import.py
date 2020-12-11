import csv
import os
from urllib import parse

import httpx
from django.core.files import File

from DjangoBlog.settings import MEDIA_ROOT
from blog.models import BlogPost, UserModel


def get_image(url: str) -> bin:
    try:
        image = httpx.get(url)
        if image.status_code == 200:
            return image.content
        else:
            raise FileNotFoundError
    except Exception as e:
        print(f'Error {e} happened while downloading image')


def run():
    """
    CSV format:
    title, short_description, content, created_date, updated_date, thumbnail_image, author
    Assuming thumbnail_image is a URL of the image hosted on a server
    """
    with open('blog/import.csv') as file:
        csv_data = csv.reader(file)
        to_import_list = []
        for i, row in enumerate(csv_data):
            if i != 0 and len(row) == 7:
                has_thumbnail = False
                # image_path = ''
                image = get_image(row[5].strip())
                if image:
                    url = parse.urlsplit(row[5].strip())
                    image_path = os.path.join(MEDIA_ROOT, url.path.split('/')[-1])
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image)
                        has_thumbnail = True
                user, _ = UserModel.objects.get_or_create(username=row[6])
                to_import_list.append(
                    BlogPost(
                        title=row[0],
                        short_description=row[1],
                        content=row[2],
                        created_date=row[3],
                        updated_date=row[4],
                        thumbnail_image=File(open(image_path, 'rb')) if has_thumbnail else None,
                        author=user or None
                    )
                )

        BlogPost.objects.bulk_create(to_import_list)
