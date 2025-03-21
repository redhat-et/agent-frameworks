from typing import Dict, List, Optional, Any

def create_agent_prompt(model: str, instructions: str, tool_groups: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Create a prompt for setting up an agent with specified parameters.
    
    Args:
        model: Model to use for the agent (e.g., 'meta-llama/<>')
        instructions: Instructions for the agent to follow
        tool_groups: Comma-separated list of tool groups to enable for the agent
        
    Returns:
        List of messages for the prompt
    """
    tool_group_list = []
    if tool_groups:
        tool_group_list = [group.strip() for group in tool_groups.split(",") if group.strip()]
    
    messages = []
    
    # Add system message with instructions
    messages.append({
        "role": "system",
        "content": instructions
    })
    
    # Add user message describing the agent setup
    agent_description = f"I want to set up an agent using the {model} model"
    if tool_group_list:
        agent_description += f" with the following tool groups: {', '.join(tool_group_list)}"
    agent_description += ".\n\nPlease confirm the setup and let me know how I can interact with this agent."
    
    messages.append({
        "role": "user",
        "content": agent_description
    })
    
    return messages