from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import models

app = FastAPI(title='ML & GenAI Model Registry')

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(models.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido al registro de modelos ML"}