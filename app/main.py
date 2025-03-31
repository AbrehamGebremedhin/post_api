"""
Main application module.
This module initializes and configures the FastAPI application.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routes import auth, posts
from app.api.utils.database import init_db

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Post API",
    description="A FastAPI-based API for managing posts",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """
    Execute startup events.
    """
    # Initialize the database
    init_db()

@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: A message indicating the API is running.
    """
    return {"message": "Post API is running"}

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run("app.main:app", host=host, port=port, reload=debug) 