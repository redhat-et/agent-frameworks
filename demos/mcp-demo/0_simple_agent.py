# Code bellow written following examples here: https://llama-stack.readthedocs.io/en/latest/building_applications
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client import LlamaStackClient
from termcolor import cprint
import argparse
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--remote", help="Uses the remote_url",action="store_true")
args = parser.parse_args()

# Connect to the llama stack server
model="meta-llama/Llama-3.2-3B-Instruct"
if args.remote:
    base_url = os.getenv("REMOTE_BASE_URL")
else:
    base_url="http://localhost:8321"
logger.info(f"Connected to Llama Stack server @ {base_url}")


client = LlamaStackClient(base_url=base_url)
# Create the agent
agent = Agent(
    client,
    model=model,
    instructions="You are a helpful assistant that can use tools to answer questions.",
)

# Create a session
session_id = agent.create_session(session_name="Demo_conversation")

while True:
    user_input = input(">>> ") 
    if "/bye" in user_input:
        break
    turn_response = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": user_input}],
    )
    for log in EventLogger().log(turn_response):
        log.print()
