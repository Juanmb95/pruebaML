import importlib
import os
class RutaT:
    @staticmethod
    def get_folder():
            locMod = importlib.import_module(__name__)
            filename = locMod.__file__
            pathBase   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(filename))))
            return pathBase

if __name__ == "__main__":
    print(RutaT.get_folder())
