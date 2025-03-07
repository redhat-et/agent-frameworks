from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client import LlamaStackClient
from ..tools import ArbitraryClientTool, GenerateParam



client = LlamaStackClient(base_url="http://localhost:8321")

# GENERATE PARAM TOOL
    
generate_param_tool = GenerateParam("param","str","This is a parameter")
# print(generate_param_tool.get_tool_definition())
agent_config_param = AgentConfig(
model="meta-llama/Llama-3.1-8B-Instruct",
enable_session_persistence = False,
instructions = """You are a Parameter generator assistant. Use the GenerateParam tool to generate realistic and random parameters for a function that will be created.
When using the generate_param_tool tool:
1. Create a name, parameter type, and description for the parameter
2. Pass these into the generate_param_tool
3. Present the result clearly""",
toolgroups = [],
client_tools = [generate_param_tool.get_tool_definition()],
tool_choice="auto",
tool_prompt_format="json",
max_infer_iters=4,
)
agent_param = Agent(client=client,
            agent_config=agent_config_param,
            client_tools=[generate_param_tool],
            )

session_id = agent_param.create_session("test")
response = agent_param.create_turn(
            messages=[{"role":"user","content":"use the generate_param_tool and pass in a realistic and random parameter"}],
            session_id= session_id,
            stream=False,
            )

steps = response.steps
#######################################
#############
# Set Steam = False to use the steps
# for step in steps:
#     print(step)
#     print("\n")

# Set Stream = True to use the EventLogger
# for log in EventLogger().log(response):
#         log.print()
assert len(steps) == 3
assert steps[0].step_type == "inference"
assert steps[1].step_type == "tool_execution"
assert steps[2].step_type == "inference"
param = steps[1].tool_calls[0].arguments['param']

name = param.get('name', 'Not Available')
parameter_type = param.get('parameter_type', 'Not Available')
description = param.get('description', 'Not Available')
            

print(f" name {name}, parameter_type:{parameter_type}, description:{description}")


# ARBITRARY CLIENT TOOL
i=1
arbitrary_client_tool = ArbitraryClientTool(i, name, parameter_type, description)
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
            session_id= session_id,
            )

for log in EventLogger().log(response):
        log.print()

print("END:")
print("\n")
