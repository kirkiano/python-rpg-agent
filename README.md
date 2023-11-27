# RPG periodical scrapers

General documentation for the RPG can be found in the [master
repo](https://github.com/kirkiano/rpg-docker).

This repo provides the bots that scrape titles from various
periodicals and announces them in certain addresses in the RPG.
Python version 3.11.3.

## Execution

### Virtual environment

```
python -m venv <path/to/venv>
workon <venv>
pip install -r requirements/dev.txt
```

### Environment variables

The Makefile searches `.env` for the following environment variables,
some of which are passed as command-line arguments to the executable:
* `HOST`: hostname of the server (*ie*, the auth driver)
* `PORT`: port number on which the server (auth driver) listens for TCP connections
* `BOTFILE`: path to the bot file. Information about its expected format is
  shown by running `python src/main.py -h`.
* `WAITLEAVE`: maximum number of seconds a bot will wait before moving
* `WAIT_BETWEEN_RECONNECTS`: number of seconds to wait before trying again to
  connect to the server
* `LOG_LEVEL_TOP` (optional; default `INFO`): threshold for logging top-level events
* `LOG_LEVEL_BOT` (optional; default `INFO`): threshold for logging top-level events within a bot
* `LOG_LEVEL_ROAM` (optional; default `INFO`): threshold for logging a bot's motion
* `LOG_LEVEL_SPEECH` (optional; default `WARNING`): threshold for logging a bot's speech
* `LOG_LEVEL_TCP` (optiona; default `WARNING`): threshold for logging bytes sent and received

A log level should be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.

### Invocation

Activate the virtualenv, set the above env vars in `.env`, and
enter `make run`. Command-line arguments are explained by running
`python src/main.py -h`.

## Testing

`make test`

## Docker

```
cd docker/prod
make
```

## Docs

Run `make doc` then navigate to `sphinx/build/html/index.html`.

## TODO

See `TODO`.
