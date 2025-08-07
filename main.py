# main.py

from fastapi import FastAPI, Form
from app import models
from app.database import engine
from app.routers import users, roles, permissions
from app.routes import router
from fastapi.responses import JSONResponse
from app.auth import create_access_token

# Optional: ensure tables are created without using Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SACRED: Smart Access Control with Role Encapsulated Design",
    description="A secure, flexible role and permission-based access control system.",
    version="1.0.0"
)

app.include_router(router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)

@app.get("/")
def root():
    return {"message": "SACRED access control service is running"}

@app.post("/token")
def generate_token_for_testing(user_id: int = Form(...)):
    token = create_access_token({"sub": str(user_id)})
    return JSONResponse({"access_token": token, "token_type": "bearer"})

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
