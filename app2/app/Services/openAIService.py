class OpenAIService:
    def __init__(self, client):
        self.client = client
        self.context_template = """ You're going to be given text containing data relative to the winners of two competitions.
                                    Extract the results into a JSON Object of the following template:
                                    {
                                        "departments": [
                                            {
                                                "place":number
                                                "department":string
                                                "description":string
                                            }, 
                                            ...
                                        ],
                                        "individual": [
                                            {
                                                "place":number
                                                "name":string
                                                "department":string
                                                "description"string
                                            },
                                            ...
                                        ]
                                    }
                                Here is the text: 
                                [TEXT]
                                Output only the JSON object.
                            """
    def get_query(self,data: dict, template: str):
        # Replace placeholders in the template with corresponding data from the dictionary
        for key, value in data.items():
            placeholder = f'[{key.upper()}]'
            query = template.replace(placeholder, value)
        return query
    def get_message(self,role,message):     
        return {'role':role, 'content':message}
    
    def get_start_message(self,text):
        return self.get_message('system',self.get_query({"text":text},self.context_template))

    def process_query(self, conversation):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        return response.choices[0].message.content