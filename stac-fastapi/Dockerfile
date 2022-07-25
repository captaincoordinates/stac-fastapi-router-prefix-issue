FROM python:3.10-slim-bullseye

RUN useradd --shell /bin/bash apiuser

COPY requirements.txt /
RUN pip install -r /requirements.txt

ARG DEBIAN_FRONTEND noninteractive
RUN apt-get update --fix-missing \
 && apt-get install -y --no-install-recommends \
   build-essential \
   git \
 && apt-get clean

WORKDIR /stac-branch
RUN git clone -b router_prefix --single-branch https://github.com/drnextgis/stac-fastapi.git
RUN pip install -e stac-fastapi/stac_fastapi/api \
 && pip install -e stac-fastapi/stac_fastapi/types \
 && pip install -e stac-fastapi/stac_fastapi/extensions \
 && pip install -e stac-fastapi/stac_fastapi/pgstac

COPY src /
WORKDIR /src

USER apiuser

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--reload"]