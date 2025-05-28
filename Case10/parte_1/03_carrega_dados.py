import psycopg2
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://case10:case1010@localhost:5432/case10db')

print("\nCarregando os Dados!\n")

def case10_carrega_dados(csv_file, table_name, schema):

    try:
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
        print(f"Dados do arquivo {csv_file} foram inseridos na tabela {schema}.{table_name}.")
    except Exception as e:
        print(f"Erro ao inserir dados do arquivo {csv_file} na tabela {schema}.{table_name}: {e}")

case10_carrega_dados('datasets/organizacoes.csv', 'organizacoes', 'case10')
case10_carrega_dados('datasets/ferramentas.csv', 'ferramentas', 'case10')
case10_carrega_dados('datasets/aplicacoes.csv', 'aplicacoes', 'case10')

print("\nDados Carregados com Sucesso!\n")
print("\nAguarde, o Relatório poderá levar alguns minutos para ser finalizado!\n")
