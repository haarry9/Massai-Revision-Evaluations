from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.config.settings import settings

# Create FastAPI app
app = FastAPI(
    title="Product Research RAG System",
    description="AI-powered product research using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["rag"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Product Research RAG System",
        "docs": "/docs",
        "health": "/api/health"
    }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "src.main:app",
#         host=settings.api_host,
#         port=settings.api_port,
#         reload=True
#     )