import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

diretorio_dados = "reports"
diretorio_vectordb = "chromadb"

def cria_vectordb():
    loader = PyPDFDirectoryLoader(diretorio_dados)
    documentos = loader.load()

    if not documentos:
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documentos)

    model_name = "intfloat/multilingual-e5-base"
    encode_kwargs = {'normalize_embeddings': True}

    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs
    )

    vectordb = Chroma.from_documents(
        chunks,
        embedding_model,
        persist_directory=diretorio_vectordb
    )

if __name__ == "__main__":
    cria_vectordb()
