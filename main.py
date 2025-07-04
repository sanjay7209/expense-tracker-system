import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Request
from api import api_router
from master_data import master_api_router
import uvicorn

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Expense Management System')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],                                                                    
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(api_router)
app.include_router(master_api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Expense Management System"}


if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)


