FROM python:3.12-slim-bookworm

ARG NB_USER=mickey
ARG NB_UID=1000

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential pkg-config libsodium-dev libgmp-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . /tmp/pymavryk
RUN pip install notebook jupyter-client /tmp/pymavryk
RUN michelson-kernel install

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY *.ipynb ${HOME}/
RUN chown -R ${NB_USER}:${NB_USER} ${HOME}/

WORKDIR ${HOME}
USER ${USER}

EXPOSE 8888
ENTRYPOINT []
