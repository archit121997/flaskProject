import os
from datetime import date

from flask import Flask, flash, request, redirect, render_template
from script import *
from blob import *
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            today = date.today()
            date1 = today.strftime("%d%m%Y")

            #date = '20221301'

            myFileName = f'PPCT_Properties_{date1}.csv'

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], myFileName))

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], myFileName)

            noneExceptions = columnsWithNoneValues(file_path)



            parseExceptions = parseCSV(file_path)

            childPropertyException = startsWithP(file_path)

            dataTypeException = dataTypeValidation(file_path)

            #uploadToBlobStorage(file_path, myFileName )
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are csv')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = False)


