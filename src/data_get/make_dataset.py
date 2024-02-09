from datetime import datetime
import pandas as pd
import os
import json
from src.config.get_r import *

class TrerData:
    def __init__(self):
        self.path = RutaT.get_folder()
        self.path_json = RutaT.get_folder() + "//src//static//config.json"
        if os.path.exists(self.path_json):
            with open( self.path_json, 'r' ) as f_in :
                json_str = f_in.read()
                cfg = json.loads(json_str)
        else:
            print("no existe")
        params = cfg.get('SetParams')
        self.params = params

    def data(self, train, inference):
        if(inference == True):
            data = pd.read_csv(self.path + self.params.get("ruta_inference") + "\\" + self.params.get("archivo") + "_{}.csv".format(datetime.now().strftime('%Y-%m-%d')))
            return data
        if(train == True):
            data = pd.read_csv(self.path + self.params.get("ruta_train") + "\\" + self.params.get("archivo") + "_{}.csv".format(datetime.now().strftime('%Y-%m-%d')))
            return data
        else:
            return "No day datos disponibles"
    def data_proce(self):
        data = pd.read_excel(self.path + self.params.get("ruta_procesa") + "\\" + self.params.get("archivo_proces") + "_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))
        return data
    def data_proce_inf(self):
        data = pd.read_excel(self.path + self.params.get("ruta_procesa") + "\\" + self.params.get("archivo_proces_inf") + "_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))
        return data
    def data_test_git(self):
        data = pd.read_csv(r"/home/runner/work/pruebaML/pruebaML/data/raw/weatherAUS_2024-02-09.csv".format(datetime.now().strftime('%Y-%m-%d')))
        #data = pd.read_csv("data/raw/weatherAUS_2024-02-09.csv")
        return data