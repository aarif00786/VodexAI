import uvicorn
from fastapi import FastAPI
from app.routers import item_route, record_route

def create_app():
    app = FastAPI()
    # Include routers
    app.include_router(item_route.router, prefix="/item", tags=["item"])
    app.include_router(record_route.router, prefix="/record", tags=["records"])
    return app

# Create the app instance
app = create_app()

def main():
    uvicorn.run(
        "main:app",  # Refers to the app object
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=4,
        log_level='debug'
    )

if __name__ == "__main__":
    main()
