# Tic Tac Toe

A very simple multiplayer Python implementation of Tic Tac Toe wich can be played in local mode, with peer-to-peer connection, or using a Kafka topic for message exchange.

There is a *config.json* file at the root to configure the client:
* To run in local mode, set `local` to `true`.
* To run with peer-to-peer connection, set `sockets_host` to point to a given host:port (for example, `localhost:1234`).
* To use Kafka message exchange, set `kafka_url` and `kafka_topic`. This will only work if `sockets_host` is not set. You can create a local Kafka server by running `docker compose up -d` (Docker needs to  be installed with the compose plugin).

In local mode, `python main.py` must be triggered once to start playing. In the other cases, two instances must be launched,
selecting "X" on one to create a game and play as first player, and "O" on the other to join the existing game and play as
the second player.

It kind of supports running on a web browser by transpiling the code to WebAssembly using [pygbag](https://pypi.org/project/pygbag/).
For this, the game must be ran in local mode (check previous paragraph).
You can install pygbag in the active venv and run from the root directory of the project (this assumes that the active Python
is 3.12):

```shell
pip install pygbag
python -m pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl .
```

The web browser version has several issues, so it is not recommended.
