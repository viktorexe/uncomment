from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .routes.process_route import router as process_router

app = FastAPI(
    title="Uncomment API",
    description="Advanced comment removal service for 10+ programming languages",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(process_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(content={
        "message": "Uncomment API is running",
        "version": "1.0.0",
        "status": "healthy"
    })

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return JSONResponse(content={
        "status": "healthy",
        "service": "uncomment-api",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)