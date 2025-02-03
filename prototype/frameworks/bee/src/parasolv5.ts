import "dotenv/config";
import { UnconstrainedMemory } from "bee-agent-framework/memory/unconstrainedMemory";
import { AgentWorkflow } from "bee-agent-framework/experimental/workflows/agent";
import { BaseMessage, Role } from "bee-agent-framework/llms/primitives/message";
import { GroqChatLLM } from "bee-agent-framework/adapters/groq/chat";
import { CustomTool } from "bee-agent-framework/tools/custom";
import fs from "fs";


const workflow = new AgentWorkflow();

// Define the LLMs, calling the GroqChatLLM constructor with the modelId
const chatLLM1 = new GroqChatLLM({ 
  modelId: "gemma2-9b-it"  
  // modelId: "mixtral-8x7b-32768"
  // modelId: "deepseek-r1-distill-llama-70b"
});

const chatLLM2 = new GroqChatLLM({
  // modelId: "llama-3.1-8b-instant" 
  // modelId: "gemma2-9b-it"
  modelId: "deepseek-r1-distill-llama-70b" 
});

// Define the custom tools, calling the CustomTool.fromSourceCode method with python source code
const ApproverTool = await CustomTool.fromSourceCode(
  {
    // Ensure the env exists
    url: process.env.CODE_INTERPRETER_URL!,
    env: {},
  },
  `
def approve_text(score: int) -> str:
    """
    Determines approval based on score.
    :param score: The input score to be evaluated.
    :return: "Approved" if score > 50, otherwise "Denied".
    """
    return "Approved" if score > 50 else "Denied"`
);

const ScorerTool = await CustomTool.fromSourceCode(
  {
    url: process.env.CODE_INTERPRETER_URL!,
    env: {},
  },
  `
import random
import json

def generate_score(text: str) -> str:
    """
    Generate a random score for the given text.
    :param text: The input text to be scored.
    :return: A JSON object with the score.
    """
    score = random.randint(1, 100)
    return json.dumps({"tool_name": "ScorerTool", "score": score})
`
);


// Add the agents to the workflow, can assign different LLMs to each agent.
workflow.addAgent({
  name: "Scorer",
  instructions: "You are a scorer assistant. based on user input, give a risk score an integer range from 1-100. higher score means low risk. (tell me about the tool used)",
  tools: [ScorerTool],
  llm: chatLLM2, 
});

workflow.addAgent({
  name: "Approver",
  // instructions: "You are a approver assistant. given the risk score, if > 50 approve, else deny. tell user if user got approved or not. Output acceptance or denial letter with an explanation as to why to the user.",
  instructions: "You are a approver assistant. given the risk score, run approvertool on that risk score. tell user if user got approved or not and why (tell me about the tool used). ",
  tools: [ApproverTool],
  llm: chatLLM2,
});


const inputFile = "input.json";
let userInput = "";

// Read input from input.json file
if (fs.existsSync(inputFile)) {
  const data = fs.readFileSync(inputFile, "utf-8");
  userInput = JSON.parse(data).text;
} else {
  console.error("No input file found.");
  process.exit(1);
}

const memory = new UnconstrainedMemory();
// Add the user input to the memory
await memory.add(
  BaseMessage.of({
    role: Role.USER,
    text: userInput,
    meta: { createdAt: new Date() },
  }),
);

const { result } = await workflow.run(memory.messages);

await memory.addMany(result.newMessages);

// Extract the steps and final answer from the result
const steps = result.newMessages.map(msg => `${msg.text}`);

// Write the output to output.json file
if (!result.finalAnswer) {
  fs.writeFileSync("output.json", JSON.stringify({ error: "No valid response from AI" }, null, 2));
} else {
  fs.writeFileSync("output.json", JSON.stringify({
    thinking_process: steps,
    result: result.finalAnswer
  }, null, 2));
}


