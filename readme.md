Here is a detailed `README.md` file that covers setting up the project, changing the IP, starting Kafka with Docker, running the Flask app, and testing the APIs:

```markdown
# Kafka Flask Application

This project provides a Flask application that interacts with Kafka for message production and consumption. It includes endpoints to produce messages to Kafka topics, consume messages from Kafka topics, and manage Kafka topics and partitions.

## Prerequisites

- Docker
- Kafka Broker running on `localhost:9092`
- Python 3.7+ and `pip` installed

## Project Structure

```
/kafka-flask-app
│
├── app.py                       # Flask application entry point
├── services/
│   ├── kafka_consumer_service.py  # Kafka consumer service
│   ├── kafka_producer_service.py  # Kafka producer service
│   └── kafka_admin_service.py     # Kafka admin service for managing topics/partitions
│
├── models/
│   ├── __init__.py               # Models import
│   └── message_model.py          # Message data model (optional)
│
├── utils/
│   ├── __init__.py               # Utility module
│   └── kafka_config.py           # Kafka configuration
│
├── docker-compose.yml            # Docker Compose configuration for Kafka
└── requirements.txt              # Python dependencies
```

## Setup

### 1. **Clone the Repository**

Clone the repository to your local machine:

```bash
git clone <repository_url>
cd kafka-flask-app
```

### 2. **Update Kafka IP in Configuration**
Make sure that the IP address in `kafka_config.py` matches your Kafka broker's IP.

- Open the file `utils/kafka_config.py` and change the default Kafka IP address (if necessary):
  
```python
BOOTSTRAP_SERVERS = 'localhost:9092'  # Change this if Kafka is hosted elsewhere
```

### 3. **Set Up Kafka with Docker**
This project includes a `docker-compose.yml` file to set up a Kafka broker. Follow these steps to set up Kafka using Docker:

- Ensure you have Docker and Docker Compose installed on your machine.

- Run the following command to start Kafka using Docker Compose:

```bash
docker-compose up -d
```

This will start Kafka and Zookeeper containers. Kafka will be available at `localhost:9092` by default.

**Note:** Ensure your firewall and network settings allow connections to `localhost:9092`. You can modify the Docker Compose file if you need to expose Kafka on a different IP.

### 4. **Install Python Dependencies**

Install the required Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install the necessary Python packages, including Flask, Confluent Kafka, and other dependencies.

### 5. **Start the Flask App**

Once Kafka is running and the dependencies are installed, start the Flask application:

```bash
python app.py
```

By default, the Flask app will be accessible at `http://127.0.0.1:5000/`.

---

## API Endpoints

### 1. **POST /produce**

This endpoint allows you to produce a message to a Kafka topic.

- **URL**: `/produce`
- **Method**: `POST`
- **Request Body** (JSON):
    ```json
    {
      "topic": "test-topic",
      "message": "Hello Kafka!"
    }
    ```
- **Response** (JSON):
    ```json
    {
      "Topic": "test-topic",
      "Message": "Hello Kafka!",
      "Guid": "<UUID>"
    }
    ```
- **Description**: Produces a message with a unique UUID to the specified Kafka topic.

### 2. **GET /consume**

This endpoint allows you to consume messages from a specified Kafka topic and partition.

- **URL**: `/consume?topic=test-topic&partition=0`
- **Method**: `GET`
- **Query Parameters**:
  - `topic`: The Kafka topic to consume from (e.g., `test-topic`).
  - `partition`: The Kafka partition to consume from (e.g., `0`).
  
- **Response** (JSON):
    ```json
    [
      {
        "Id": "<UUID>",
        "Message": "Hello Kafka!",
        "Topic": "test-topic",
        "Partition": 0,
        "Offset": 1
      }
    ]
    ```
- **Description**: Consumes messages from the specified topic and partition and returns the message details in a structured format.

### 3. **POST /admin/topic**

This endpoint allows you to create a new Kafka topic with specified partition and replication factor.

- **URL**: `/admin/topic`
- **Method**: `POST`
- **Request Body** (JSON):
    ```json
    {
      "topic": "new-topic",
      "partitions": 3,
      "replication_factor": 1
    }
    ```
- **Response** (JSON):
    ```json
    {
      "message": "Topic 'new-topic' created successfully"
    }
    ```
- **Description**: Creates a new Kafka topic with the specified number of partitions and replication factor.

### 4. **DELETE /admin/topic**

This endpoint allows you to delete a Kafka topic.

- **URL**: `/admin/topic?topic=new-topic`
- **Method**: `DELETE`
- **Query Parameters**:
  - `topic`: The Kafka topic to delete (e.g., `new-topic`).

- **Response** (JSON):
    ```json
    {
      "message": "Topic 'new-topic' deleted successfully"
    }
    ```
- **Description**: Deletes the specified Kafka topic.

### 5. **POST /admin/partitions**

This endpoint allows you to add partitions to an existing Kafka topic.

- **URL**: `/admin/partitions`
- **Method**: `POST`
- **Request Body** (JSON):
    ```json
    {
      "topic": "test-topic",
      "partitions": 2
    }
    ```
- **Response** (JSON):
    ```json
    {
      "message": "Added 2 partitions to 'test-topic'"
    }
    ```
- **Description**: Adds the specified number of partitions to an existing Kafka topic.

---

## Testing the APIs

You can test the API endpoints using tools like **Postman**, **curl**, or a **Python script**.

### 1. **Test /produce (POST)**

```bash
curl -X POST http://127.0.0.1:5000/produce -H "Content-Type: application/json" -d '{"topic": "test-topic", "message": "Hello Kafka!"}'
```

### 2. **Test /consume (GET)**

```bash
curl "http://127.0.0.1:5000/consume?topic=test-topic&partition=0"
```

### 3. **Test /admin/topic (POST)**

```bash
curl -X POST http://127.0.0.1:5000/admin/topic -H "Content-Type: application/json" -d '{"topic": "new-topic", "partitions": 3, "replication_factor": 1}'
```

### 4. **Test /admin/topic (DELETE)**

```bash
curl -X DELETE "http://127.0.0.1:5000/admin/topic?topic=new-topic"
```

### 5. **Test /admin/partitions (POST)**

```bash
curl -X POST http://127.0.0.1:5000/admin/partitions -H "Content-Type: application/json" -d '{"topic": "test-topic", "partitions": 2}'
```

---

## Troubleshooting

### 1. **Kafka Broker Connection Issues**

- Make sure Kafka is running and accessible at the configured IP (`localhost:9092` by default).
- If Kafka is running on a different IP, update the configuration in `utils/kafka_config.py`.

### 2. **Topic Not Found**

- Ensure that the Kafka topic exists. You can create a topic using the `/admin/topic` API endpoint.

### 3. **Consumer Not Receiving Messages**

- Make sure the consumer is subscribing to the correct Kafka topic and partition. Use the `/consume` API to consume messages.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Explanation:

- **Set up**: This section walks the user through cloning the repository, modifying the IP address (if necessary), and using Docker Compose to start Kafka.
- **API Endpoints**: Details the various API endpoints (`/produce`, `/consume`, `/admin/topic`, `/admin/partitions`), what they do, and what requests and responses look like.
- **Testing**: Instructions for testing the APIs using tools like **Postman**, **curl**, and **Python script**.
- **Troubleshooting**: Common issues like Kafka connection problems and missing topics are addressed.

This README provides complete information for users to set up the project and use its features effectively.