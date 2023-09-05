from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi_pagination import add_pagination
from config import settings
from routers.presence_history import router


app = FastAPI(title="Presence Service")

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
app.include_router(router)
add_pagination(app)
