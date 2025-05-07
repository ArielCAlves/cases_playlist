import pandas as pd

def limpa_dados(df_1, df_2, df_3, df_4):
    df_1 = df_1.dropna()
    df_2 = df_2.dropna()
    df_3.TEMPO_PERMANENCIA_CLIENTE_MESES = df_3.TEMPO_PERMANENCIA_CLIENTE_MESES.astype(int)
    df_3 = df_3[['ID', 'TEMPO_PERMANENCIA_CLIENTE_MESES']]
    df_4 = df_4.dropna()
    df_4["DATA_MENSAL"] = pd.to_datetime(df_4["DATA_MENSAL"])

    max_date = df_4["DATA_MENSAL"].max()
    df_rfv = df_4.copy()
    df_rfv['DATA_MENSAL'] = df_rfv['DATA_MENSAL'].dt.to_period('M').dt.to_timestamp()

    recency = (max_date - df_rfv.groupby('ID')["DATA_MENSAL"].max()).dt.days
    frequency = df_rfv.groupby("ID")["DATA_MENSAL"].nunique()
    value = df_rfv.groupby("ID")["TOTAL_CASOS"].sum()

    df_rfv = pd.DataFrame({
        'ID': recency.index,
        'RECENCIA': recency.values,
        'FREQUENCIA': frequency.values,
        'VALOR': value.values
    })

    df_merged = pd.merge(df_1, df_2, how='left', on='NUMERO_DO_CASO')
    df_merged = pd.merge(df_merged, df_3, how='left', on='ID')
    df_merged = pd.merge(df_merged, df_4, how='left', on='ID')
    df_merged.drop(columns=['TOTAL_FATURADO_DOLAR', 'DATA_ABERTURA', 'TOTAL_CASOS_y'], inplace=True)
    df_merged.rename(columns={'TOTAL_CASOS_x': 'TOTAL_CASOS'}, inplace=True)

    df_faturamento = df_4.groupby('ID')['TOTAL_DOLAR_FATURADO'].sum().reset_index()
    df_ticket_medio = df_4.groupby('ID')['TOTAL_DOLAR_FATURADO'].mean().reset_index()
    df_ticket_medio.rename(columns={'TOTAL_DOLAR_FATURADO': 'TICKET_MEDIO'}, inplace=True)

    df_servicos = df_merged[['ID', 'SERVICO_AGRUPADO']].assign(SERVICO_AGRUPADO=lambda df: df['SERVICO_AGRUPADO'].str.split(';')).explode('SERVICO_AGRUPADO')
    servico_counts = df_servicos['SERVICO_AGRUPADO'].value_counts()
    corte = 500000
    frequentes = servico_counts[servico_counts >= corte]
    raros = servico_counts[servico_counts < corte]
    substituicoes_outros = {letra: letra for letra in frequentes.index}
    for letra in raros.index:
        substituicoes_outros[letra] = 'OUTROS'
    df_servicos['SERVICO_AGRUPADO'] = df_servicos['SERVICO_AGRUPADO'].map(substituicoes_outros)
    df_result_servicos = df_servicos.groupby(['ID', 'SERVICO_AGRUPADO']).size().unstack(fill_value=0).reset_index()

    df_resultado_abandonados = df_merged.groupby("ID").agg({
        "TOTAL_CASOS": "sum",
        "TOTAL_NAO_ABANDONADOS": "sum",
        "TOTAL_ABANDONADOS": "sum"
    }).reset_index()

    df_merged = df_merged[['ID','TEMPO_PERMANENCIA_CLIENTE_MESES']].groupby('ID').first().reset_index()
    df_merged_final = pd.merge(df_merged, df_result_servicos, on='ID')
    df_merged_final = pd.merge(df_merged_final, df_resultado_abandonados, on='ID')
    df_merged_final = pd.merge(df_merged_final, df_faturamento, on='ID')
    df_merged_final = pd.merge(df_merged_final, df_ticket_medio, on='ID')
    df_merged_final = pd.merge(df_merged_final, df_rfv, on='ID')

    df_merged_final["PERCENTUAL_ABANDONADOS"] = (df_merged_final["TOTAL_ABANDONADOS"] / df_merged_final["TOTAL_CASOS"]) * 100
    df_merged_final["CHURN"] = df_merged_final["PERCENTUAL_ABANDONADOS"].apply(lambda x: "SIM" if x >= 60 else "NAO")

    df_merged_final.drop(columns=['TOTAL_NAO_ABANDONADOS','TOTAL_ABANDONADOS','PERCENTUAL_ABANDONADOS','TOTAL_CASOS'], inplace=True)
    return df_merged_final