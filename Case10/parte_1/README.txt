# Case10 - RAG com Relatório de Tendências em IA

# Instruções:

# 1 - Instale o WSL via Power Shell como administrador
Comando: wsl --install

# 2 - Confira a versão e instale o Ubuntu ou outra distro de sua preferência
Comando: wsl -l -v
Comando: wsl --install -d Ubuntu

(se quiser listar as versões disponíveis: wsl --list --online)

# 3 - Instale o Docker Desktop

# 4 - Abra o Docker Desktop > Settings > Resources > WSL integration > habilite as opções > Apply & Restart

# 5 - Instale o Ollama

# 6 - Baixe o Modelo llama 3.1
Abra o CMD (Win+R e digite cmd)
Execute o comando: ollama run llama3.1
Use ollama list para saber se foi instalado

# 7- Abra o terminal ou prompt de comando, navegue até a pasta onde estão os arquivos e crie o ambiente virtual
Comando: python -m venv case10_parte1
Ative (Comando no Windows): case10_parte1\Scripts\activate
Se o seu sistema operaiconal for Linux: source case10_parte1/bin/activate

# 8 - Execute o pipeline (o requirements será executado automaticamente):
python 05_executa_pipeline.py


Obs: o Docker Desktop e o Ollama precisam estar abertos. Se não tiver baixado o modelo antes vai aumentar o tempo de execução.
