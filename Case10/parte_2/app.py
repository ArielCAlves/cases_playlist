import streamlit as st
from agentic_rag import AgentState, agent_workflow

st.set_page_config(page_title="Case 10 - Agente de IA para Relatórios", page_icon=":bar_chart:", layout="centered")

st.sidebar.title("Exemplo de Perguntas")
st.sidebar.write("""
- Quais ferramentas de IA foram mais utilizadas pelas organizações em 2024?
- Como a IA está sendo aplicada no setor jurídico segundo o relatório?
- Qual o impacto da IA no setor público de acordo com os dados analisados?
- Que uso a empresa Clara Rocha Sistemas faz da ferramenta MLflow?
- O que a empresa Paula Costa Analytics está automatizando com ChromaDB?
""")

if st.sidebar.button("Suporte"):
    st.sidebar.write("Dúvidas? Busque o canal do Youtube: @arielcarvalhodados")

st.title("Case 10 - Agente de IA")
st.title("IA Generativa e Agentic RAG")

query = st.text_input("Digite sua pergunta:")

if st.button("Enviar"):
    with st.spinner("Processando consulta... Aguarde."):
        output = agent_workflow.invoke(AgentState(query=query))

    st.subheader("Resposta:")
    resposta = output.get("ranked_response", "Nenhuma resposta.")
    confidence = output.get("confidence_score", 0.0)

    if isinstance(resposta, dict) and "answer" in resposta:
        resposta = resposta["answer"]

    st.markdown(resposta)
    st.subheader("Confiança da Resposta com Base no RAG:")
    st.markdown(f"`{confidence:.2f}`")

    documentos_relacionados = output.get("retrieved_info", [])
    if documentos_relacionados:
        st.subheader("Documentos Relacionados:")
        for doc in documentos_relacionados:
            st.markdown(f"**ID:** `{doc.id}`")
            st.markdown(f"**Fonte:** `{doc.metadata.get('source', 'Desconhecida')}`")
            st.text_area("Conteúdo", doc.page_content, height=80)
    else:
        st.write("Nenhum documento relacionado encontrado.")
