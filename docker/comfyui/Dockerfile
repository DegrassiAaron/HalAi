# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    COMFYUI_HOME=/opt/ComfyUI

ARG COMFYUI_GIT_REPO=https://github.com/comfyanonymous/ComfyUI.git
ARG COMFYUI_GIT_REF=master

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${COMFYUI_HOME}

RUN git clone --branch "${COMFYUI_GIT_REF}" --depth 1 "${COMFYUI_GIT_REPO}" "${COMFYUI_HOME}"

WORKDIR ${COMFYUI_HOME}

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8188

ENV CLI_ARGS=""

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD []
