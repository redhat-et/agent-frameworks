# 🐝 Bee Agent Framework for prisol demo 

The **Bee Framework** provides two ways to develop agents:  

## 1. Low/No Code UI  
<img width="800" alt="UI Example" src="https://github.com/user-attachments/assets/a7c57c50-1df9-4c37-be3d-0d2cedfaabfe" />  

### Pros
- Easy to use, with side-by-side editing and testing.

### Cons
1. Limited functionality:
   - Cannot call other agents within the same project.
   - Supports custom tools and can call tools in a custom agent.
2. Error messages are not intuitive:
   - Custom tools must include docstrings in the correct position with proper spacing, or they will result in a `400` error.
3. Examples screenshots:  
   <img width="500" height="500" alt="scorer" src="https://github.com/user-attachments/assets/554a074e-4c50-46d3-895b-bbcedb77ea44" />
   <img width="500" height="500" alt="approver" src="https://github.com/user-attachments/assets/e0d5fe60-a17b-4fee-b960-6f03e679feb8" />  

## 2. Developer Version for Advanced Settings  
The developer version provides more advanced customization options for building agents.

This is a customized version of the [Bee Agent Framework](https://github.com/i-am-bee/bee-agent-framework), featuring an AI agent (`prisolv5.ts`) that evaluates risk and approval decisions. You can interact with the agent via:

✅ **Command Line Execution**  
✅ **REST API (FastAPI)**  
✅ **Web Interface (Streamlit UI)**  

📚 Learn more about Bee Agent Framework in the [official documentation](https://i-am-bee.github.io/bee-agent-framework/).

---

## 🚀 Features

- 🤖 **Custom AI Agent (`prisolv5.ts`)** – Processes risk scoring and approval via calling any LLMs and custom tools

---

## 📦 Requirements

- **[Node.js 18+](https://nodejs.org/)** (use [nvm](https://github.com/nvm-sh/nvm) for version management)
- **Python 3.x** (for FastAPI & Streamlit)
- **Docker** (optional, for containerized infrastructure)
- **LLM Provider** (local or external, e.g., **Ollama, OpenAI, Groq, WatsonX**)

---

## 🛠️ Getting started

1. Clone this repository
2. Install dependencies `npm ci`.
3. Configure your project by filling in missing values in the `.env` file (default LLM provider is locally hosted `Ollama`).
4. Run the agent 
    4.1 run it via terminal 
    `npm run start src/prisolv3.ts` play with it using terminal
    or
    `npm run start src/prisolv5.ts` which reads from input.json and return output.json
    or
    4.2 run it via a easy UI
    `python server.py` 
    `streamlit rn app.py`
    Open http://localhost:8501 in your browser.


