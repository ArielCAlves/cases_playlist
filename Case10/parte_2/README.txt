# Para executar a app:

# Abra o terminal ou prompt de comando, navegue até a pasta com os arquivos e execute o comando abaixo para criar um ambiente virtual:
python -m venv case10_parte2

# Ative o ambiente:
case10_parte2\Scripts\activate

# Instale o pip e as dependências:
python -m pip install --upgrade pip
pip install -r requirements.txt 

# Abra o terminal ou prompt de comando, navegue até a pasta com os arquivos e execute: 
# OBS: pegue o arquivo gerado na parte 1 e coloque na pasta reports da parte 2 antes de executar

python rag.py
streamlit run app.py
python testa_agentic_rag.py -v



