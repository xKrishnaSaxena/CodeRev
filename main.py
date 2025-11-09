from fastapi import FastAPI
from pydantic import BaseModel

class Code(BaseModel):
    code_snippet:str
    language:str
    context:str

app = FastAPI()

@app.get("/health")
def health_checker():
    return {"Hello world"}

@app.post("/review")
def code_review(code:Code):
    print(code.code_snippet)
    print(code.language)
    print(code.context)

    res={"type":"Issue_type", "severity":"Issue_severity", "description":"Issue_description", "line_numbers":"Issue_line_numbers", "suggestions":"Issue_Suggestions" , "Overall_Score":"Code_Score"}

    return res