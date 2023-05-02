FROM python:3.11.3-alpine3.17

RUN apk add gcc g++ musl-dev libffi-dev py3-cffi
# py3-virtualenv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv/rpg_periodical_scrapers
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src/app
COPY . .

RUN pip install --upgrade pip
COPY ./requirements/prod.txt requirements/prod.txt
RUN pip install -r requirements/prod.txt

CMD python src/main.py $PORT $BOTFILE --host $HOST --waitleave $WAITLEAVE
