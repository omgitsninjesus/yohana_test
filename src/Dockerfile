FROM python:3.11.2-slim-bullseye

# needed to capture stderr output
# https://github.com/bottlepy/bottle/issues/1130#issuecomment-478096704
# https://stackoverflow.com/a/59812588/109102
ENV PYTHONUNBUFFERED=1 
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY . /app

WORKDIR /app/src

