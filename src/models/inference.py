from sklearn.preprocessing import MinMaxScaler
import pickle
from src.features.pipeline_inference import *
from src.data_get.make_dataset import *
import pickle
from src.config.get_r import RutaT
import pandas as pd

# Cargar el modelo desde el archivo modelo.pkl
class InferenceStep:
    @staticmethod
    def ejecutar(params):
        with open(RutaT.get_folder() + params.get("ruta_models") + "\\sk_rain_model_{}.pkl".format(datetime.now().strftime('%Y-%m-%d')), 'rb') as file:
            model = pickle.load(file)
        td = TrerData()
        data = td.data_proce_inf()
        scaler = MinMaxScaler()
        data = scaler.fit_transform(data)
        resultado = model.predict(data)
        print("Resultado de la inferencia:", resultado)