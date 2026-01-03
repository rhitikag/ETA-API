# ETA-API

Simple FastAPI application providing an endpoint to predict ETA from an input JSON file.

## Prerequisites

- Python 3.8 or newer
- git

## Installation

1. Clone the repository:

   git clone https://github.com/rhitikag/ETA-API.git
   cd ETA-API

2. (Optional) Create and activate a virtual environment:

   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

## Running the application

Start the server with uvicorn:

uvicorn app:app --host 0.0.0.0 --port 8000

The server will be available at http://127.0.0.1:8000.

## Using the API

Open the interactive API docs in your browser:

http://127.0.0.1:8000/docs

There is a `predict-file` endpoint in the Swagger UI where you can upload an `input.json` file and receive predictions.

Notes:

- Ensure the uploaded `input.json` matches the expected model input schema used by the application.
- If port 8000 is already in use, change the `--port` value when starting uvicorn.

## Example (optional)

If you have an example `input.json`, upload it via the `predict-file` section in the docs UI to test the prediction endpoint.

---

If you'd like, I can also add a sample `input.json` structure to this README or expand usage examples for curl/Postman.
