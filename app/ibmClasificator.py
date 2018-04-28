import json
import requests
import cv2
from watson_developer_cloud import VisualRecognitionV3
import os

############## creacion de objeto apra api de visual recognition de IBM ###############                                                                                                          
visual_recognition = VisualRecognitionV3(
        '2016-05-20',
        api_key="4893812447dc238483d5c01a41dfc798057baaeb")

############# Funcion para llamar al clasificador de ibm ############                                                                                                                            
def ibmClasificator(files):
        file_path = '/home/user1/plantificator/output/'+ files
        print(file_path)
        with open(file_path, 'rb') as images_file:
                classes = visual_recognition.classify(
                        images_file,
                        parameters=json.dumps({
                                'classifier_ids': ['pestsClasificator_501793644'],
                                'threshold': 0.6
                        }))
        #print(classes)                                                                                                                                                                          
        predict = classes["images"][0]["classifiers"][0]["classes"][0]["class"]
        return predict

########### posts de simulacion de sensores ####################                                                                                                                                 
#r = requests.post("https://tucultivo.herokuapp.com/sensors/?/values", data={"sensor": {"value": 27}})                                                                                           
#r2 = requests.post("https://tucultivo.herokuapp.com/sensors/?/values", data={"sensor": {"value": 28}})                                                                                          



