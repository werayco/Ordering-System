import json
import logging
from confluent_kafka import Consumer, Producer
from app.services.elasticsearch_client import elasticsearch_client
from app.config import settings
from app.utils import deserialize_from_json

logger = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer({
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": "search-service",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        })
        self.dlq_producer = Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})

    async def consume(self):
        self.consumer.subscribe(["inventory"])
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue

                if msg.error():
                    logger.error(f"Kafka error: {msg.error()}")
                    continue

                key_bytes = msg.key()
                value_bytes = msg.value()

                try:
                    key = key_bytes.decode() if key_bytes else None
                    value = deserialize_from_json(value_bytes)
                    await elasticsearch_client.crud_document(key,value)
                    self.consumer.commit(msg)
                except Exception as e:
                    logger.error(f"Failed to process message at offset {msg.offset()}: {e}")
                    self._send_to_dlq(key_bytes, value_bytes, str(e))
                    self.consumer.commit(msg) 

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()


    def _send_to_dlq(self, key_bytes, value_bytes, error: str):
        try:
            self.dlq_producer.produce(
                topic="inventory.dlq",
                key=key_bytes,
                value=json.dumps({
                    "original_value": value_bytes.decode(errors="replace") if value_bytes else None,
                    "error": error,
                }).encode(),
            )
            self.dlq_producer.flush()
        except Exception as dlq_err:
            logger.critical(f"Failed to publish to DLQ, message permanently lost: {dlq_err}")

