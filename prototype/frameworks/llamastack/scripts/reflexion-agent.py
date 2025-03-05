# Mimicing react_agent from https://github.com/meta-llama/llama-stack-apps/pull/166
# Reflexion is an advanced prompting technique that can greatly improve the accuracy 
# across various coding and reasoning benchmarks.
#
# This implementation demonstrates a ReflexionAgent that can:
# 1. Solve problems step-by-step with explicit reasoning
# 2. Self-evaluate solutions and identify mistakes
# 3. Learn from previous attempts through reflection
# 4. Leverage tools (calculator, fact-checker) to improve accuracy
#
# The agent is based on the paper "Reflexion: Language Agents with Verbal Reinforcement Learning"
# (https://arxiv.org/abs/2303.11366) and uses Llama 3.1 8B as the underlying model.

import uuid

import fire

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.client_tool import client_tool
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.lib.agents.reflexion.agent import ReflexionAgent


@client_tool
def calculator(expression: str):
    """
    Calculate the result of a mathematical expression.
    
    :param expression: A mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)", "cos(0)")
    :returns: The calculated result
    """
    try:
        # Use safer eval with limited namespace
        import math
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith('__')}
        allowed_names.update({"abs": abs, "round": round})
        
        # Calculate and return result
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error calculating result: {str(e)}"


@client_tool
def fact_check(statement: str):
    """
    Verify if a statement is factually correct.
    
    :param statement: The statement to fact check
    :returns: Information about the statement's accuracy
    """
    # This is a mock implementation for demonstration
    if "earth is flat" in statement.lower():
        return "This statement is false. The Earth is an oblate spheroid."
    elif "moon landing" in statement.lower() and "fake" in statement.lower():
        return "This statement is false. The moon landings were real historical events."
    elif "water boils at 100" in statement.lower():
        return "This statement is true, but only at sea level under standard atmospheric pressure."
    else:
        return "I don't have specific fact-checking information about this statement in my knowledge base."


def main():
    client = LlamaStackClient(
        base_url="http://localhost:8321",
    )

    model = "meta-llama/Llama-3.1-8B-Instruct"
    agent = ReflexionAgent(
        client=client,
        model=model,
        builtin_toolgroups=["builtin::websearch"],
        client_tools=[calculator, fact_check],
    )

    session_id = agent.create_session(f"reflexion-session-{uuid.uuid4().hex}")

    # First turn - solving a math problem
    print("\n=== TURN 1: Math Problem ===\n")
    response1 = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": "What is the square root of 144 plus 25?",
            }
        ],
        session_id=session_id,
        stream=True,
    )
    for log in EventLogger().log(response1):
        log.print()

    # Second turn - builds on first, requiring reflection
    print("\n=== TURN 2: Follow-up Question ===\n")
    response2 = agent.create_turn(
        messages=[
            {
                "role": "user", 
                "content": "Is the result a prime number? Use your calculator tool to verify.",
            }
        ],
        session_id=session_id,
        stream=True,
    )
    for log in EventLogger().log(response2):
        log.print()

    # Third turn - testing fact checking and reflection
    print("\n=== TURN 3: Fact Checking ===\n")
    response3 = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": "Someone told me the Earth is flat. Can you fact check this claim?",
            }
        ],
        session_id=session_id,
        stream=True,
    )
    for log in EventLogger().log(response3):
        log.print()

    # Fourth turn - a more complex problem requiring both reflection and tools
    print("\n=== TURN 4: Complex Problem ===\n")
    response4 = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": "If I have 3 containers with volumes of 10, 15, and 25 liters, and I fill them to 80% capacity, what's the total volume of liquid I'll need? Then convert your answer to gallons.",
            }
        ],
        session_id=session_id,
        stream=True,
    )
    for log in EventLogger().log(response4):
        log.print()


if __name__ == "__main__":
    fire.Fire(main)