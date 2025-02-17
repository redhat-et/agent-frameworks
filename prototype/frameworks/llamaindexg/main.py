import random
import os
from pydantic import BaseModel
from fastapi import FastAPI
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

# Load the model name from environment variables
MODEL_NAME = os.environ.get("MODEL_NAME", "mistral")  # Default to "mistral" if not set

# Initialize the LLM model dynamically based on environment variable
llm = Ollama(model=MODEL_NAME)

# Function to calculate insurance score
def calculate_insurance_score() -> int:
    score = random.randint(1, 100)  # Random score
    return score

# Function to approve insurance based on score
def approve(score: int) -> str:
    return 'Approved' if score > 50 else 'Rejected'

# FastAPI app setup
app = FastAPI()

class UserInput(BaseModel):
    text: str

# Helper function to create an agent
def create_agent(system_prompt: str, tool_function) -> AgentRunner:
    agent_worker = FunctionCallingAgentWorker.from_tools(
        [FunctionTool.from_defaults(tool_function)],
        llm=llm,
        verbose=False,
        allow_parallel_tool_calls=False,
        system_prompt=system_prompt
    )
    return AgentRunner(agent_worker)

# Endpoint to process user input and return score & approval
@app.post("/process_input/")
async def process_input(user_input: UserInput):
    state = {"input_text": user_input.text, "response": "", "approval_status": ""}

    # Step 1: Generate insurance score using the scorer agent
    scorer_system_prompt = """
    You are responsible for determining a score for the user that represents how good a user is as an insurance customer.
    You should always use the tools you have access to to generate the score.
    ensuring they follow these rules:

    1. Generate a random number between 1 and 100
    2. Return just the number
    """
    
    scorer_agent = create_agent(scorer_system_prompt, calculate_insurance_score)
    state["response"] = str(scorer_agent.chat(f"Generate the score for the user given: {state['input_text']}"))

    # Step 2: Review the score and determine approval using the approver agent
    approver_system_prompt = """
    You are responsible for identifying whether the score is optimal for the approval for an insurance.
    You should always use the tools you have access to to generate the response.
    ensuring they follow these rules:

    1. Tell the user whether the score is approved or rejected
    2. Also, share your thoughts on this in 2 sentences
    """

    approver_agent = create_agent(approver_system_prompt, approve)
    approval_status = approver_agent.chat(f"Review the score {state['response']} and approve/reject it.")
    state["approval_status"] = approval_status

    return state
