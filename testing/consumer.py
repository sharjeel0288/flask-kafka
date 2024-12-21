from confluent_kafka import Consumer, KafkaException, KafkaError
import uuid
import time

class KafkaConsumerService:
    def __init__(self, bootstrap_servers='localhost:9092', group_id='consumer-group'):
        self.config = {
            'bootstrap.servers': bootstrap_servers,  # Ensure the correct IP/hostname for the Kafka broker
            'group.id': group_id,
            'auto.offset.reset': 'earliest',  # Start reading from the beginning if no offset
            'session.timeout.ms': 6000,
            'enable.auto.commit': False,  # Optionally disable auto-commit for finer control over message processing
        }
        self.consumer = Consumer(self.config)

    def consume_messages(self, topic='KafkaPublisher'):
        # Subscribing to the Kafka topic
        self.consumer.subscribe([topic])

        try:
            while True:
                # Polling for new messages
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue  # No message available yet

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition reached, which is normal when there are no more messages in the partition
                        print(f"End of partition reached: {msg.partition} at offset {msg.offset()}")
                    else:
                        # If another error occurs, raise the exception
                        raise KafkaException(msg.error())
                else:
                    # Successfully received a message, now process it
                    message_value = msg.value().decode('utf-8')
                    messages = message_value.split(' ')

                    # Example: Assuming the 4th part is the ID, you can change this logic based on your message format
                    consumed_message = {
                        'Id': str(uuid.UUID(messages[3])),  # Assuming the 4th part is the ID
                        'Message': message_value,
                        'Topic': msg.topic(),
                        'Partition': msg.partition(),
                        'Offset': msg.offset()
                    }

                    # Logging consumed message details
                    print(f"Consumed message: {message_value} from topic {msg.topic()} at partition {msg.partition()} and offset {msg.offset()}")
                    time.sleep(1)  # Adding a slight delay between messages for better simulation

        except KafkaException as e:
            print(f"Error while consuming messages: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            # Closing the consumer connection
            self.consumer.close()

if __name__ == "__main__":
    consumer_service = KafkaConsumerService()  # Update the bootstrap server as needed
    consumer_service.consume_messages()
