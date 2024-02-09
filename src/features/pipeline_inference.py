import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import FunctionTransformer
import pandas as pd
from datetime import datetime
from src.data_get.make_dataset import *
from src.config.get_r import *

class Transformations2:
    def ejecutar(params):
        td = TrerData()
        data = td.data(inference = True, train = False)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.assign(month=data['Date'].dt.month, year=data['Date'].dt.year, day=data['Date'].dt.day).drop('Date', axis=1)
        custom_transformer1 = FunctionTransformer(Transformations2.one_hot_encoder)
        custom_transformer2 = FunctionTransformer(Transformations2.binary_encoder)
        custom_transformer3 = FunctionTransformer(Transformations2.imputer_vars)
        #imputer = SimpleImputer(strategy='median')
        preprocesing = Pipeline(steps=[
            ("oneHot", custom_transformer1),
            ("binary", custom_transformer2),
            ("imputer", custom_transformer3)
        ])
        #pipeline = make_pipeline(preprocessor)
        preprocesing.fit(data)
        data_out = preprocesing.transform(data)
        print(data_out)
        half_rows = len(data_out) // 5
        data_out = data_out.drop(data_out.index[:half_rows])
        data_out.to_excel(RutaT.get_folder() + params.get("ruta_procesa") + "data_model_inf_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))

    @staticmethod
    def binary_encoder(df):
        """
        Funcion que codifica la columna RainToday en una codificacion binaria
        """
        #encoder = ce.BinaryEncoder(cols=['RainToday'])
        #df_decode = encoder.fit_transform(df)
        #for col in encoder.get_feature_names_out():
        #    df.loc[:, col] = df_decode.loc[:, col]
        #df.drop(columns= 'RainToday', inplace=True)
        df['RainToday_1'] = df['RainToday'].apply(lambda x: 1 if x == 'Yes' else 0)
        df['RainToday_0'] = df['RainToday'].apply(lambda x: 0 if x == 'Yes' else 1)
        df.drop(columns= 'RainToday', inplace=True)
        return df
    @staticmethod
    def one_hot_encoder(df):
        """
        Funcion que permite crear las varibles dummies en codificacion onehot
        """
        ohe = OneHotEncoder()
        cat = [columna for columna in df.columns if columna not in ['RainToday'] and df[columna].dtype == 'O']
        num = [var for var in df.columns if df[var].dtype!='O']
        binary = ['RainToday']
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
    def imputer_vars(df):
        num = [var for var in df.columns if df[var].dtype!='O']
        print(num)
        df[num] = df[num].fillna(df[num].median())
        return df

if __name__ == "__main__":

    data = pd.read_csv(r"D:\Prueba_ML\prueba-nequi-rain-aust\data\raw\inference\weatherAUS_{}.csv".format(datetime.now().strftime('%Y-%m-%d')))
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.assign(month=data['Date'].dt.month, year=data['Date'].dt.year, day=data['Date'].dt.day).drop('Date', axis=1)

    custom_transformer1 = FunctionTransformer(Transformations2.one_hot_encoder)
    custom_transformer2 = FunctionTransformer(Transformations2.binary_encoder)
    custom_transformer3 = FunctionTransformer(Transformations2.imputer_vars)
    #imputer = SimpleImputer(strategy='median')

    preprocesing = Pipeline(steps=[
        ("oneHot", custom_transformer1),
        ("binary", custom_transformer2),
        ("imputer", custom_transformer3)
    ])
    #pipeline = make_pipeline(preprocessor)
    preprocesing.fit(data)
    data_out = preprocesing.transform(data)
    print(data_out)
    data_out.to_excel(r"D:\Prueba_ML\prueba-nequi-rain-aust\data\proccesed\data_model_inference_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))

