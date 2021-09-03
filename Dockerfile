FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1 COLUMNS=200 TZ=Asia/Almaty
# Add alpine mirrors
RUN sed -i 's/dl-cdn.alpinelinux.org/mirror.neolabs.kz/g' \
    /etc/apk/repositories && \
# Set timezone
    apk add tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Almaty /etc/localtime && \
    echo "Asia/Almaty" > /etc/timezone && \
# Add system dependencies
    apk update && \
    apk add bash build-base alpine-sdk libmagic jpeg-dev openjpeg-dev postgresql-client \
    gcc libc-dev postgresql-dev gettext \
    make git libffi-dev openssl-dev python3-dev \
    libxml2-dev libxslt-dev curl
# Adds our application code to the image
WORKDIR /src
# Adds our application src to the image
RUN pip install --upgrade pip
# Install project dependencies
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY ./project /src