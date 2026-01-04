from fastapi import FastAPI

from app.controller.auth_controller import auth_router
from app.controller.task_controller import task_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(task_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
