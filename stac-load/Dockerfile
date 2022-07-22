FROM python:3.10-slim-bullseye

ARG PGSTAC_VERSION
RUN pip install pypgstac[psycopg]==${PGSTAC_VERSION}

COPY /src /

CMD ["/src/load.sh"]