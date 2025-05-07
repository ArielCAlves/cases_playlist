import pandas as pd

def extrai_dados(path_base):
    df_1 = pd.read_csv(f"{path_base}/parte1.csv")
    df_2 = pd.read_csv(f"{path_base}/parte2.csv")
    df_3 = pd.read_csv(f"{path_base}/parte3.csv")
    df_4 = pd.read_csv(f"{path_base}/parte4.csv")

    return df_1, df_2, df_3, df_4