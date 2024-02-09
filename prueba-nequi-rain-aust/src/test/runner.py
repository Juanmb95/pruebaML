import unittest
from unittest import TextTestRunner
from src.test.test_rain_aus_fun import *
from src.test.test_rain_aus_fun_inf import *
import time
from unittest.runner import TextTestResult
import logging
from src.config.get_r import RutaT

class RunTest:
    @staticmethod
    def ejecutar(params, tipo):
        if(tipo == "train"):
            logging.basicConfig(filename = RutaT.get_folder() + params.get("ruta_logs") + "\\archivo_pruebas_unitarias_{}".format(datetime.now().strftime('%Y-%m-%d')) + ".log", level=logging.INFO)
            suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctions)
        else:
            logging.basicConfig(filename = RutaT.get_folder() + params.get("ruta_logs") + "\\archivo_pruebas_unitarias_inf{}".format(datetime.now().strftime('%Y-%m-%d')) + ".log", level=logging.INFO)
            suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctionsInf)
        result = TextTestRunner().run(suite)
        for test_case, errors in result.failures + result.errors:
            logging.error(f"Error en la prueba: {test_case.id()}\n{errors}")
