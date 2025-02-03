import "dotenv/config";
import { UnconstrainedMemory } from "bee-agent-framework/memory/unconstrainedMemory";
import { AgentWorkflow } from "bee-agent-framework/experimental/workflows/agent";
import { BaseMessage, Role } from "bee-agent-framework/llms/primitives/message";
import { GroqChatLLM } from "bee-agent-framework/adapters/groq/chat";
import { createConsoleReader } from "./helpers/io.js";
import { CustomTool } from "bee-agent-framework/tools/custom";
const workflow = new AgentWorkflow();

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

// const ScorerTool = await CustomTool.fromSourceCode(
//   {
//     // Ensure the env exists
//     url: process.env.CODE_INTERPRETER_URL!,
//     env: {},
//   },
//   `import random

// def generate_score(text: str) -> str:
//     """
//     Generate a random score for the given text.
//     :param text: The input text to be scored.
//     :return: A randomly generated score as a string.
//     """
//     return str(random.randint(1, 100))`
// );

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

// console.log("ApproverTool Loaded:", ApproverTool);
// console.log("ScorerTool Loaded:", ScorerTool);


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

const reader = createConsoleReader();
const memory = new UnconstrainedMemory();


for await (const { prompt } of reader) {
  await memory.add(
    BaseMessage.of({
      role: Role.USER,
      text: prompt,
      meta: { createdAt: new Date() },
    }),
  );

  const { result } = await workflow.run(memory.messages).observe((emitter) => {
    emitter.on("success", (data) => {
      reader.write(`-> ${data.step}`, data.response?.update?.finalAnswer ?? "-");
    });
  });
  await memory.addMany(result.newMessages);
  reader.write(`Agent 🤖`, result.finalAnswer);
}
