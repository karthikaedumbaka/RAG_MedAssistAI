from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your modules
try:
    from middlewares.exception_handlers import catch_exception_middleware
except ImportError:
    # Fallback exception handler
    from fastapi import Request
    from fastapi.responses import JSONResponse
    import traceback
    import logging
    
    logger = logging.getLogger(__name__)
    
    async def catch_exception_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled error: {e}\n{traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )

try:
    from routes.upload_pdf import router as upload_router
    from routes.ask_question import router as ask_router
except ImportError as e:
    print(f"Import error: {e}")
    print("Creating fallback routers...")
    
    # Create fallback routers
    from fastapi import APIRouter
    
    upload_router = APIRouter()
    ask_router = APIRouter()
    
    @upload_router.post("/upload_pdfs/")
    async def upload_pdfs_fallback():
        return {"error": "Upload functionality not available - check imports"}
    
    @ask_router.post("/ask/")
    async def ask_question_fallback():
        return {"error": "Ask functionality not available - check imports"}

# Create FastAPI app
app = FastAPI(
    title="Medical AI Assistant",
    description="Chatbot for Medical AI Assistant",
    version="1.0.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add exception handling middleware
app.middleware("http")(catch_exception_middleware)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Medical AI Assistant API", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(upload_router, tags=["upload"])
app.include_router(ask_router, tags=["chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)