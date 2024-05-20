import json
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from openai import BaseModel
from pydantic import Field

from app.Dependencies.dependencies import get_data_service, get_openai_service
from app.Services.dataService import DataService
from app.Services.openAIService import OpenAIService
import secrets

load_dotenv()
app = FastAPI()


# Simulated session storage for demonstration purposes
sessions={}

@app.get("/token")
def get_token():
    """
    Get a token for a chat with the chatbot. You should include this token as a query parameter in subsequent requests to the chat endpoint
    """
    key = secrets.token_urlsafe()
    sessions[key]=[]
    return key


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, strip_whitespace=True)
    token: str = Field(..., min_length=1, strip_whitespace=True)
    class Config :
        extra="forbid"

@app.post("/chat")
async def test(request:ChatRequest, openAIservice: OpenAIService = Depends(get_openai_service), dataService:DataService = Depends(get_data_service)):
    """
    The request body should contain the query and the token as strings.
    """
    token = request.token
    query = request.query
    if(not token in sessions):
        raise HTTPException(status_code=400, detail="Invalid token")
    #retrieve the conversation or start a new one
    conversation = sessions[token]
    if(len(conversation) == 0):
        conversation.append(openAIservice.get_start_message())
    #process the user query
    conversation.append(openAIservice.get_message("user",query))
    response = openAIservice.process_query(conversation)
    # when the query is not relevant or the chatbot needs clarification
    if(response.tool_calls is None):
        conversation.append(openAIservice.get_message("assistant",response.content))
        return response.content
    # get the function call response
    response.content = str(response.tool_calls[0].function)
    # get the data
    result = await dataService.get_data(response.tool_calls[0].function.name,json.loads(response.tool_calls[0].function.arguments))
    # process the data
    conversation.append(openAIservice.get_fct_call_message(response.tool_calls[0],result))
    #return the chatbot's response
    final_response = openAIservice.process_query(conversation)
    return final_response.content