import joblib
import os
import numpy as np
import pandas as pd

def carrega_modelo(model_path, scaler_path, columns_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    columns = joblib.load(columns_path)
    return model, scaler, columns

def faz_previsoes(model, X_new):
    return model.predict(X_new)

def salva_top_churn(model, scaler, X, df_original, path_base, top_percent=0.4):
    X_scaled = scaler.transform(X)
    y_proba = model.predict_proba(X_scaled)

    churn_probabilities = y_proba[:, 1]
    results = pd.DataFrame({
        'client_id': range(len(churn_probabilities)),
        'CHURN_PROBABILITY': churn_probabilities
    })
    results.sort_values(by='CHURN_PROBABILITY', ascending=False, inplace=True)
    top_40_percent_count = int(top_percent * len(results))
    top_40_percent_clients = results.head(top_40_percent_count)
    df_rf = df_original.loc[top_40_percent_clients['client_id']]
    df_rf['CHURN_PROBABILITY'] = top_40_percent_clients.set_index('client_id')['CHURN_PROBABILITY']
    df_rf.drop(columns=['CHURN'], inplace=True)

    os.makedirs(path_base, exist_ok=True)
    df_rf.to_excel(f"{path_base}/resultado.xlsx", index=False)
