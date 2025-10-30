from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Config:
    local: bool = False
    kafka_url: str = ""
    kafka_topic: str = ""

    def __post_init__(self) -> None:
        if not self.local:
            assert self.kafka_url, "kafka_url must be provided"
            assert self.kafka_topic, "kafka_topic must be provided"


def load_config(filename: str) -> Config:
    try:
        with open(filename) as f:
            data = json.load(f)
        return Config(
            local=data.get("local", False),
            kafka_url=data.get("kafka_url", ""),
            kafka_topic=data.get("kafka_topic", ""),
        )
    except FileNotFoundError:
        return Config(local=True)
