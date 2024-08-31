from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_client_azure_openai():
    GPT4V_KEY = os.getenv("GPT4V_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
    return AzureOpenAI(api_key=GPT4V_KEY,
                    azure_endpoint=AZURE_ENDPOINT,
                    api_version="2024-02-15-preview")

def get_client_openai():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
