from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.core.database import engine


app = FastAPI(
    title="Support Ticket Management System",
    version="1.0.0"
)


app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Support Ticket Management System API is running"
    }


@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "success": True,
        "message": "Database connection successful",
        "result": result.scalar()
    }