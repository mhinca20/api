import json
import requests
from watson_developer_cloud import VisualRecognitionV3
import os

############## creacion de objeto apra api de visual recognition de IBM ###############                                                                                                         \
                                                                                                                                                                                                 
visual_recognition = VisualRecognitionV3(
        '2016-05-20',
        api_key="4893812447dc238483d5c01a41dfc798057baaeb")

############# Funcion para llamar al clasificador de ibm ############                                                                                                                           \
result=[]                                                                                                                                                                                                 
def ibmClasificator():
        files_path = '/home/user1/plantificator/output/'
        for files in os.listdir(files_path):
                file_path = files_path+ files
                print(file_path)
                with open(file_path, 'rb') as images_file:
                        classes = visual_recognition.classify(
                                images_file,
                                parameters=json.dumps({
                                        'classifier_ids': ['pestsClasificator_501793644'],
                                        'threshold': 0.6
                                }))
                #print(classes)                                                                                                                                                                         \
                                                                                                                                                                                                        
                predict = classes["images"][0]["classifiers"][0]["classes"][0]["class"]
                result.append(predict)
        return result

########### posts de simulacion de sensores ####################                                                                                                                                \
                                                                                                                                                                                                 
#r = requests.post("https://tucultivo.herokuapp.com/sensors/?/values", data={"sensor": {"value": 27}})                                                                                          \
                                                                                                                                                                                                 
#r2 = requests.post("https://tucultivo.herokuapp.com/sensors/?/values", data={"sensor": {"value": 28}})                                                                                         \
  