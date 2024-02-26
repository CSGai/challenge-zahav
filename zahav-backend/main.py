from uvicorn import run
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.controllers.physics_controller import router as pys_router
from src.controllers.root_controller import router as root_router

# initialization
backend = FastAPI()

# add cors middleware to allow back to front communications

origins = [
    "http://localhost:5173",
]

backend.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# routers
backend.include_router(root_router)
backend.include_router(pys_router)


if __name__ == "__main__":
    run(backend, host="localhost", port=443)