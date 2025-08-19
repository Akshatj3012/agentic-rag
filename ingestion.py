"""
ingestion.py
------------
Handles data ingestion for the Adaptive RAG pipeline. Responsible for loading, preprocessing, and storing documents for retrieval.
"""

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_community.document_loaders import WebBaseLoader
from model import embed_model   
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

doc_splits = text_splitter.split_documents(docs_list)

embed = embed_model

# Create vector store with documents
vectorstore = FAISS.from_documents(doc_splits, embed)
        
# Save vectorstore locally for future use without rebuilding
vectorstore.save_local("./FAISS_index")

# Create retriever
retriever = vectorstore.as_retriever()