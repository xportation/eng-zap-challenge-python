from fastapi import FastAPI

from portal_api import views, di


def create_app():
    container = di.Container()
    container.wire(modules=[views])

    app = FastAPI()
    app.container = container
    app.include_router(views.router)
    return app
