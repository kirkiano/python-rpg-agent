FROM python:3.11.3-alpine3.17

RUN apk add gcc g++ musl-dev libffi-dev py3-cffi
# py3-virtualenv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv/rpg_periodical_scrapers
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV APP_REPO=/usr/src/periodical-scraper
WORKDIR $APP_REPO/app

RUN pip install --upgrade pip
COPY ./requirements/prod.txt requirements/prod.txt
RUN pip install -r requirements/prod.txt

CMD python src/main.py $PORT $APP_REPO/botfile --host $HOST \
        --waitleave $WAITLEAVE \
        --wait-between-reconnects $WAIT_BETWEEN_RECONNECTS
