from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
import uvicorn
from .routes import user, auth, message, room
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

origin = ['*']

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/message_media", StaticFiles(directory="message_media"),
          name="message_media")

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


# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
