from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import interview_route
from app.database import engine, Base
from app.models import interview, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://app.localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(interview_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
