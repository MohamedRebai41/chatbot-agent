import os
from fastapi import HTTPException
import httpx
class DataService:
    async def get_data(self, name, params):
        if name == "get_department_competition_result":
            return await self.get_department_competition_result(params["ranks"])
        elif name == "get_individual_competition_result":
            return await self.get_individual_competition_result(params["ranks"])
        else:
            raise Exception("Method not supported")
    async def get_department_competition_result(self,ranks):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{os.getenv("DATA_SERVICE_BASE_URL")}/department/",params={"ranks":ranks})
                results = response.json()
        except:
            raise HTTPException(status_code=504, detail="Something went wrong. Try again later.")
        return results
    async def get_individual_competition_result(self, ranks):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{os.getenv("DATA_SERVICE_BASE_URL")}/individual/",params={"ranks":ranks})
                results = response.json()
        except:
            raise HTTPException(status_code=504, detail="Something went wrong. Try again later.")
        return results
    def get_methods_description(self):
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_department_competition_result",
                    "description": "Get the competition results for departments based on ranks. Limited to the top 3 winners",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ranks": {
                                "type": "array",
                                "items": {
                                    "type": "integer"
                                },
                                "description": "The ranks to filter the competition results by"
                            }
                        },
                        "required": ["ranks"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_individual_competition_result",
                    "description": "Get the competition results for individuals based on ranks. Limited to the top 3 winners",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ranks": {
                                "type": "array",
                                "items": {
                                    "type": "integer"
                                },
                                "description": "The ranks to filter the competition results by"
                            }
                        },
                        "required": ["ranks"]
                    }
                }
            }
        ]
        return tools    