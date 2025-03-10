from fastapi import FastAPI
# from routes.homepage import router as homepage_router
from app.routes.users import router as user_router
from app.db.connection import engine
from app.db.connection import Base
import uvicorn

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Include routes
# app.include_router(homepage_router, prefix="/api", tags=["homepage"])
app.include_router(user_router, prefix="/api/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
