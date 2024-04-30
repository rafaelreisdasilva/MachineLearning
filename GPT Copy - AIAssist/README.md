# ML Model API

This project aims to deploy a state-of-the-art Gen AI model that competes with Chat GPT behind a RESTful API for commercialization. We've chosen Flask as our REST API framework and utilized PostgreSQL as our database for storing model responses.

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Set up your PostgreSQL database and configure the connection URL in the `docker-compose.yaml` file.
4. Ensure Docker and Docker Compose are installed on your machine.
5. Build and run the Docker containers using `docker-compose up`.
6. Access the API endpoints through `http://localhost:5000`.

## Usage

### Health Check Endpoint

- **Endpoint:** `/health_check`
- **Description:** Basic health check endpoint to verify if the API is up and running.
- **Parameters:** None
- **Response:** None
- **Status Code:** 204

### Model Call Endpoint

- **Endpoint:** `/call_model`
- **Description:** Endpoint to call the ML model with a given prompt.
- **Parameters:** `prompt`
- **Response:** `response`
- **Status Code:** 201
- **Authentication:** Basic authentication is required using a username and password.

### Asynchronous Model Call Endpoint

- **Endpoint:** `/async_call_model`
- **Description:** Endpoint to call the ML model asynchronously with a given prompt.
- **Parameters:** `prompt`
- **Response:** `job_id`
- **Status Code:** 200
- **Authentication:** Basic authentication is required using a username and password.

### Asynchronous Model Status Endpoint

- **Endpoint:** `/async_call_status`
- **Description:** Endpoint to check the status of an asynchronous job.
- **Parameters:** `job_id`
- **Response:** `job_status` and `response`
- **Status Code:** 200
- **Authentication:** Basic authentication is required using a username and password.

### Rate Limiting

- Each user is limited to 3 calls to the ML model (`ml_model.super_chat_gpt_like_model`) to prevent abuse.

## Technologies Used

- Flask: Lightweight Python web framework for building RESTful APIs.
- PostgreSQL: Relational database management system for storing model responses.
- Docker: Containerization platform for building, shipping, and running applications.
- Docker Compose: Tool for defining and running multi-container Docker applications.
- Celery (Optional): Distributed task queue for handling asynchronous tasks.
- Redis (Optional): In-memory data structure store used as a message broker for Celery.

## Testing
- **Using Postman Web**
Open Postman.
Import the provided Postman collection.
Select the desired request (e.g., /async_call_model) and fill in the required parameters.
Send the request and verify the response.
- **Using Postman Agent**
Install Postman Agent on your machine.
Start Postman Agent.
Import the provided Postman collection.
Run the desired request (e.g., /async_call_model) and provide the required parameters.
Verify the response.
- **Example Tests**
- **Async Call Model Request**
- **URL: http://localhost:5000/async_call_model**
- **Method: POST**
- **Headers: Content-Type: application/json**
- **Body: { "prompt": "Hello, world!" }**
- **Expected Response:**
- **Status Code: 200**
- **Body: { "job_id": "6fde421b-5079-4c22-ad78-e65a6fefaaaf" }**
  
Async Call Status Request
- **URL: http://localhost:5000/async_call_status?job_id=6fde421b-5079-4c22-ad78-e65a6fefaaaf**
- **Method: GET**
- **Headers: Content-Type: application/json**
- **Expected Response:**
- **Status Code: 200**
- **Body: { "job_status": "processing", "response": null }**
- By following these steps and example tests, you can validate the functionality of the ML Model API and ensure its correct operation. If you encounter any issues or have any questions, feel free to reach out for assistance. Happy testing!

## Future Improvements

1. **Enhanced Model:** Incorporate more sophisticated machine learning models such as GPT-2 for improved responses.
2. **Celery Integration:** Utilize Celery with Redis as the message broker for efficient handling of asynchronous tasks.
3. **API Documentation:** Generate comprehensive API documentation using tools like Swagger for better developer experience.
4. **Logging and Monitoring:** Implement logging and monitoring solutions to track API usage, performance, and errors.
5. **Security Enhancements:** Strengthen authentication mechanisms, implement rate limiting, and sanitize inputs to prevent security vulnerabilities.
6. **Deployment Pipeline:** Set up a CI/CD pipeline for automated testing, building, and deploying the application to production environments.

By following these steps, you can replicate our solution and adapt it to your specific requirements. If you have any questions or need further assistance, feel free to reach out to us.

Happy coding!
