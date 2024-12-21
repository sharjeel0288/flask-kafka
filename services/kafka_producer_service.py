from confluent_kafka import Producer
import uuid
import time

class KafkaProducerService:
    def __init__(self, bootstrap_servers):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'flask-producer'
        }
        self.producer = Producer(self.config)

    def produce_message(self, topic, message):
        """Produce a single message to Kafka"""
        try:
            self.producer.produce(topic, value=message)
            self.producer.flush()  # Ensure the message is delivered
            return {"status": "success", "message": message}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def produce_messages(self, topic, num_messages=10):
        """Produce multiple messages with unique UUIDs"""
        results = []
        for _ in range(num_messages):
            message_id = uuid.uuid4()
            message = f"Message from id {message_id}"
            result = self.produce_message(topic, message)
            results.append(result)
            time.sleep(1)  # Delay for better simulation
        return results
