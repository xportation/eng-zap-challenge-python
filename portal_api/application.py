from fastapi import FastAPI

from portal_api import views


def create_app():
    app = FastAPI()
    app.include_router(views.router)
    return app
