# syntax=docker/dockerfile:1
FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
RUN --mount=type=secret,id=system_ca,required=true \
    apt-get -o Acquire::https::CaInfo=/run/secrets/system_ca update && \
    DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::https::CaInfo=/run/secrets/system_ca install -y --no-install-recommends \
    ca-certificates curl git python3 python3-venv xz-utils && \
    rm -rf /var/lib/apt/lists/*
RUN --mount=type=secret,id=system_ca,required=true \
    curl --cacert /run/secrets/system_ca --fail --location --silent --show-error \
    https://nodejs.org/dist/v24.19.0/node-v24.19.0-linux-x64.tar.xz -o /tmp/node.tar.xz && \
    curl --cacert /run/secrets/system_ca --fail --location --silent --show-error \
    https://nodejs.org/dist/v24.19.0/SHASUMS256.txt -o /tmp/node-shasums && \
    awk '$2 == "node-v24.19.0-linux-x64.tar.xz" {print $1 "  /tmp/node.tar.xz"}' /tmp/node-shasums | sha256sum -c - && \
    tar -xJf /tmp/node.tar.xz -C /usr/local --strip-components=1 && \
    rm /tmp/node.tar.xz /tmp/node-shasums
