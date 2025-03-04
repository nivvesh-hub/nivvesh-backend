from fastapi import FastAPI
from routes.homepage import router as homepage_router
from routes.users import router as user_router
from db.connection import engine
from models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(homepage_router, prefix="/api", tags=["homepage"])
app.include_router(user_router, prefix="/api", tags=["users"])
