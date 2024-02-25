from uvicorn import run
from fastapi import FastAPI

from src.controllers.physics_controller import router as pys_router
from src.controllers.root_controller import router as root_router

# initialization
backend = FastAPI()

# routers
backend.include_router(root_router)
backend.include_router(pys_router)


if __name__ == "__main__":
    run(backend, host="localhost", port=443)