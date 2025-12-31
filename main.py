from fastapi import FastAPI
import uvicorn
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

print("SYS.PATH:", sys.path)

from app.database import Base, engine
from app.routes.identity import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nexus",
    description="Digital Identity Visibility",
    version="0.1"
)

app.include_router(router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)