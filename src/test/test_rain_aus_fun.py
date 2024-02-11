import pandas as pd
from datetime import datetime
from importlib import reload
import unittest
#from pipeline_preprocesado import delete_regis_vo
from src.features.pipeline_preprocesado import *
from src.data_get.make_dataset import *

class TestFunctions(unittest.TestCase):
    def setUp(self):
        td = TrerData()
        self.df = td.data(inference = False, train = True)
        return super().setUp()
    def test_validar_delete_regis_vo(self):
        a = transformations_1.delete_regis_vo(self.df)
        val = a['RainTomorrow'].isnull().sum()
        self.assertEqual(val, 0)
    def test_binary_encoder(self):
        a = transformations_1.binary_encoder(self.df)
        self.assertIn(a['RainToday_0'].unique()[0], [0,1])
        self.assertIn(a['RainToday_1'].unique()[0], [0,1])
    def test_vo_encoder(self):
        a = transformations_1.vo_encoder(self.df)
        self.assertIn(a['RainTomorrow'].unique()[0], [0,1])
    def test_imputer_vars(self):
        a = transformations_1.imputer_vars(self.df)
        num = [var for var in a.columns if a[var].dtype!='O']
        self.assertEqual(a[num].isnull().sum().sum(), 0)
    def test_one_hot_encoder(self):
        a = transformations_1.one_hot_encoder(self.df)
        list_col_ori = [columna for columna in self.df.columns if columna not in ['RainToday', 'RainTomorrow'] and self.df[columna].dtype == 'O']
        list_col_mod = [columna for columna in a.columns if columna not in ['RainToday', 'RainTomorrow']]
        self.assertNotIn(list_col_ori[0], list_col_mod)


if __name__ == '__main__':
    unittest.main()