from src.data_get.make_dataset import TrerData
import os
import json
from datetime import datetime
from src.features.pipeline_preprocesado import *
from src.features.pipeline_inference import *
from src.controls.controles import *
from src.test.test_rain_aus_fun import *
from src.test.runner import *
from src.models.train_model import *
from src.models.inference import *

def main():
    path = r"D:\Prueba_ML\prueba-nequi-rain-aust\src\static\config.json"
    if os.path.exists(path):
        with open( path ) as f_in :
            json_str = f_in.read()
        cfg = json.loads(json_str)
    else:
        print("no existe")
    params = cfg.get('SetParams')
    process = [params.get("ruta_inference"), params.get("ruta_train")]

    td = TrerData()
    #inference
    if os.path.exists(process[0]):
        archivos = os.listdir(process[0])
        archivos_csv = [archivo for archivo in archivos if archivo.endswith('.csv')]
        if params.get("archivo") + "_{}".format(datetime.now().strftime('%Y-%m-%d')) + ".csv" in archivos_csv:
            pass
            #steps = [Transformations2.ejecutar(params), Controls(params, "test"), RunTest.ejecutar(params, "test"), InferenceStep().ejecutar(params)]

    #train
    if os.path.exists(process[1]):
        archivos = os.listdir(process[1])
        archivos_csv = [archivo for archivo in archivos if archivo.endswith('.csv')]
        if params.get("archivo") + "_{}".format(datetime.now().strftime('%Y-%m-%d')) + ".csv" in archivos_csv:
            pass
            steps = [transformations_1.ejecutar(params), Controls(params, "train"), RunTest.ejecutar(params, "train"), ModelTrain(params).train]

main()






