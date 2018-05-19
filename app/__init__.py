import os,json,requests,sys,datetime
from subprocess import call
from flask import Flask, request, redirect, url_for, flash,send_from_directory,jsonify,make_response
from werkzeug.utils import secure_filename
from watson_developer_cloud import VisualRecognitionV3
import app.ibmClasificator as ibm

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/home/user1/plantificator/testeo'
VIEW_FOLDER = '/home/user1/plantificator/output'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
visual_recognition = VisualRecognitionV3(
        '2016-05-20',
        api_key="4893812447dc238483d5c01a41dfc798057baaeb")

app = Flask(__name__)
app.secret_key='tuCultivo'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIEW_FOLDER'] = VIEW_FOLDER
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
            print('No file part')
            return redirect(request.url)
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        if file.filename =='':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #ejecutar modelo ml pre procesamiento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
            call(["python3.6","../plantificator/trashminator.py", "../plantificator"])
            #llamar a ibm para clasificar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
            result=ibm.ibmClasificator(filename)
            ################# Borrar las imagenes de output para que no se llene la maquina                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            #try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
            #    os.remove(VIEW_FOLDER+'/'+filename)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            #except: pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

            if result=='sinPlagas':
                result=False
            else:
                result=True
            print(result,filename)
            imginf=filename.split("_")
            now = datetime.datetime.now()
            datenow=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
            #enviar resultado a la pagina                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
            r=requests.post("https://tucultivo.herokuapp.com/farms/"+imginf[0]+"/lots/"+imginf[1]+"/grooves/"+imginf[2]+"/plague_reports",
                data=json.dumps({
                    'plague_report':{
                        'reportDate':datenow,
                        'result':result
                    }
                }),
                headers={'Content-Type': 'application/json',
                         'X-USER-TOKEN': 'KsLvYG3EmNuBg58EbEh2etAC'
                }
            )

            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    <!doctype html>
    <title>tuCultivoApi</title>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    <h1>Subir nueva foto</h1>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    <form method=post enctype=multipart/form-data> 
        <p><input type=file name=file>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            <input type=submit value=Subir>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    </form>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['VIEW_FOLDER'],
                               filename)
