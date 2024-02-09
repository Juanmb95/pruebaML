from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import confusion_matrix
import pickle
#from features.pipeline_preprocesado import *
from src.data_get.make_dataset import *
from src.config.get_r import RutaT

class ModelTrain:
    @staticmethod
    def train(params):
        data_out =  TrerData().data_proce()
        x = data_out.drop(['RainTomorrow'], axis=1)
        y = data_out['RainTomorrow']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
        scaler = MinMaxScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        logreg = LogisticRegression(max_iter = 500, C = 1, solver = 'liblinear', random_state = 0)
        logreg.fit(x_train, y_train)
        y_pred_test = logreg.predict(x_test)
        y_pred_train = logreg.predict(x_train)
        precision_test = accuracy_score(y_test, y_pred_test)
        recall_test = accuracy_score(y_test[y_test == 1], y_pred_test[y_test == 1])
        precision_train = accuracy_score(y_train, y_pred_train)
        recall_train = accuracy_score(y_train[y_train == 1], y_pred_train[y_train == 1])
        auc_test = roc_auc_score(y_test, y_pred_test)
        auc_train = roc_auc_score(y_train, y_pred_train)
        df = pd.DataFrame({
            'Metric': ['Precision model_test', 'Recall_test', 'Precision model_train', 'Recall_train', 'Auc_test', 'Auc_train'],
            'Value': [precision_test, recall_test, precision_train, recall_train, auc_test, auc_train]
        })
        df.to_excel(RutaT.get_folder() + params.get("ruta_reports") + "\\" + "metrics_model_{}.xlsx".format(datetime.now().strftime('%Y-%m-%d')))
        cm = confusion_matrix(y_test, y_pred_test)
        print(cm)
        with open(RutaT.get_folder() + params.get("ruta_models") + '\\sk_rain_model_{}.pkl'.format(datetime.now().strftime('%Y-%m-%d')), 'wb') as f:
            pickle.dump(logreg, f)
