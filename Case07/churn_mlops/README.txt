# Automação do Pipeline do Churn

# Importante: removi o random_state de tudo para garantir a aleatoriedade.

Cada parte é um módulo Python e o script churn_mlops.py irá orquestrar todo o pipeline.
Aqui está uma visão geral dos scripts e diretórios:

churn_mlops/
│
├── dados/                         # Dados brutos e processados
├── modelos/                       # Modelos treinados
├── pipeline/
│   ├── __init__.py                # Inicializador do módulo pipeline
│   ├── extrai_dados.py        # Extração de dados
│   ├── limpa_dados.py         # Limpeza de dados
│   ├── processa_dados.py      # Pré-processamento
│   ├── treina_modelo.py       # Treinamento do modelo
│   ├── avalia_modelo.py       # Avaliação e Monitoramento do modelo
│   └── deploy.py              # Deploy do modelo
│
└── churn_mlops.py                    # Script principal para execução do pipeline


# Siga os passos para executar:

# Crie um ambiente virtual:

python -m venv churnenv

# Ative o ambiente virtual:

# Windows:
churnenv\Scripts\activate

# MacOS/Linux:
source churnenv/bin/activate

# Execute os comandos:

pip install --upgrade pip (se der problema execute python -m pip install --upgrade pip)

pip install -r requirements.txt

# Abra outro terminal e ative o ambiente virtual de novo e execute:

mlflow ui --port 8282

# Deixe o seguinte link aberto em outra aba:

http://127.0.0.1:8282

# No primeiro terminal aberto execute:

python churn_mlops.py


# Confira os resultados.

# Qualquer dúvida assista o vídeo disponível no meu canal com passo a passo.


