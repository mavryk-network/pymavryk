FROM python:3.12-slim-bookworm

ARG NB_USER=mickey
ARG NB_UID=1000

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential pkg-config libsodium-dev libgmp-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . /tmp/pymavryk
RUN pip install 'notebook>=7.0' jupyter-client /tmp/pymavryk

ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

USER ${NB_USER}
RUN michelson-kernel install

USER root
COPY binder/*.ipynb ${HOME}/
RUN chown -R ${NB_USER}:${NB_USER} ${HOME}/

WORKDIR ${HOME}
USER ${USER}

EXPOSE 8888
ENTRYPOINT []
