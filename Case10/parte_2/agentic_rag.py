import os
import numpy as np
from langgraph.graph import StateGraph
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import torch
torch.classes.__path__ = []

os.environ["TOKENIZERS_PARALLELISM"] = "false"

llm = Ollama(model="gemma2:2b", temperature=0)

embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base", encode_kwargs={'normalize_embeddings': True})

vector_db = Chroma(persist_directory="chromadb", embedding_function=embedding_model)
retriever = vector_db.as_retriever()

prompt = PromptTemplate.from_template(
    "Você é um analista especializado em impacto de tecnologias de IA em organizações. Responda em português com base em:\n{context}\nPergunta: {input}"
)

chain = RunnablePassthrough() | prompt | llm | StrOutputParser()
qa_chain = create_retrieval_chain(retriever, chain)

class AgentState(BaseModel):
    query: str
    next_step: str = ""
    retrieved_info: list = []
    possible_responses: list = []
    similarity_scores: list = []
    ranked_response: str = ""
    confidence_score: float = 0.0

def passo_decisao_agente(state: AgentState) -> AgentState:
    query = state.query.lower()
    if any(p in query for p in ["explique", "resuma", "defina", "conceito", "geral", "o que "]):
        state.next_step = "gerar"
    else:
        state.next_step = "retrieve"
    return state

def retrieve_info(state: AgentState) -> AgentState:
    retrieved_docs = retriever.invoke(state.query)
    state.retrieved_info = retrieved_docs
    return state

def gera_multiplas_respostas(state: AgentState) -> AgentState:
    responses = [qa_chain.invoke({"input": state.query}) for _ in range(5)]
    state.possible_responses = responses
    return state

def avalia_similaridade(state: AgentState) -> AgentState:
    retrieved_texts = [doc.page_content for doc in state.retrieved_info]
    responses = state.possible_responses
    retrieved_embeddings = embedding_model.embed_documents(retrieved_texts) if retrieved_texts else []
    response_texts = [str(response) for response in responses]
    response_embeddings = embedding_model.embed_documents(response_texts) if response_texts else []

    if not retrieved_embeddings or not response_embeddings:
        state.similarity_scores = [0.0] * len(response_texts)
        return state

    similarities = [
        np.mean([cosine_similarity([response_embedding], [doc_embedding])[0][0] for doc_embedding in retrieved_embeddings])
        for response_embedding in response_embeddings
    ]

    state.similarity_scores = similarities
    return state

def rank_respostas(state: AgentState) -> AgentState:
    response_with_scores = list(zip(state.possible_responses, state.similarity_scores))
    if response_with_scores:
        ranked_responses = sorted(response_with_scores, key=lambda x: x[1], reverse=True)
        state.ranked_response = ranked_responses[0][0]
        state.confidence_score = ranked_responses[0][1]
    else:
        state.ranked_response = "Desculpe, não encontrei informações relevantes."
        state.confidence_score = 0.0
    return state

workflow = StateGraph(AgentState)
workflow.add_node("decision", passo_decisao_agente)
workflow.add_node("retrieve", retrieve_info)
workflow.add_node("generate_multiple", gera_multiplas_respostas)
workflow.add_node("evaluate_similarity", avalia_similaridade)
workflow.add_node("rank_responses", rank_respostas)

workflow.set_entry_point("decision")
workflow.add_conditional_edges(
    "decision",
    lambda state: {
        "retrieve": "retrieve",
        "gerar": "generate_multiple"
    }[state.next_step]
)
workflow.add_edge("retrieve", "generate_multiple")
workflow.add_edge("generate_multiple", "evaluate_similarity")
workflow.add_edge("evaluate_similarity", "rank_responses")

agent_workflow = workflow.compile()
