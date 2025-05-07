import os
import joblib
from pipeline.extrai_dados import extrai_dados
from pipeline.limpa_dados import limpa_dados
from pipeline.processa_dados import preprocessa_dados
from pipeline.treina_modelo import treina_modelo
from pipeline.avalia_modelo import avalia_modelo, monitora_modelo
from pipeline.deploy import carrega_modelo, salva_top_churn

def executa_pipeline(data_path, target_column):
    model_path = "modelos/model_rf.pkl"
    scaler_path = "modelos/scaler.pkl"
    columns_path = "modelos/columns.pkl"

    print("Executando a Etapa 1 - Extração e Carga dos Dados.\n")
    df1, df2, df3, df4 = extrai_dados(data_path)

    print("\nExecutando a Etapa 2 - Limpeza dos Dados.\n")
    df_original = limpa_dados(df1, df2, df3, df4)

    print("\nExecutando a Etapa 3 - Pré-Processamento.\n")
    X_train, X_test, y_train, y_test, scaler, columns = preprocessa_dados(df_original, target_column)

    if y_train is None or len(y_train) == 0:
        print("Erro: `y_train` está vazio após o pré-processamento.")
        return

    print("\nExecutando a Etapa 4 - Treinamento do Modelo.\n")
    model = treina_modelo(X_train, y_train)

    joblib.dump(scaler, scaler_path)
    joblib.dump(columns, columns_path)
    joblib.dump(model, model_path)

    print("\nExecutando a Etapa 5 - Avaliação do Modelo.\n")
    if y_test is not None and len(y_test) > 0:
        accuracy, report = avalia_modelo(model, X_test, y_test)
        print(f"Acurácia do modelo: {accuracy}")       

        monitora_modelo(model, accuracy, report)
    else:
        print("Erro: `y_test` está vazio, não é possível avaliar o modelo.")

    print("\nEtapa 6 - Deploy do Modelo.\n")
    model_deployed, scaler_deployed, columns_deployed = carrega_modelo(model_path, scaler_path, columns_path)

    if model_deployed and scaler_deployed and columns_deployed is not None:
        print("Modelo e pré-processamento carregados com sucesso para produção.")
    else:
        print("Erro: O modelo ou o pré-processamento não foram carregados corretamente.")

    print("\nEtapa 7 - Salvando resultados.\n")
    X_full = df_original[columns_deployed].copy().reset_index(drop=True)
    salva_top_churn(model_deployed, scaler_deployed, X_full, df_original.reset_index(drop=True), path_base=data_path)

if __name__ == "__main__":
    print("\nIniciando a Execução do Pipeline de Churn...\n")

    data_path = "dados"
    target_column = "CHURN"

    executa_pipeline(data_path, target_column)

    print("\nExecução do Pipeline Concluída com Sucesso!\n")
