#OpenAI dependency
from fastapi import Depends
from openai import OpenAI

from app.Services.dataService import DataService
from app.Services.openAIService import OpenAIService


def get_openai_client():
    return OpenAI()

def get_data_service():
    return DataService()


def get_openai_service(client=Depends(get_openai_client)):
    return OpenAIService(client)
