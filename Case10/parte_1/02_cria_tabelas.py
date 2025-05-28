import psycopg2


def executa_script_sql(filename):    
    conn = psycopg2.connect(
        dbname="case10db",
        user="case10",
        password="case1010",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    with open(filename, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    try:
        cur.execute(sql_script)
        conn.commit()
        print("\nScript executado com sucesso!\n")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao executar o script: {e}")
    finally:
        cur.close()
        conn.close()

executa_script_sql('case10_tabelas.sql')
