from fastapi import FastAPI
from pydantic import BaseModel
from routes import router

app = FastAPI()
app.include_router(router=router)

class QueryRequest(BaseModel):
    query:str


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/chat")
# def chat(req:QueryRequest):
#     query = req.query
#     # response = generate_response(query)
#     return {"response":str(response)}





