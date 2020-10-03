FROM python:3.7.9-slim 

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

COPY .tox/dist/ .

RUN /venv/bin/pip install --disable-pip-version-check *.tar.gz

ENV PATH=$PATH:/venv/bin

WORKDIR /work

ENTRYPOINT ["/bin/sh"]

USER 1001

LABEL name={NAME}
LABEL version={VERSION}