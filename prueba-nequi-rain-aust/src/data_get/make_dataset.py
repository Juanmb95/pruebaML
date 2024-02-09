from datetime import datetime
import pandas as pd
import os
import json

class TrerData:
    def __init__(self):
        path = r"D:\Prueba_ML\prueba-nequi-rain-aust\src\static\config.json"
        if os.path.exists(path):
            with open( path ) as f_in :
                json_str = f_in.read()
            cfg = json.loads(json_str)
        else:
            print("no existe")
        self.params = cfg.get('SetParams')
    def data(self, train, inference):
        if(inference == True):
            data = pd.read_csv(self.params.get("ruta_inference") + "\\" + self.params.get("archivo") + "_{}.csv".format(datetime.now().strftime('%Y-%m-%d')))
            return data
        if(train == True):
            data = pd.read_csv(self.params.get("ruta_train") + "\\" + self.params.get("archivo") + "_{}.csv".format(datetime.now().strftime('%Y-%m-%d')))
            return data
        else:
            return "No day datos disponibles"
    def data_proce(self):
        data = pd.read_excel(self.params.get("ruta_procesa") + "\\" + self.params.get("archivo_proces") + "_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))
        return data
    def data_proce_inf(self):
        data = pd.read_excel(self.params.get("ruta_procesa") + "\\" + self.params.get("archivo_proces_inf") + "_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))
        return data
