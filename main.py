from fastapi import FastAPI
from routes import router
import core.settings
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register

tracer_provider = register()
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
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





