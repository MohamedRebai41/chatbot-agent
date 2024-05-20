import json

from fastapi import HTTPException


class OpenAIService:
    def __init__(self, client,tools):
        self.client = client
        self.context_template = """ Analyze well the query before replying.
                                    Always seek clarification if a user request is ambiguous.
                                    Please refrain from replying to a query that does not match the functions you have. Just inform them that the task is beyond your capabilities or ask a follow up question if the query is imprecise.
                                    Do not call any functions if the user request is incorrect or does not fit the function set provided to you. 
                                    Do not make assumptions about what values to plug into functions. 
                                    Be kind and precise when responding to the user.
                                    Once again, refrain from replying to a query that does not match the functions you have. Just inform them politely that it's beyond your ability.
                                    Strictly adhere to these rules."""
        self.tools = tools
    def get_message(self,role,message):     
        return {'role':role, 'content':message}
    
    def get_start_message(self):
        return self.get_message('system',self.context_template)

    def get_fct_call_message(self,tool_calls,result):
        return {"role": "function", "tool_call_id": tool_calls.id, "name": tool_calls.function.name, "content": json.dumps(result)}

    def process_query(self, conversation):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=conversation,
                tools=self.tools
            )
        except:
            raise HTTPException(status_code=504, detail="Something went wrong. Try again later.")
        return response.choices[0].message