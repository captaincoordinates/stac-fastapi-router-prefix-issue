FROM python:3.10-slim-bullseye

RUN useradd --shell /bin/bash apiuser

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY src /
WORKDIR /src

USER apiuser

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
