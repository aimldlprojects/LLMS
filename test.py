from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO)

# Pydantic model for the incoming JSON payload
class Payload(BaseModel):
    data: str

# API endpoint to receive JSON payload and write to log file
@app.post("/receive-payload")
def receive_payload(payload: Payload):
    try:
        # Log the received data
        logging.info(f"Received payload: {payload.data}")

        # Additional processing logic can be added here

        return {"message": "Payload received successfully"}
    except Exception as e:
        logging.error(f"Error processing payload: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
