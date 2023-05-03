# Periodical scrapers

*Note: this demo project aims more to add features than to achieve
test coverage.*

General documentation for the RPG can be found in the [master
repo](https://github.com/kirkiano/rpg-docker).

This repo provides the bots that scrape headlines or titles from various
periodicals and announces them in specific addresses in the RPG.

## Execution

### Virtual environment

Activate the appropriate virtualenv: `workon <venv>`.

To create a new one:
```
python -m venv <path/to/venv>
workon <venv>
pip install -r requirements/dev.txt
```

### Environment variables

The following environment variables are sought for in `.env`; see `.envs/sample`.
(See `Makefile` for how they are passed on the command line.)
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

A log level should be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`,
or `CRITICAL`.


### Invocation

After activating the virtualenv and setting env vars in `.env`, enter `make run`.
Command-line arguments are explained by running `python src/main.py -h`.

Note that `waitleave`, the maximum time a bot will wait before moving,
should be set long enough to give the asynchronous tasks time to respond
to the server's pings, otherwise the server will time the connection out.
(That timeout too should be set long enough.)

## Testing

`make test`

## Docker

```
cd docker/prod
make
```

## TODO

See `TODO`.
