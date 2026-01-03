from fastapi import FastAPI

from app.controller.auth_controller import auth_router

app = FastAPI()
app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
