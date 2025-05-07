import logging
import mlflow
from datetime import datetime
from sklearn.metrics import accuracy_score, classification_report

logging.getLogger("mlflow").setLevel(logging.CRITICAL)

def avalia_modelo(model, X_test, y_test, threshold=0.405):
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_prob >= threshold).astype(int)
    accuracy = accuracy_score(y_test, y_pred)
    print("Relatório de classificação:")
    print(classification_report(y_test, y_pred))
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    return accuracy, report_dict

def monitora_modelo(model, accuracy, report, nome_base='Churn', uri='http://127.0.0.1:8282'):
    mlflow.set_tracking_uri(uri)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_experimento = f"{nome_base}_{timestamp}"
    mlflow.set_experiment(nome_experimento)
    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "modelo")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision_churn", report['1']['precision'])
        mlflow.log_metric("recall_churn", report['1']['recall'])
        mlflow.log_metric("f1_churn", report['1']['f1-score'])
