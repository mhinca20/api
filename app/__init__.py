import os,json,requests,sys,datetime,zipfile,glob
from subprocess import call
from flask import Flask, request, redirect, url_for, flash,send_from_directory,jsonify,make_response
from werkzeug.utils import secure_filename
from watson_developer_cloud import VisualRecognitionV3
import app.ibmClasificator as ibm
import app.simulIBM as ibms

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/home/user1/plantificator/testeo'
VIEW_FOLDER = '/home/user1/plantificator/output'
ZIP_FOLDER= '/home/user1/plantificator/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip'])
visual_recognition = VisualRecognitionV3(
        '2016-05-20',
        api_key="4893812447dc238483d5c01a41dfc798057baaeb")

app = Flask(__name__)
app.secret_key='tuCultivo'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIEW_FOLDER'] = VIEW_FOLDER
app.config['ZIP_FOLDER'] = ZIP_FOLDER
#Comprobar si el archivo tiene extencion valida                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#ruta para el inicio y para hacer el post con la imagen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        if file.filename =='':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['ZIP_FOLDER'], filename))
            zip_ref = zipfile.ZipFile(str(app.config['ZIP_FOLDER'])+'/'+file.filename, 'r')
            zip_ref.extractall('ensayo')
            zip_ref.close()
            files = glob.glob('ensayo/*')
            names=[]
            for file1 in files:
                if(os.path.isdir(file1)):
                    images = glob.glob('ensayo/' + file1.split("/")[-1] + '/*')
                    for image in images:
                        os.rename(image, str(app.config['UPLOAD_FOLDER'])+'/'+ image.split("/")[-1])
                        names.append(image.split("/")[-1])
                    os.rmdir('ensayo/' + file1.split("/")[-1])
            ################### POST PARA INFROMACION ###############################
            respo=requests.post("https://tucultivo.herokuapp.com/lots/"+request.form['lotid']+"/get_info",
                        data={},
                        headers={'Content-Type': 'application/json'}
                    )
            #print(list(respo.text))
            respo=eval(respo.text)
            farm=respo[0]["farm_id"]
            surcos=[]
            plantas=[]
            for i in respo[1]:
                surcos.append(i["id"])
                plantas.append(i["quantity"])
            #surcos=request.form['s'].split(',')
            #plantas=request.form['p'].split(',')
            print(farm,surcos,plantas)
            cont=0
            img=0
            namesN=[]
            for i in surcos:
                for j in range(int(plantas[cont])):
                    filenamen=str(farm)+'_'+request.form['lotid']+'_'+str(i)+'_'+str(j)+'.jpg'
                    namesN.append(filenamen)
                    print(filenamen+"oeeeeeeeeeeeee")
                    os.rename(str(app.config['UPLOAD_FOLDER'])+'/'+names[img],str(app.config['UPLOAD_FOLDER'])+'/'+filenamen)
                    img+=1
                cont+=1

            #ejecutar modelo ml pre procesamiento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            call(["python3.6","../plantificator/trashminator.py", "../plantificator"])
            #llamar a ibm para clasificar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            #results=ibm.ibmClasificator()
            results=ibms.simulIBM()
            #results=['conPlagas','conPlagas','conPlagas']
            ################# Borrar las imagenes de output para que no se llene la maquina                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            #try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            #    os.remove(VIEW_FOLDER+'/'+filename)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            #except: pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          \
            n=0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            for result in results:
                if result=='sinPlagas':
                    result=False
                else:
                    result=True
                    imginf=namesN[n].split("_")
                    now = datetime.datetime.now()
                    datenow=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
                    #enviar resultado a la pagina                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                    #print(request.form['identificador'])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                    r=requests.post("https://tucultivo.herokuapp.com/farms/"+imginf[0]+"/lots/"+imginf[1]+"/grooves/"+imginf[2]+"/plague_reports",
                                    data=json.dumps({
                                        'plague_report':{
                                            'reportDate':datenow
                                        },
                                'sick_plant':{'location':imginf[3].split('.')[0]}
                                    }),
                        headers={'Content-Type': 'application/json',
                                'X-USER-TOKEN': 'KsLvYG3EmNuBg58EbEh2etAC'
                            }
                    )
                print(result,namesN[n])
                n+=1
            return '''                                                                                                                                                                           
                        <!doctype html>
                        <title>tuCultivoApi</title>                                                                                                                                                          
                        las fotos del lote de su cultivo se subieron satisfactoriamente
                        <br>
                        </form>
                '''


    return '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    <!doctype html>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    <title>tuCultivoApi</title>                                                                                                                          
    <h1>Subir nuevas fotos del lote</h1>                                                                                                                            
    <form method=post enctype=multipart/form-data>
        IDENTIFICACION DEL LOTE:<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        <input type="text" name="lotid">                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        <p><input type=file name=file>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
           <input type=submit value=Subir>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    </form>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['VIEW_FOLDER'],
                               filename)
