from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.llm_config import get_settings
from app.config.log_config import logger
from app.routes.navigate import router as api_router

# -------------------------------------------------
# App Initialization
# -------------------------------------------------

app = FastAPI(title="Agentic Web Automation API")

# Allow Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

app.include_router(api_router)