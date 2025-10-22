# Tic Tac Toe

A very simple Python implementation of Tic Tac Toe with client / server architecture.

The server is stateless. All game state must be shared between the players (by default, a Kafka topic
is used for this).

Also, the game can be ran in local mode, simply by removing the comment on the first line of the `create_game`
function on *main.py*:

```python
# return TicTacToeGameLocal()
```

It supports running on a web browser by transpiling the code to WebAssembly using [pygbag](https://pypi.org/project/pygbag/).
For this, the game must be ran in local mode (check previous paragraph).
You can install pygbag in the active venv and run from the root directory of the project (this assumes that the active Python
is 3.12):

```shell
pip install pygbag
python -m pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl .
```

## Kafka

* [Download Kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/4.1.0/kafka_2.13-4.1.0.tgz).
* Decompress the package and cd into Kafka's dir.
* Generate cluster UUID: `KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"`
* Format log directories: `bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties`
* Start server: `bin/kafka-server-start.sh config/server.properties`

Then, start two instances of *main.py*, selecting X in one and O in the other to have the two players.

## TODO

* Logging.
* Server deployment on Render or Railway.
* Check web render offset (input is at top left, rendering is at bottom left).
* Code cleanup.
