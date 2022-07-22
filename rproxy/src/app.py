from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response as FastapiResponse
from typing import Any, Dict, Final, Optional
from requests import Response as RequestsResponse, get, post
from pydantic import BaseModel
from urllib.parse import quote as url_escape
from os import environ
from re import sub, escape


app: Final = FastAPI()
stac_host: Final = environ.get("STAC_HOST", "stac")
stac_prefix: Final = "/stac"


class UnformattedResponse(BaseModel):
    content: Any
    headers: Dict[str, str]
    status_code: int


def returnable_response(response: RequestsResponse) -> FastapiResponse:
    return FastapiResponse(
        content=response.content,
        headers=response.headers,
        status_code=response.status_code,
    )


def strip_prefix(path: str) -> str:
    return sub(rf"^{escape(stac_prefix)}", "", path)


def issue_get(
    path: str,
    query_params: Optional[Dict[str, Any]] = {},
    headers: Optional[Dict[str, str]] = {},
) -> FastapiResponse:
    requests_response = get(
        "http://{host}{path}{query_string}".format(
            host=stac_host,
            path=strip_prefix(path),
            query_string="?{0}".format(
                "&".join([
                    f"{key}={url_escape(value)}"
                    for key, value
                    in query_params.items()
                ])
            ) if query_params else ""
        ),
        headers=headers,
    )
    return returnable_response(requests_response)


def issue_post(
    path: str,
    body: Optional[str] = "",
    headers: Optional[Dict[str, str]] = {},
) -> FastapiResponse:
    stripped_path = strip_prefix(path)
    requests_response = post(
        f"http://{stac_host}{stripped_path}",
        data=body,
        headers=headers,
    )
    return returnable_response(requests_response)


@app.get("{full_path:path}")
async def get_all(
    full_path: str,
    request: Request,
):
    return issue_get(
        path=full_path,
        query_params=dict(request.query_params),
        headers=dict(request.headers),
    )


@app.post("{full_path:path}")
async def post_all(
    full_path: str,
    request: Request,
):
    return issue_post(
        path=full_path,
        body=(await request.body()).decode("UTF-8"),
        headers=dict(request.headers),
    )


def custom_openapi():
    stac_openapi = get(f"http://{stac_host}/openapi.json").json()
    key_paths = "paths"
    stac_openapi[key_paths] = {
        f"{stac_prefix}{path}": info
        for path, info in stac_openapi[key_paths].items()
    }
    return stac_openapi


app.openapi = custom_openapi
