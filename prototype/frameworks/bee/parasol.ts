import "dotenv/config";
import { UnconstrainedMemory } from "bee-agent-framework/memory/unconstrainedMemory";
import { AgentWorkflow } from "bee-agent-framework/experimental/workflows/agent";
import { BaseMessage, Role } from "bee-agent-framework/llms/primitives/message";
import { GroqChatLLM } from "bee-agent-framework/adapters/groq/chat";
import { CustomTool } from "bee-agent-framework/tools/custom";
import express from "express";
import type { Request, Response } from "express";

const app = express();
app.use(express.json()); // Parse JSON request bodies

const memory = new UnconstrainedMemory(); // Store conversation history

const workflow = new AgentWorkflow();

// Define the LLMs, calling the GroqChatLLM constructor with the modelId
const chatLLM1 = new GroqChatLLM({ 
  // modelId: "gemma2-9b-it"  
  // modelId: "mixtral-8x7b-32768"
  modelId: "deepseek-r1-distill-llama-70b"
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


app.get("/", (req, res) => {
  res.send("✅ Express Server is Running!");
});

// 📌 **RESTful API Endpoint (Replaces Console Input)**
app.post("/evaluate", async (req: Request, res: Response): Promise<void> => {
  try {
    const { text } = req.body;
    if (!text) {
      res.status(400).json({ error: "Missing 'text' in request body" });
      return;
    }

    // Store user input in memory
    await memory.add(
      BaseMessage.of({
        role: Role.USER,
        text,
        meta: { createdAt: new Date() },
      }),
    );

    // **Streaming Responses**
    let responseData = { thinking_process: [] as string[], result: "" };

    const { result } = await workflow.run(memory.messages).observe((emitter) => {
      emitter.on("success", (data) => {
        responseData.thinking_process.push(`-> ${data.step}: ${data.response?.update?.finalAnswer ?? "-"}`);
      });
    });

    await memory.addMany(result.newMessages);

    responseData.result = result.finalAnswer || "No valid response from AI";

    res.json(responseData);
  } catch (error) {
    console.error("Error processing request:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server is running on http://localhost:${PORT}`);
});
