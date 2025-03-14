from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client import LlamaStackClient
from ..tools import ArbitraryClientTool, GenerateParam


client = LlamaStackClient(base_url="http://localhost:8321")

# GENERATE PARAM TOOL
i=20

generate_param_tool = GenerateParam("param","str","This is a parameter")
agent_config_param = AgentConfig(
model="meta-llama/Llama-3.1-8B-Instruct",
enable_session_persistence = False,
instructions = """You are a Parameter generator assistant. Use the GenerateParam tool to generate realistic and random parameters for a function that will be created.
When using the generate_param_tool tool:
1. Choose a random topic and parameter type (str/bool/int/float).
3. For the randomly selected parameter type and topic create a realistic name to match the parameter type, and a description also.
4. Pass these the name, parameter type and description in to the generate_param_tool
""",
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

session_id = agent_param.create_session("test")
for count in range(i):
    response = agent_param.create_turn(
                messages=[{"role":"user","content":"use the generate_param_tool and pass in a name, type, and description"}],
                session_id= session_id,
                stream=False,
                )

    steps = response.steps

    param = steps[0].api_model_response.tool_calls[0].arguments['param']

    name = param.get('name', 'Not Available')
    type = param.get('type', 'Not Available')
    description = param.get('description', 'Not Available')
                

    print(f" name {name}, type:{type}, description:{description}")
    all_params["name"].append(name)
    all_params["type"].append(type)
    all_params["description"].append(description)

# ARBITRARY CLIENT TOOL
i=1
arbitrary_client_tool = ArbitraryClientTool(all_params)

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

for log in EventLogger().log(response):
        log.print()

print("END:")
print("\n")
