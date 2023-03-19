from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from .routes import user, auth, message
from fastapi.middleware.cors import CORSMiddleware

# from .database import engine
# from app.Models import user

# user.Base.metadata.create_all(bind=engine)
origin = ['*']

app = FastAPI()
app.mount("/media", StaticFiles(directory="../media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Route:
    def __init__(self, *args) -> None:
        [app.include_router(keys.router) for keys in args]


app_route = Route(user, auth, message)


@app.get('/')
def root():
    return {'message': 'Welcome'}
