from confluent_kafka.admin import AdminClient, NewTopic

class KafkaAdminService:
    def __init__(self, bootstrap_servers):
        self.admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    def list_topics(self):
        """List all topics"""
        try:
            metadata = self.admin_client.list_topics(timeout=10)
            return {"status": "success", "topics": list(metadata.topics.keys())}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        """Create a new topic"""
        try:
            new_topic = NewTopic(topic_name, num_partitions, replication_factor)
            self.admin_client.create_topics([new_topic])
            return {"status": "success", "topic": topic_name}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def delete_topic(self, topic_name):
        """Delete a topic"""
        try:
            self.admin_client.delete_topics([topic_name])
            return {"status": "success", "topic": topic_name}
        except Exception as e:
            return {"status": "error", "error": str(e)}
