#Instalar opencv en el servidor que usemos
import os,json,requests,sys
from subprocess import call
from flask import Flask, request, redirect, url_for, flash,send_from_directory,jsonify,make_response
from werkzeug.utils import secure_filename
from watson_developer_cloud import VisualRecognitionV3
#asi se hace un post desde consola
#curl -F "file=@/home/mhincapie/Imágenes/oe.png" http://127.0.0.1:8000/
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/home/user1/plantificator/testeo'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
visual_recognition = VisualRecognitionV3(
	'2016-05-20',
	api_key="4893812447dc238483d5c01a41dfc798057baaeb")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Comprobar si el archivo tiene extencion valida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#ruta para el inicio y para hacer el post con la imagen
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #No funciona en el momento el call porque el trashminator solo ejecuta desde la carpeta
			###ruta = ruta al directorio que contiene a trashmiantor.py
            call(["python3.6","../../plantificator/trashminator.py", " ../../plantificator/"])
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
#response example
#return make_response(jsonify({
#        'status': 'bien',
#        'message': 'message'
#    })), 200
