import json
import os
from typing import List
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from openai import BaseModel
from pydantic import conlist

from app.Dependencies.dependencies import get_data_service, get_openai_service
from app.Services.dataService import DataService
from app.Services.openAIService import OpenAIService



load_dotenv()
data_file_path = os.getenv("DATA_FILE_PATH")
with open(data_file_path, 'r',errors='replace') as file:
        data = json.load(file)
app = FastAPI()


@app.get("/data")
def get_data():
    return data


@app.post("/data")
async def set_data(file:UploadFile = File() ,openAiService:OpenAIService = Depends(get_openai_service)):
    """
    The text data uploaded to this endpoint will be processed. Useful data will be extracted into a json file that will represent our little database. 
    """
    content = await file.read()
    text = content.decode('utf-8')
    conversation = [openAiService.get_start_message(text)]
    response = openAiService.process_query(conversation)
    with open(data_file_path,'w') as file:
        file.write(response)
    return json.loads(response)



@app.get("/department/")
def get_department_results(ranks: List[int] = Query(...), dataService: DataService = Depends(get_data_service) ):
    """
    The ranks requested are injected as a query parameter
    """
    if(len(ranks)==0):
        raise HTTPException(status_code=400, detail="Ranks cannot be empty.") 
    if any(rank > 3 for rank in ranks):
        raise HTTPException(status_code=400, detail="Ranks greater than 3 are not allowed.")
    return dataService.get_department_competition_result(data,ranks) 

@app.get("/individual/")
def get_individual_results(ranks: List[int] = Query(...), dataService: DataService = Depends(get_data_service) ):
    """
    The ranks requested are injected as a query parameter
    """
    if(len(ranks)==0):
        raise HTTPException(status_code=400, detail="Ranks cannot be empty.") 
    if any(rank > 3 for rank in ranks):
        raise HTTPException(status_code=400, detail="Ranks greater than 3 are not allowed.")
    return dataService.get_individual_competition_result(data,ranks) 

