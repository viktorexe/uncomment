from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.routes.process_route import router as process_router

app = FastAPI(
    title="Uncomment API",
    description="Advanced comment removal service",
    version="1.0.0"
)

# CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(process_router)

@app.get("/")
async def root():
    return {"message": "Uncomment API", "status": "running"}

# Vercel serverless handler
handler = app