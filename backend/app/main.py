from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
from .services.retrieval import retrieve_relevant_data
from .services.generation import generate_answer 

app = FastAPI(); 

class Query(BaseModel): 
    query: str 

@app.post("/generate/")

async def generate_response(query: Query):
    try: 
        #Retreive relevant data
        documents = retrieve_relevant_data(query.query)

        #Generate answer using the query
        response = generate_answer(query.query, documents)

        return {"answer": response}
    
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))