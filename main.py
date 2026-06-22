from routes.ai_routes import router as ai_router
from routes.auth_routes import router as auth_router
from fastapi import FastAPI
from routes.leads import router
from database import engine
from models import Base

app = FastAPI()
app.include_router(ai_router)

Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(auth_router)

@app.get("/")
def home():

    return {
        "message":"CloudBot Running"
    }