import psycopg2
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import textwrap

llm = Ollama(model="llama3.1")
output_parser = StrOutputParser()

def gera_analises():
    conn = psycopg2.connect(
        dbname="case10db",
        user="case10",
        password="case1010",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    query = """
        SELECT
            o.nome AS organizacao,
            o.setor,
            f.nome AS ferramenta,
            f.categoria,
            a.descricao_uso,
            a.beneficio_percentual,
            a.ano
        FROM
            case10.aplicacoes a
        JOIN
            case10.organizacoes o ON a.id_org = o.id
        JOIN
            case10.ferramentas f ON a.id_ferramenta = f.id
        WHERE
            a.beneficio_percentual > 30
        ORDER BY
            o.nome;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    analises = []

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um analista de tecnologia. Analise os dados abaixo e forneça um resumo em português sobre os padrões de uso de IA por organização."),
        ("user", "question: {question}")
    ])
    chain = prompt | llm | output_parser

    for row in rows:
        organizacao, setor, ferramenta, categoria, descricao_uso, beneficio, ano = row
        consulta = (
            f"Organização: {organizacao} | Setor: {setor} | Ferramenta: {ferramenta} "
            f"(Categoria: {categoria}) | Uso: {descricao_uso} | Benefício: {beneficio}% | Ano: {ano}."
        )
        response = chain.invoke({'question': consulta})
        analises.append(response)

    conn.close()

    width, height = A4
    margem_esquerda = 3 * cm
    margem_direita = 2 * cm
    margem_topo = 3 * cm
    margem_inferior = 2 * cm
    largura_texto = width - margem_esquerda - margem_direita
    altura_max = height - margem_topo
    altura_min = margem_inferior
    max_caracteres = int(largura_texto / 5.5)

    c = canvas.Canvas("resultado/analises.pdf", pagesize=A4)
    y = height - margem_topo
    c.setFont("Times-Roman", 12)

    for analise in analises:
        paragrafos = analise.split('\n')
        for paragrafo in paragrafos:
            linhas = textwrap.wrap(paragrafo, width=max_caracteres)
            for linha in linhas:
                if y < margem_inferior + 20:
                    c.showPage()
                    c.setFont("Times-Roman", 12)
                    y = height - margem_topo
                c.drawString(margem_esquerda, y, linha)
                y -= 15
            y -= 10
        y -= 20

    c.save()
    return analises

analises = gera_analises()
for analise in analises:
    print(analise)
