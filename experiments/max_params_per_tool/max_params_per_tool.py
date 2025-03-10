from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client import LlamaStackClient
from ..tools import ArbitraryClientTool, GenerateParam


client = LlamaStackClient(base_url="http://localhost:8321")

# GENERATE PARAM TOOL
i=2

generate_param_tool = GenerateParam("param","str","This is a parameter")
# print(generate_param_tool.get_tool_definition())
agent_config_param = AgentConfig(
model="meta-llama/Llama-3.1-8B-Instruct",
enable_session_persistence = False,
instructions = """You are a Parameter generator assistant. Use the GenerateParam tool to generate realistic and random parameters for a function that will be created.
When using the generate_param_tool tool:
1. Create one realistic name, select a parameter type to match it, and a description.
2. Pass these into the generate_param_tool
3. Present the result clearly""",
toolgroups = [],
client_tools = [generate_param_tool.get_tool_definition()],
tool_choice="auto",
tool_prompt_format="json",
max_infer_iters=4,
)
agent_param = Agent(client,agent_config_param,
            tools=[generate_param_tool],
            )
all_params = {"name": [], "type": [], "description": []}
# for count in i:
session_id = agent_param.create_session("test")
response = agent_param.create_turn(
            messages=[{"role":"user","content":"use the generate_param_tool and pass in a name, type, and description"}],
            session_id= session_id,
            stream=False,
            )

steps = response.steps
#######################################
#############
# Set Steam = False to use the steps
for step in steps:
    print(step)
    print("\n")
# # Set Stream = True to use the EventLogger
# for log in EventLogger().log(response):
#         log.print()
# assert len(steps) == 3

param = steps[0].api_model_response.tool_calls[0].arguments['param']

name = param.get('name', 'Not Available')
type = param.get('type', 'Not Available')
description = param.get('description', 'Not Available')
            

print(f" name {name}, type:{type}, description:{description}")
all_params["name"].append(name)
all_params["type"].append(type)
all_params["description"].append(description)

# ARBITRARY CLIENT TOOL
# all_params = {"name": ["speed"], "type": ["int"], "description": ["Car speed in km/hr"]}

i=1
arbitrary_client_tool = ArbitraryClientTool(all_params)
print(arbitrary_client_tool.get_tool_definition())
agent_config = AgentConfig(
    model="meta-llama/Llama-3.1-8B-Instruct",
    enable_session_persistence = False,
    instructions = "You are a helpful assistant.",
    toolgroups = [],
    client_tools = [arbitrary_client_tool.get_tool_definition()],
    tool_choice="auto",
    tool_prompt_format="json",
    max_infer_iters=4,
    )

agent = Agent(client=client,
            agent_config=agent_config,
            client_tools=[arbitrary_client_tool]
            )

session_id = agent.create_session("test")
response = agent.create_turn(
            messages=[{"role":"user","content":"use the arbitrary_client_tool and pass in parameters"}],
            session_id= session_id
            )
# steps = response.steps
# for step in steps:
#     print(step)
#     print("\n")

for log in EventLogger().log(response):
        log.print()

print("END:")
print("\n")
