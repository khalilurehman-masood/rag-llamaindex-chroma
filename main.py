from fastapi import FastAPI
from routes import router
import core.settings

app = FastAPI()


app.include_router(router=router)



@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/chat")
# def chat(req:QueryRequest):
#     query = req.query
#     # response = generate_response(query)
#     return {"response":str(response)}





