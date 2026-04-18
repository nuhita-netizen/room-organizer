import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api.endpoints import router as api_router

# Ensure required runtime directories exist (e.g. on Render where gitignored dirs are absent)
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/results", exist_ok=True)

app = FastAPI(title="Room Architecture AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")

