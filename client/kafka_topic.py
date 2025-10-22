from kafka.admin import KafkaAdminClient, NewTopic


def create_topic(url: str, topic: str) -> None:
    client = KafkaAdminClient(bootstrap_servers=url)
    topic = NewTopic(
        name=topic,
        num_partitions=1,
        replication_factor=1,
    )
    try:
        client.create_topics([topic])
    finally:
        client.close()


def delete_topic(url: str, topic: str) -> None:
    client = KafkaAdminClient(bootstrap_servers=url)
    try:
        client.delete_topics([topic])
    finally:
        client.close()
