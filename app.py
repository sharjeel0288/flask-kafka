from flask import Flask, request, jsonify
from services.kafka_consumer_service import KafkaConsumerService
from services.kafka_producer_service import KafkaProducerService
from services.kafka_admin_service import KafkaAdminService
from models.message_model import MessageModel
from utils.kafka_config import DEFAULT_GROUP_ID, KAFKA_BOOTSTRAP_SERVERS

app = Flask(__name__)

# Initialize services
consumer_service = KafkaConsumerService(KAFKA_BOOTSTRAP_SERVERS,DEFAULT_GROUP_ID)
producer_service = KafkaProducerService(KAFKA_BOOTSTRAP_SERVERS)
admin_service = KafkaAdminService(KAFKA_BOOTSTRAP_SERVERS)

@app.route('/consume', methods=['GET'])
def consume_messages():
    """Endpoint to consume messages from Kafka."""
    # Extract topic and partition from query parameters
    topic = request.args.get('topic')
    partition = int(request.args.get('partition', 0))

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        # Consume messages from the provided topic and partition
        messages = consumer_service.consume_messages(topic, partition)
        # Return the structured messages
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/produce', methods=['POST'])
def produce_message():
    """Endpoint to produce a message to a Kafka topic."""
    data = request.get_json()
    
    # Extract topic and message from the request body
    topic = data.get('topic')
    message = data.get('message')

    if not topic or not message:
        return jsonify({"error": "Both topic and message are required"}), 400

    try:
        # Produce the message
        result = producer_service.produce_message(topic, message)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/topic', methods=['POST'])
def create_topic():
    """Endpoint to create a Kafka topic."""
    data = request.get_json()
    
    topic = data.get('topic')
    num_partitions = data.get('partitions', 1)
    replication_factor = data.get('replication_factor', 1)

    if not topic:
        return jsonify({"error": "Topic name is required"}), 400

    try:
        # Create the topic
        admin_service.create_topic(topic, num_partitions, replication_factor)
        return jsonify({"message": f"Topic '{topic}' created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/topic', methods=['DELETE'])
def delete_topic():
    """Endpoint to delete a Kafka topic."""
    topic = request.args.get('topic')

    if not topic:
        return jsonify({"error": "Topic name is required"}), 400

    try:
        # Delete the topic
        admin_service.delete_topic(topic)
        return jsonify({"message": f"Topic '{topic}' deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/partitions', methods=['POST'])
def create_partition():
    """Endpoint to add partitions to an existing topic."""
    data = request.get_json()
    
    topic = data.get('topic')
    num_partitions = data.get('partitions', 1)

    if not topic:
        return jsonify({"error": "Topic name is required"}), 400

    try:
        # Add partitions to the topic
        admin_service.add_partitions(topic, num_partitions)
        return jsonify({"message": f"Added {num_partitions} partitions to '{topic}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
