# rpg-bot-periodical-scraper

*Note: this demo project aims more to add features than to achieve
test coverage.*

General documentation for the RPG can be found in the [master
repo](https://github.com/kirkiano/rpg-docker).

This repo provides the bots that scrape headlines or titles from various
periodicals and announces them in specific addresses in the RPG.

## Invocation

The Makefile includes targets that run the program, with or without
Docker. Command-line arguments are explained by running
`python src/main.py -h`. Note that `waitleave`, the maximum time a bot
will wait before moving to a neighbor, should be set long enough to
give the asynchronous tasks time to respond to the server's pings,
otherwise the server will time the connection out. (That timeout too
should be set long enough.) 

## Environment variables

- `LOG_LEVEL` should be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`,
  or `CRITICAL`. If absent, the log level defaults to `INFO`.

## TODO

See the `TODO` file for outstanding items.
