import uvicorn
from fastapi import FastAPI
import uvicorn

from src.my_app import deployments_router

class MyApp:
    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(deployments_router.router)

    def run_my_app(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)