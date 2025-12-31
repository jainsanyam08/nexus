from fastapi import FastAPI
import uvicorn
import os

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