from fastapi import FastAPI
#------------------------------------
from database import Base, engine
#from app.database import Base, engine -> Use this when running locally
#-------------------------------------
from routes import quiz_routes 
#from app.routes import quiz_routes -> Use this when running locally
#-------------------------------------
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(quiz_routes.router)
