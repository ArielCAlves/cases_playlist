from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)


def preprocessa_dados(df, target_column):
    df[target_column] = df[target_column].replace({'SIM': 1, 'NAO': 0})
    df[target_column] = df[target_column].infer_objects(copy=False)
    features = ['TEMPO_PERMANENCIA_CLIENTE_MESES',
                'TICKET_MEDIO',
                'RECENCIA',
                'FREQUENCIA',
                'C',
                'D',
                'H',
                'OUTROS']

    df = df[features + [target_column]].dropna()
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns
