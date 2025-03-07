from llama_stack_client.lib.agents.client_tool import ClientTool
from llama_stack_client.types.tool_def_param import Parameter


class ArbitraryClientTool(ClientTool):
    def __init__(self, n, name, type, description):
        self.n = n
        self.name = name
        self.type = type
        self.description = description
    
    def _arbitrary_tool(self, *kwargs):
        return kwargs

    def _generate_kwargs(self,num:int,name:str,parameter_type:str,description:str) -> dict:
       kwargs = {f"q_{n}": Parameter(
                name=f"{name}",
                parameter_type=f"{parameter_type}",
                description=f"{description}",
                required=True,
            ) for n in range(num)}
       
       return kwargs

    def get_name(self):
        return "arbitrary_client_tool"
    
    def get_description(self):
        return "This tool is used to evaluate the number of parameters an LLM can manage during tool calling."
    
    def get_params_definition(self):
        return self._generate_kwargs(self.n,self.name,self.type,self.description)
    
    def run_impl(self, **kwargs):
        return self._arbitrary_tool(kwargs)



# Tool params
# Should
class GenerateParam(ClientTool):
    def __init__(self, name, parameter_type, description):
        self.name = name
        self.parameter_type = parameter_type
        self.description = description
    
    def _arbitrary_tool(self, *kwargs):
        return kwargs

    def _generate_kwargs(self, name:str,parameter_type:str,description:str) -> dict:
       kwargs = {f"Param": Parameter(
                name=f"{name}",
                parameter_type=f"{parameter_type}",
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