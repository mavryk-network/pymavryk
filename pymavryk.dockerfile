FROM python:3.12-alpine3.17 AS compile-image
RUN apk add --update --no-cache \
	build-base \
	libtool \
	autoconf \
	automake \
	python3-dev \
	libffi-dev \
	gmp-dev \
	libsodium-dev

RUN python -m venv --without-pip --system-site-packages /opt/pymavryk \
    && mkdir -p /opt/pymavryk/src/pymavryk/ \
    && touch /opt/pymavryk/src/pymavryk/__init__.py \
    && mkdir -p /opt/pymavryk/src/michelson_kernel/ \
    && touch /opt/pymavryk/src/michelson_kernel/__init__.py
WORKDIR /opt/pymavryk
ENV PATH="/opt/pymavryk/bin:$PATH"
ENV PYTHON_PATH="/opt/pymavryk/src:$PATH"

COPY pyproject.toml requirements.slim.txt README.md /opt/pymavryk/

RUN /usr/local/bin/pip install --prefix /opt/pymavryk --no-cache-dir --disable-pip-version-check --no-deps -r /opt/pymavryk/requirements.slim.txt -e .

FROM python:3.12-alpine3.17 AS build-image
RUN apk add --update --no-cache \
	binutils \
	gmp-dev \
	libsodium-dev

RUN adduser -D pymavryk
USER pymavryk
ENV PATH="/opt/pymavryk/bin:$PATH"
ENV PYTHONPATH="/home/pymavryk:/home/pymavryk/src:/opt/pymavryk/src:/opt/pymavryk/lib/python3.12/site-packages:$PYTHONPATH"
WORKDIR /home/pymavryk/
ENTRYPOINT ["python"]

COPY --chown=pymavryk --from=compile-image /opt/pymavryk /opt/pymavryk
COPY --chown=pymavryk . /opt/pymavryk
