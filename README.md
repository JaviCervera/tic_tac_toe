# Tic Tac Toe

A very simple Python implementation of Tic Tac Toe with client / server architecture.

The server is stateless. All game state must be shared between the players (in local mode, state is shared directly
between players; in server mode, a Kafka topic is used).

There is a *config.json* file at the root to configure the client. To run in local mode, set `local` to `true`.
To play using a Flask server and a Kafka topic, the simplest approach is to install Docker and run `docker compose up -d`.

In local mode, `python main.py` must be triggered once to start playing. When using a server, two instances must be launched,
selecting "X" on one to create a game and play as first player, and "O" on the other to join the existing game and play as
the second player.

It supports running on a web browser by transpiling the code to WebAssembly using [pygbag](https://pypi.org/project/pygbag/).
For this, the game must be ran in local mode (check previous paragraph).
You can install pygbag in the active venv and run from the root directory of the project (this assumes that the active Python
is 3.12):

```shell
pip install pygbag
python -m pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl .
```

## Kafka setup

> NOTE: These are old instructions, you should use `docker compose up -d` to launch Flask and Kafka servers now.

* [Download Kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/4.1.0/kafka_2.13-4.1.0.tgz).
* Decompress the package and cd into Kafka's dir.
* Generate cluster UUID: `KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"`
* Format log directories: `bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties`
* Start server: `bin/kafka-server-start.sh config/server.properties`

Then, start two instances of *main.py*, selecting X in one and O in the other to have the two players.

## TODO

* Kafka deployment on https://www.confluent.io/confluent-cloud/.
* Check web render offset (input is at top left, rendering is at bottom left).
