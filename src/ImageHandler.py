import base64
import os
from urllib.request import urlretrieve
'''
This module handles routines with image data
POSTed via request with three options:
- load form-data,
- JSON base64 coded image
- image from URL source
'''


def handle_multiple_files(request, photos):
    files = request.files.getlist('images')
    # list to hold our uploaded image urls
    for f in files:
        if len(f.filename) > 0:  # in case empty submission was made
            photos.save(
                f,
                name=f.filename
            )


def handle_json_files(request, upload_path):
    imgstring = request.get_json()['photo']
    imgdata = base64.b64decode(imgstring)
    filename = 'base64_image.jpg'  # I assume you have a way of picking unique filenames
    with open(os.path.join(upload_path, filename), 'wb') as f:
        f.write(imgdata)


def handle_url_files(request, upload_path):
    url = request.form['image_url']
    urlretrieve(url, os.path.join(upload_path, str(url).split('/')[-1]))


def gather_pics_urls():
    pics = os.listdir('static/')
    for i in range(len(pics)):
        pics[i] = os.path.join('../static/', pics[i])
    return pics