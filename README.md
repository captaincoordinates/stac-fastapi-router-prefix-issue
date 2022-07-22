# stac-fastapi Router Prefix Issue

This repo demonstrates a problem in [stac-fastapi](https://github.com/stac-utils/stac-fastapi) with router prefixes in path handling.

## To Reproduce
1. docker-compose up
2. navigate to http://localhost:8080/docs in browser
3. observe all paths start with `/router_prefix`
4. execute GET on landing page endpoint
    1. `curl -X 'GET' 'http://localhost:8080/router_prefix/' -H 'accept: application/json'`
5. observe all `href` properties exclude `/router_prefix`
6. execute GET on search endpoint, passing `limit=1` (there are two items in the STAC catalog)
    1. `curl -X 'GET' 'http://localhost:8080/router_prefix/search?limit=1' -H 'accept: application/geo+json'`
7. observe `next` and `self` `href` properties in response's `links` section include `/router_prefix` while `root` `href` properties does not
