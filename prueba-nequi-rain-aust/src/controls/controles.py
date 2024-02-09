import pandas as pd
from datetime import datetime
from src.data_get.make_dataset import TrerData
import logging

class Controls():
    def __init__(self, params, tipo):
        td = TrerData()
        if(tipo == "train"):
            self.df = td.data_proce()
            logging.basicConfig(filename=params.get("ruta_logs") + "\\archivo_controls_{}".format(datetime.now().strftime('%Y-%m-%d')) + ".log", level=logging.INFO)
        else:
            self.df = td.data_proce_inf()
            logging.basicConfig(filename=params.get("ruta_logs") + "\\archivo_controls_inf_{}".format(datetime.now().strftime('%Y-%m-%d')) + ".log", level=logging.INFO)
        logging.info(self.__validate_duplicate())
        logging.info(self.__null_values())
        logging.info(self.__num_columns())
        logging.info(self.__otuliers())
        logging.info(self.__cardinalidad())

    def __validate_duplicate(self):
        print("Duplicados")
        registros_duplicados = self.df.duplicated().sum()
        return "la cantidad de registros duplicados es {}".format(registros_duplicados)
    def __null_values(self):
        print("Nulos")
        cadena = ""
        porc_nulidad = 0
        for columna in self.df.columns:
            suma_nulos_columna = self.df[columna].isnull().sum()
            porcentaje_nulos_columna = (suma_nulos_columna / len(self.df)) * 100
            porc_nulidad = porcentaje_nulos_columna + porc_nulidad
            cadena = "Porcentaje de valores nulos en la columna {} es {} \n".format(columna, porcentaje_nulos_columna) + cadena
        if porc_nulidad == 0:
            text = "la nulidad es 0"
        else:
            text = cadena + "\ncontrol fallido"
        return text
    def __num_columns(self):
        print("Numero de columans")
        column = self.df.shape[1]
        return "El numero de columnas del dataframe es {}".format(column)
    def __otuliers(self):
        print("Outliers")
        text = ""
        for column in self.df.columns:
            if(self.df[column].max() == 1 or self.df[column].min() == 0):
                pass
            else:
                IQR = self.df[column].quantile(0.75) - self.df[column].quantile(0.25)
                rango_inferior = self.df[column].quantile(0.25) - (IQR * 1.5)
                rango_superior = self.df[column].quantile(0.75) + (IQR * 1.5)
                if self.df[column].max() > rango_superior or self.df[column].min() < rango_inferior:
                    text = "El limite superior para la variable {} es {} el inferior es {} se presentan outliers, valor mayor {}, valor menor {} \n".format(column, rango_superior, rango_inferior, self.df[column].max(), self.df[column].max() ) + text
        if text == "":
            return "No hay outliers"
        else:
            return text
    def __cardinalidad(self):
        print("Cardinalidad de variables")
        text = ""
        for columna in self.df.columns: #cardinalidad de variables
            text = 'columna {}: {} \n'.format(columna, self.df[columna].nunique()) + text
        return text

if __name__ == "__main__":
    data = pd.read_csv(r"D:\Prueba_ML\prueba-nequi-rain-aust\data\proccesed\data_model_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))
    Controls(data)
