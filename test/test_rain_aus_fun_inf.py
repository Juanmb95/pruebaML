import pandas as pd
from datetime import datetime
from importlib import reload
import unittest
#from pipeline_preprocesado import delete_regis_vo
from src.features.pipeline_inference import *
from src.data_get.make_dataset import *

class TestFunctionsInf(unittest.TestCase):
    def setUp(self):
        td = TrerData()
        self.df = td.data(inference = True, train = False)
        return super().setUp()
    def test_binary_encoder(self):
        a = Transformations2.binary_encoder(self.df)
        self.assertIn(a['RainToday_0'].unique()[0], [0,1])
        self.assertIn(a['RainToday_1'].unique()[0], [0,1])
    def test_imputer_vars(self):
        a = Transformations2.imputer_vars(self.df)
        self.assertEqual(a.isnull().sum().sum(), 0)
    def test_one_hot_encoder(self):
        a = Transformations2.one_hot_encoder(self.df)
        list_col_ori = [columna for columna in self.df.columns if columna not in ['RainToday', 'RainTomorrow'] and self.df[columna].dtype == 'O']
        list_col_mod = [columna for columna in a.columns if columna not in ['RainToday', 'RainTomorrow']]
        self.assertNotIn(list_col_ori[0], list_col_mod)


if __name__ == '__main__':
    unittest.main()