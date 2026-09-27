from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent import Agent
from models import ChatRequest, PermissionRequest
from memory import init_db


app = FastAPI(
    title="Bharat Personal Agent",
    description="Privacy-first personal AI agent prototype"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Initialize SQLite database
init_db()

# Create agent
agent = Agent()


@app.get("/")
def home():

    return {
        "name": "Bharat Personal Agent",
        "status": "running",
        "mode": "demo"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    return agent.process(
        request.message,
        request.user_id
    )


@app.post("/permission")
def permission(request: PermissionRequest):

    message = agent.handle_permission(
        request.permission_id,
        request.allowed
    )

    return {
        "message": message
    }


@app.post("/continue")
def continue_request(request: ChatRequest):

    return agent.continue_request(
        request.user_id
    )