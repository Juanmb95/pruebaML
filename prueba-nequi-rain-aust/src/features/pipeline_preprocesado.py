import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
import category_encoders as ce
from sklearn.preprocessing import FunctionTransformer
import pandas as pd
from datetime import datetime
from src.data_get.make_dataset import *

class transformations_1:

    def ejecutar(params):
        td = TrerData()
        data = td.data(inference = False, train = True)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.assign(month=data['Date'].dt.month, year=data['Date'].dt.year, day=data['Date'].dt.day).drop('Date', axis=1)
        custom_transformer = FunctionTransformer(transformations_1.delete_regis_vo)
        custom_transformer2 = FunctionTransformer(transformations_1.outliers_replace)
        custom_transformer3 = FunctionTransformer(transformations_1.one_hot_encoder)
        custom_transformer4 = FunctionTransformer(transformations_1.binary_encoder)
        custom_transformer5 = FunctionTransformer(transformations_1.vo_encoder)
        custom_transformer6 = FunctionTransformer(transformations_1.imputer_vars)
        #imputer = SimpleImputer(strategy='median')
        preprocesing = Pipeline(steps=[
            ("delete", custom_transformer),
            ("outliers", custom_transformer2),
            ("oneHot", custom_transformer3),
            ("binary", custom_transformer4),
            ("vo", custom_transformer5),
            ("imputer", custom_transformer6)
        ])
        #pipeline = make_pipeline(preprocessor)
        preprocesing.fit(data)
        data_out = preprocesing.transform(data)
        print(data_out)
        total_filas = len(data_out)
        indice_medio = total_filas // 4
        data_out = data_out.drop(data_out.index[indice_medio:])
        data_out.to_excel(params.get("ruta_procesa") + "\\" + "data_model_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))

    @staticmethod
    def delete_regis_vo(df):
        """
        Funcion que elimina los registros que tengan la vo nula
        """
        df = df.dropna(subset=['RainTomorrow'])
        return df
    @staticmethod
    def binary_encoder(df):
        """
        Funcion que codifica la columna RainToday en una codificacion binaria
        """
        encoder = ce.BinaryEncoder(cols=['RainToday'])
        df_decode = encoder.fit_transform(df)
        for col in encoder.get_feature_names_out():
            df.loc[:, col] = df_decode.loc[:, col]
        df.drop(columns= 'RainToday', inplace=True)
        return df
    @staticmethod
    def outliers_replace(df):
        """
        Este metodo busca los outliers de las columnas numericas con el metodo del rango intercurtilico, en caso de que algun valor
        sea detectado como un outlier se reemplaza este valor por el percentil 25 o 75 segun sea el caso.
        """
        for columna in [var for var in df.columns if df[var].dtype!='O']:
            IQR = df[columna].quantile(0.75) - df[columna].quantile(0.25)
            rango_inferior = df[columna].quantile(0.25) - (IQR * 1.5)
            rango_superior = df[columna].quantile(0.75) + (IQR * 1.5)
            df.loc[df[columna] > rango_superior, columna] = df[columna].quantile(0.75)
            df.loc[df[columna] < rango_inferior, columna] = df[columna].quantile(0.25)
        return df
    @staticmethod
    def one_hot_encoder(df):
        """
        Funcion que permite crear las varibles dummies en codificacion onehot
        """
        ohe = OneHotEncoder()
        cat = [columna for columna in df.columns if columna not in ['RainToday', 'RainTomorrow'] and df[columna].dtype == 'O']
        num = [var for var in df.columns if df[var].dtype!='O']
        binary = ['RainToday', 'RainTomorrow']
        features = ohe.fit_transform(df[cat]).toarray()
        features_label = ohe.categories_
        labels = []
        for i in range(len(features_label)):
            label_list = np.array(features_label[i]).tolist()
            label_name = ["dummie_" + str(cat[i]) + "_" + str(elemento) for elemento in label_list]
            labels.extend(label_name)
        dummies = pd.DataFrame(features, columns = labels)
        df = pd.concat([df[num],df[binary],dummies], axis=1)
        df_sin_nans = df.copy().filter(regex='_nan$', axis=1).columns
        df.drop(columns=df_sin_nans, inplace=True)
        df.drop_duplicates(inplace=True)
        return df
    @staticmethod
    def vo_encoder(df):
        """
        Funcion que codifica la variable objetivo
        """
        df['RainTomorrow'] = df['RainTomorrow'].replace({'Yes': 1, 'No': 0})
        columna_extraida = df.pop('RainTomorrow')
        df['RainTomorrow'] = columna_extraida
        return df
    @staticmethod
    def imputer_vars(df):
        num = [var for var in df.columns if df[var].dtype!='O']
        df[num] = df[num].fillna(df[num].median())
        return df

if __name__ == "__main__":

    data = pd.read_csv(r"D:\Prueba_ML\prueba-nequi-rain-aust\data\raw\train\weatherAUS.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.assign(month=data['Date'].dt.month, year=data['Date'].dt.year, day=data['Date'].dt.day).drop('Date', axis=1)

    custom_transformer = FunctionTransformer(transformations_1.delete_regis_vo)
    custom_transformer2 = FunctionTransformer(transformations_1.outliers_replace)
    custom_transformer3 = FunctionTransformer(transformations_1.one_hot_encoder)
    custom_transformer4 = FunctionTransformer(transformations_1.binary_encoder)
    custom_transformer5 = FunctionTransformer(transformations_1.vo_encoder)
    custom_transformer6 = FunctionTransformer(transformations_1.imputer_vars)
    #imputer = SimpleImputer(strategy='median')

    preprocesing = Pipeline(steps=[
        ("delete", custom_transformer),
        ("outliers", custom_transformer2),
        ("oneHot", custom_transformer3),
        ("binary", custom_transformer4),
        ("vo", custom_transformer5),
        ("imputer", custom_transformer6)
    ])
    #pipeline = make_pipeline(preprocessor)
    preprocesing.fit(data)
    data_out = preprocesing.transform(data)
    print(data_out)
