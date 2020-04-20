from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

import os

from ImageHandler import handle_json_files, handle_multiple_files, handle_url_files, gather_pics_urls

app = Flask(__name__, template_folder="../templates", static_folder='../static')

app.config['SECRET_KEY'] = 'sss'
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['png', 'jpg', 'jpeg'])

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


@app.route('/', methods=['GET', 'POST'])
def index():
    pics = gather_pics_urls()
    return render_template('index.html', pics=pics)


@app.route('/upload', methods=['POST'])
def upload():
    json_request = False
    if request.get_json() is not None:
        json_request = True
        handle_json_files(request, app.config['UPLOADED_PHOTOS_DEST'])
    if not json_request and len(request.files.getlist('images')) > 0:
        handle_multiple_files(request, photos)
    if len(request.form) > 0:
        if len(request.form['image_url']) != 0:
            handle_url_files(request, app.config['UPLOADED_PHOTOS_DEST'])
    pics = gather_pics_urls()
    return render_template('index.html', pics=pics)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')