# Tic Tac Toe

A very simple Python implementation of Tic Tac Toe with client / server architecture

It supports running on a web browser by transpiling the code to WebAssembly using [pygbag](https://pypi.org/project/pygbag/).
You can install pygbag in the active venv and run from the root directory of the project (this assumes that the active Python
is 3.12):

```shell
pip install pygbag
python -m pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl .
```

## Kafka

* [Download Kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/4.1.0/kafka_2.13-4.1.0.tgz).
* Create topic: `bin/kafka-topics.sh --create --topic tic-tac-toe --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`
* 