from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from api.models.chat import ChatRequest
from dotenv import load_dotenv
from pathlib import Path
import ollama
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("api.log")
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = Path('api/.env')
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI(docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")  
router = APIRouter()

API_URL = os.getenv("API_URL")
max_length = os.getenv("MAX_LENGTH")
OLLAMA_URL = os.getenv("OLLAMA_URL")

# Log initialization
logger.info(f"Starting application with Ollama URL: {OLLAMA_URL}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[API_URL], 
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Initialize Ollama client
try:
    client = ollama.Client(host=OLLAMA_URL)
    logger.info("Successfully initialized Ollama client")
except Exception as e:
    logger.error(f"Failed to initialize Ollama client: {str(e)}")
    client = None

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP exception: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": f"Message is too long! Please keep it under {max_length} characters."
        })

@router.get("/api/health")
async def health_check():
    try:
        if client:
            client.list()
            return {"status": "ok", "ollama_status": "connected"}
        else:
            return {"status": "degraded", "ollama_status": "not initialized"}
    except Exception as e:
        logger.error(f"Health check failed for Ollama: {str(e)}")
        return {"status": "degraded", "ollama_status": "unavailable"}

@router.post("/api/chat")
async def chat(request: ChatRequest):
    logger.info(f"Received chat request")
    
    if not client:
        logger.error("Ollama client not initialized")
        raise HTTPException(
            status_code=503, 
            detail="Chat service is currently unavailable. Please try again later."
        )
    
    try: 
        logger.info(f"Sending request to Ollama model 'gunther'")
        response = client.chat(
            model='gunther',
            messages=[{"role": "user", "content": request.message}],
        )
        logger.info("Successfully received response from Ollama")
        content = response["message"]["content"]
        return {"message": content}
        
    except ollama.ResponseError as e:
        error_msg = f"Ollama response error: {e.error}, code: {e.status_code}"
        logger.error(error_msg)
        
        if e.status_code == 404:
            user_message = "The requested AI model was not found. Please check if 'gunther' is available."
        elif e.status_code == 400:
            user_message = "There was a problem with your request. The input may be invalid."
        elif e.status_code >= 500:
            user_message = "The AI service is experiencing issues. Please try again later."
        else:
            user_message = "An unexpected error occurred while processing your request."
            
        raise HTTPException(status_code=e.status_code, detail=user_message)
        
    except ConnectionError as e:
        error_msg = f"Connection error with Ollama: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the AI service. It may be down or unreachable."
        )
        
    except TimeoutError as e:
        error_msg = f"Timeout error with Ollama: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again later."
        )
        
    except Exception as e:
        error_msg = f"Unexpected error in chat endpoint: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Our team has been notified."
        )


app.include_router(router)