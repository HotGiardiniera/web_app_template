FROM python:3.12-bookworm
LABEL authors="chm"

COPY ./app /web/app
WORKDIR /web/app

RUN apt update
RUN apt upgrade -y

RUN pip install --upgrade pip

RUN pip install pip-tools==7.3.0 # For requirements compiling
RUN pip install ipython
RUN pip install -r ./requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/docker-bashrc /root/.bashrc
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/web

ENTRYPOINT ["/entrypoint.sh"]

