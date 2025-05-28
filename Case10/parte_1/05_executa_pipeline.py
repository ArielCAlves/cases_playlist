import subprocess
from time import time

def executa_comando(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"\nComando '{command}' executado com sucesso.")
        print("\nSaída:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\nErro ao executar o comando '{command}'.")
        print("\nErro:\n", e.stderr)

def executa_pipeline(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f"\nScript {script_name} executado com sucesso.")
        print("\nSaída:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"\nErro ao executar o script {script_name}.")
        print("\nErro:\n", e.stderr)

docker_command = (
    "docker run --name case10-container "
    "-p 5432:5432 "
    "-e POSTGRES_USER=case10 "
    "-e POSTGRES_PASSWORD=case1010 "
    "-e POSTGRES_DB=case10db "
    "-d postgres:16.1"
)

pip_command = "pip install -r requirements.txt"

start_time = time()

executa_comando(docker_command)
executa_comando(pip_command)

scripts = [
    '02_cria_tabelas.py',
    '03_carrega_dados.py',
    '04_executa_llm.py'
]

for script in scripts:
    executa_pipeline(script)

destroy_docker_command = "docker rm -f case10-container"
executa_comando(destroy_docker_command)

end_time = time()
total_time = end_time - start_time

print(f"\nPipeline executado com sucesso.")
print(f"Tempo total de execução: {total_time:.2f} segundos.\n")
