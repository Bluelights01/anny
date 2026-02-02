from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.login import router as login_router
from apis.friends import router as friends_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(login_router, prefix="/auth", tags=["Authentication"])
app.include_router(friends_router, prefix="/search", tags=["friends"])

@app.get("/")
def home():
    return {"message": "API is running"}