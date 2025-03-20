from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client import LlamaStackClient
from ..tools import ArbitraryClientTool, GenerateParam
import json
import ast


client = LlamaStackClient(base_url="http://localhost:8321")

# GENERATE PARAM TOOL
def get_params(i):
    generate_param_tool = GenerateParam("param","str","This is a parameter")

    agent_param = Agent(client,
        model="meta-llama/Llama-3.1-8B-Instruct",
        enable_session_persistence = False,
        instructions = """You are a Parameter generator assistant. Use the GenerateParam tool to generate realistic and random parameters for a function that will be created.
        When using the generate_param_tool tool:
        1. Select a parameter type (str/bool/int/float) for it.
        3. For the randomly selected parameter type create a realistic name different to previous params to match the parameter type, and a description based on a random topic.
        4. Pass these the name, parameter type and description in to the generate_param_tool
        """,
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
        # for log in EventLogger().log(response):
        #     log.print()
        steps = response.steps
        # for step in steps:
        #     print(step)
        param = steps[1].tool_calls[0].arguments['param']
        if isinstance(param, str):
            try:
                # Attempt to convert the string to a dictionary (assuming it's a JSON string)
                param = ast.literal_eval(param)
            except (ValueError, SyntaxError):
                print("Error: The string is not a valid dictionary format.")
        
        
        name = param.get('name', 'Not Available')
        param_tpy = param.get('type', 'Not Available')
        description = param.get('description', 'Not Available')

        if name in all_params['name']:
            print("Parameter already exists")
            i = i - 1
        else:
            print(f"Parameter {count+1}: name {name}, type:{param_tpy}, description:{description}")
            all_params["name"].append(name)
            all_params["type"].append(param_tpy)
            all_params["description"].append(description)
        
    return all_params

def test_abitrary_client_tool(all_params):
    arbitrary_client_tool = ArbitraryClientTool(all_params)

    agent = Agent(client,
                model="meta-llama/Llama-3.1-8B-Instruct",
                enable_session_persistence = False,
                instructions = "You are a helpful assistant. Use the ArbitraryClientTool and pass in a value for each parameter according to its type.",
                tools=[arbitrary_client_tool]
                )

    session_id = agent.create_session("test")
    response = agent.create_turn(
                messages=[{"role":"user","content":"use the arbitrary_client_tool and pass in parameters according to their type"}],
                session_id= session_id,
                stream=False,
                )

    # for log in EventLogger().log(response):
    #         log.print()
    return response

def main():
    all_params = get_params(1)
    response = test_abitrary_client_tool(all_params)
    for step in response.steps:
        print(step)
if __name__ == "__main__":
    main()
