<h2> Travel Recommendations </h2>

This project is a FastAPI application that provides travel recommendations for a given country and season.

<i>
    <a href="#">
        <img src="https://img.shields.io/badge/python-brightgreen">
    </a>
</i>

<i>
    <a href="#">
        <img src="https://img.shields.io/badge/FastAPI-brightgreen">
    </a>
</i>

<i>
    <a href="#">
        <img src="https://img.shields.io/badge/MongoDB-brightgreen">
    </a>
</i>

<i>
    <a href="#">
        <img src="https://img.shields.io/badge/OpenAI-brightgreen">
    </a>
</i>

<hr/>

## Features

- FastAPI backend with endpoints to request and fetch travel recommendations.
- Asynchronous background processing with Kafka.
- MongoDB for storing task data and recommendations.
- Simple frontend to interact with the API.
- Docker Compose for containerizing the application components.

## Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher (for running tests locally)
- OpenAI API key

## Environment Variables

Clone `.env` file from `.env.template` in the root directory with the following variables:

```
MONGODB_URI=mongodb://devUser:devPassword@mongo:27017/travel_recommendations?authSource=travel_recommendations
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=travel_recommendations
OPENAI_API_KEY=<your_openai_api_key>
```

## Running the Application

1. **Clone the repository:**

```bash
git clone https://github.com/kha-phan/development-task.git
cd development-task
```

2. **Build and run the Docker containers:**

```bash
docker-compose up --build
```
Remove after running
```bash
docker-compose down --remove-orphans
```

3. **Access the application:**

Open your web browser and navigate to `http://localhost:3000`.


### Frontend

The frontend is a simple HTML page that allows users to input the country and season, request travel recommendations, and view the results.

#### Features

- Input fields for country and season.
- Button to request recommendations.
- Display area for the status and recommendations.

## API Endpoints

### 1. Request Recommendations

- **URL:** `/recommendations/`
- **Method:** `GET`
- **Query Parameters:**
  - `country`: The country for which the recommendations are to be fetched.
  - `season`: The season in which the recommendations are desired (e.g., "spring", "summer", "fall", "winter").
- **Response:**
  ```json
  {
    "uid": "1234567890abcdef"
  }
  ```

### 2. Check Status and Fetch Recommendations

- **URL:** `/status/{uid}`
- **Method:** `GET`
- **Path Parameters:**
  - `uid`: The unique identifier for the request.
- **Responses:**
  - If the task is still pending:
    ```json
    {
      "uid": "1234567890abcdef",
      "status": "pending",
      "message": "The recommendations are not yet available. Please try again later."
    }
    ```
  - If the task is completed:
    ```json
    {
      "uid": "1234567890abcdef",
      "country": "Canada",
      "season": "winter",
      "status": "completed",
      "recommendations": [
        "Go skiing in Whistler.",
        "Experience the Northern Lights in Yukon.",
        "Visit the Quebec Winter Carnival."
      ]
    }
    ```
  - If the UID is not found:
    ```json
    {
      "detail": "UID not found"
    }
    ```
    
## Testing the Application

1. **Install the testing dependencies:**

```bash
pip install -r requirements.txt
pip install -r requirements_test.txt
```

2. **Run the tests:**

```bash
pytest
```

#### About evidences, please refer to [Evidences](README.envidence.md)