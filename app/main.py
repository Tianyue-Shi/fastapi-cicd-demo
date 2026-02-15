from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import close_mongo_connection, connect_to_mongo
from app.routes.health import router as health_router
from app.routes.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events."""
    # Startup: connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: close the MongoDB connection
    await close_mongo_connection()


app = FastAPI(
    title="FastAPI CI/CD Demo",
    description="A demo API for learning CI/CD pipelines",
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(health_router)
app.include_router(items_router)


@app.get("/")
async def root():
    """Root endpoint -- returns a welcome message."""
    return {"message": "Welcome to FastAPI CI/CD Demo"}