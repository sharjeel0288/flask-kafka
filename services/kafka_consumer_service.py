import uuid
from confluent_kafka import Consumer, KafkaException, KafkaError, TopicPartition
import time

class KafkaConsumerService:
    def __init__(self, bootstrap_servers, group_id):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        }
        self.consumer = Consumer(self.config)

    def consume_messages(self, topic, partition=None, timeout=10):
        """Consume messages from a topic or a specific partition"""
        try:
            if partition is not None:
                # Assign specific partition if provided
                self.consumer.assign([TopicPartition(topic, partition)])
            else:
                # Subscribe to topic if partition is not provided
                self.consumer.subscribe([topic])

            messages = []
            start_time = time.time()
            while time.time() - start_time < timeout:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        raise KafkaException(msg.error())
                else:
                    messages.append({
                        'message': msg.value().decode('utf-8'),
                        'topic': msg.topic(),
                        'partition': msg.partition(),
                        'offset': msg.offset(),
                        'Timestamp': msg.timestamp(),
                        'Key': msg.key(),
                    # 'Id': str(uuid.UUID(msg.value())),

                    })
               
            return {"status": "success", "messages": messages}
        except Exception as e:
            return {"status": "error", "error": str(e)}
        finally:
            self.consumer.close()
