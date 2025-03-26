from llama_stack_client.lib.agents.client_tool import ClientTool
from llama_stack_client.types.tool_def_param import Parameter


class ArbitraryClientTool(ClientTool):
    """AbitraryClientTool is a tool that returns the parameters passed to it.
    The agent checks the parameter type of each parameter and the passes a value based on that parameter type.
    :param all_params: A dictionary containing the parameters to be returned.
    :return: The parameters passed to the tool.
    """
    def __init__(self, all_params):
        self.all_params = all_params
    
    def _arbitrary_tool(self, *kwargs):
        return kwargs

    def _generate_kwargs(self, all_params) -> dict:
        kwargs = {f"param_{i}": Parameter(
            name=all_params["name"][i],
            parameter_type=all_params["type"][i],
            description=all_params["description"][i],
            required=True,
        ) for i in range(len(all_params["name"]))}
        return kwargs

    def get_name(self):
        return "arbitrary_client_tool"
    
    def get_description(self):
        return "This tool is used to evaluate the number of parameters an LLM can manage during tool calling."
    
    def get_params_definition(self):
        return self._generate_kwargs(self.all_params)
    
    def run_impl(self, **kwargs):
        return self._arbitrary_tool(kwargs)


class GenerateParam(ClientTool):
    """GenerateParam is a tool that generates a random realistic parameter.
    
    :param name: The name of the parameter.
    :param parameter_type: The type of the parameter.
    :param description: The description of the parameter.
    :returns: A random realistic parameter.
    """
    
    def __init__(self, name, parameter_type, description):
        self.name = name
        self.parameter_type = parameter_type
        self.description = description
    
    def _arbitrary_tool(self, *kwargs):
        return kwargs

    def _generate_kwargs(self, name:str,parameter_type:str,description:str) -> dict:
       kwargs = {f"Param": Parameter(
                name=f"{name}",
                parameter_type= f"{parameter_type}",
                description=f"{description}",
                required=True,
            )}
       
       return kwargs

    def get_name(self):
        return "generate_param_tool"
    
    def get_description(self):
        return "This tool generates a random realistic parameter, with a name, type, and description."
    
    def get_params_definition(self):
        return self._generate_kwargs(self.name,self.parameter_type,self.description)
    
    def run_impl(self, **kwargs):
        return self._arbitrary_tool(kwargs)