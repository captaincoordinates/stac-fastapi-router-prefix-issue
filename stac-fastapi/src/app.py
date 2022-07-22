from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from stac_fastapi.api.app import StacApi
from stac_fastapi.api.models import create_get_request_model, create_post_request_model
from stac_fastapi.extensions.core import (
    FieldsExtension,
    TokenPaginationExtension,
)
from stac_fastapi.pgstac.core import CoreCrudClient
from stac_fastapi.pgstac.config import Settings
from stac_fastapi.pgstac.db import close_db_connection, connect_to_db
from stac_fastapi.pgstac.types.search import PgstacSearch


settings = Settings()

extensions = [
    FieldsExtension(),
    TokenPaginationExtension(),
]
post_request_model = create_post_request_model(extensions, base_model=PgstacSearch)
api = StacApi(
    app=FastAPI(),
    settings=settings,
    extensions=extensions,
    client=CoreCrudClient(post_request_model=post_request_model),
    search_get_request_model=create_get_request_model(extensions),
    search_post_request_model=post_request_model,
    response_class=ORJSONResponse,
    middlewares=[],
    router=APIRouter(prefix="/router_prefix"),
)

app = api.app


@app.on_event("startup")
async def startup_event():
    await connect_to_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    await close_db_connection(app)
