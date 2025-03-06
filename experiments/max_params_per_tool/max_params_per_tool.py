from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client import LlamaStackClient
import json
from ..tools import ArbitraryClientTool, GenerateParam



client = LlamaStackClient(base_url="http://localhost:8321")


    
generate_param_tool = GenerateParam("param","str","This is a parameter")
# print(generate_param_tool.get_tool_definition())
agent_config_param = AgentConfig(
model="meta-llama/Llama-3.1-8B-Instruct",
enable_session_persistence = False,
instructions = """You are a Parameter generator assistant. Use the GenerateParam tool to generate random realistic parameters for a function that will be created.
When using the GenerateParam tool:
1. Create a name, parameter type, and description for the parameters
2. Return the name, parameter type, and description for the parameters
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
            messages=[{"role":"user","content":"use the GenerateParam and pass in a random parameters"}],
            session_id= session_id,
            )

print("OUTPUT:")
# for r in response:
    # print("Inference Output:")
    # print(r)
print("\n \n")

# arbitrary_client_tool = ArbitraryClientTool(i)
# print(arbitrary_client_tool.get_tool_definition())
# agent_config = AgentConfig(
#     model="meta-llama/Llama-3.1-8B-Instruct",
#     enable_session_persistence = False,
#     instructions = "You are a helpful assistant.",
#     toolgroups = [],
#     client_tools = [arbitrary_client_tool.get_tool_definition()],
#     tool_choice="auto",
#     tool_prompt_format="json",
#     max_infer_iters=4,
#     )

# agent = Agent(client=client,
#             agent_config=agent_config,
#             client_tools=[arbitrary_client_tool]
#             )

    # session_id = agent.create_session("test")
    # response = agent.create_turn(
    #             messages=[{"role":"user","content":"use the arbitrary_client_tool and pass in parameters"}],
    #             session_id= session_id,
    #             )
print("OUTPUT:")
ev = ""
for r in EventLogger().log(response):
    ev += str(r) 
print(ev)

data = json.loads(ev)
print(data)
# print(abbbs)
# print(response.ToolCall())
print("END:") 
print("\n")
