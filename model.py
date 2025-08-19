"""
model.py
--------
Defines and configures the language model (LLM) used throughout the Adaptive RAG pipeline. This may include model loading, configuration, and utility functions for LLM interaction.
"""

from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
embed_model = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME"),  
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)
llm_model = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # The deployment name for the chat model
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  # The API version for Azure OpenAI
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),  # Your Azure OpenAI API key  
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  # The endpoint for Azure OpenAI
        temperature=0,  # Setting temperature to 0 for more deterministic outputs
        streaming=False,  # Disable streaming for simpler handling of responses
        verbose=True  # Enable verbose mode for better debugging and logging
    )