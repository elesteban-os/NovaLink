from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.workers.response_consumer import start_gateway_response_consumer

app = FastAPI(
    title="NovaLink API Gateway",
    description="Translate frontend HTTP requests into RabbitMQ events and expose polling endpoints.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup_event() -> None:
    """Start the response consumer when the gateway begins."""
    start_gateway_response_consumer()

@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "api-gateway"}

@app.get("/", tags=["info"])
def root() -> dict[str, str]:
    return {"service": "api-gateway", "version": "0.1.0", "docs": "/docs"}
