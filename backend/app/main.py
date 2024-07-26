from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import gym, admin


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gym Booking API"}


app.include_router(admin.router)
app.include_router(gym.router)