from confluent_kafka import Producer
import uuid
import time

class KafkaProducerService:
    def __init__(self, bootstrap_servers='localhost:9092'):  # Use 9092 if Kafka Broker
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'producer-client'
        }
        self.producer = Producer(self.config)

    def produce_messages(self, topic='KafkaPublisher', num_messages=10):
        results = []
        
        for _ in range(num_messages):
            # Generate a new UUID for each message
            message_id = uuid.uuid4()
            message_value = f"message from id {message_id}"
            
            # Produce the message to the specified topic
            self.producer.produce(topic, value=message_value)
            
            # Wait for the message to be delivered (flush)
            self.producer.flush()
            
            # Log the produced message
            print(f"Produced message: {message_value}")
            
            # Store the result in a dictionary
            result_obj = {
                'Topic': topic,
                'Message': message_value,
                'Guid': message_id
            }
            results.append(result_obj)
            time.sleep(1)  # Adding a slight delay between messages for better simulation

        return results

if __name__ == "__main__":
    producer_service = KafkaProducerService()
    producer_service.produce_messages()
