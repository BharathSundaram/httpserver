from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort
import os
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOADED_FILES_DEST'] = ''

def initprj( ptype="LDLY"):
    if ptype == "LDLY":
        app.config['UPLOADED_FILES_DEST'] = 'uploads'
        if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
            os.makedirs(app.config['UPLOADED_FILES_DEST'])

    elif ptype == "PDLY":
        app.config['UPLOADED_FILES_DEST'] = '/data/'

@app.route('/')
def index():
    files = []
    for filename in os.listdir(app.config['UPLOADED_FILES_DEST']):
        file_path = os.path.join(app.config['UPLOADED_FILES_DEST'], filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            last_modified_time = os.path.getmtime(file_path)
            last_modified_date = datetime.datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S')
            files.append({
                'name': filename,
                'size_mb': round(file_size, 2),
                'last_modified': last_modified_date
            })
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_FILES_DEST'], filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_from_directory(app.config['UPLOADED_FILES_DEST'], filename)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    initprj("LDLY")
    app.run(debug=True,host='0.0.0.0', port=8081)
