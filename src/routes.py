from flask import render_template, request, send_from_directory
from flask import current_app as app
import os
import shutil

upload_folder = './uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/')
def home():
    return render_template(
        'index.jinja2',
        title='Plotly Dash Flask Tutorial',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask."
    )

@app.route('/upload', methods=['POST'])
def upload_files():
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for key, file in request.files.items():
        if file:
            file.save(os.path.join(upload_folder, file.filename))

    return 'Files uploaded successfully', 200

@app.route('/delete-uploads')
def delete_uploads():
    uploads_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    
    if os.path.exists(uploads_folder):
        shutil.rmtree(uploads_folder)

    return 'Deleted successfully', 200

@app.route('/static')
def index():
    return send_from_directory(app.static_folder, 'index.jinja2')
