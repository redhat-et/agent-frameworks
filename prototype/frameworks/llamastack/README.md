# Llama Stack Setup Guide

This guide will walk you through setting up and running the Llama Stack with Ollama using Podman instead of Docker.

---

## **1. Prerequisites**
Ensure you have the following installed:
- **Podman** (instead of Docker)
- **Python 3.10+**
- **pip** (latest version)
- **Ollama** ([Install Ollama](https://ollama.com/download))
- **llama_stack_client >= 0.1.3**

Verify installation:
```bash
podman --version
python3 --version
pip --version
```

---

## **2. Start Ollama**
Before running Llama Stack, start the Ollama server with:
```bash
ollama run llama3.2:3b-instruct-fp16 --keepalive 60m
```
This ensures the model stays loaded in memory for 60 minutes.

---

## **3. Set Up Environment Variables**
Set up the required environment variables:
```bash
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
```

---

## **4. Run Llama Stack Server with Podman**
Pull the required image:
```bash
podman pull docker.io/llamastack/distribution-ollama
```
Before executing the next command, make sure to create a local directory to mount into the container’s file system.

```bash
mkdir -p ~/.llama
```

Now run the server using:
```bash
podman run --privileged -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env OLLAMA_URL=http://host.containers.internal:11434 \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT
```
If needed, create and use a network:
```bash
podman network create llama-net
podman run --privileged --network llama-net -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT
```

Verify the container is running:
```bash
podman ps
```

---

## **5. Set Up Python Environment**
Create a virtual environment using `venv`:
```bash
python3 -m venv llama-stack-env
source llama-stack-env/bin/activate  # macOS/Linux
# On Windows: llama-stack-env\Scripts\activate
```
Install Llama Stack Client:
```bash
pip install --upgrade pip
pip install llama-stack-client
```
Verify installation:
```bash
pip list | grep llama-stack-client
```

---

## **6. Configure the Client**
Set up the client to connect to the Llama Stack server:
```bash
llama-stack-client configure --endpoint http://localhost:$LLAMA_STACK_PORT
```
List available models:
```bash
llama-stack-client models list
```

---

## **7. Run a RAG Agent**
If you want to enhance AI-generated responses with relevant retrieved information, you can follow the example provided in `scripts/rag.py`. This script demonstrates how to use a Retrieval-Augmented Generation (RAG) Agent to fetch external data and integrate it into its responses for improved accuracy and context awareness.

Run the script:
```bash
python scripts/rag.py
```

---
## **8. Run a Llama-Stack Code Interpreter Agent**
If you want to execute code using an AI-powered agent, you can follow the example provided in `scripts/coding-agent.py`. This script demonstrates how to use the Llama-Stack Code Interpreter Agent to process code inputs and return results in a natural language format.

Run the script:
```bash
python scripts/code-agent.py
```
---
## **9. Run a build in web search Agent**

If you wish to test around the web search tool with external web search API, you can follow the example in `scripts/tool_websearch.py`. This example modified based on exsiting web search tool from https://colab.research.google.com/github/meta-llama/llama-stack/blob/main/docs/getting_started.ipynb. Allow run it through podman follow same instruction.

Run the script:

```bash
python scripts/tool_websearch.py
```
---
## **10. Run a Custom Tool Agent**

If you wish to add your own custom tool, you can follow the example in `scripts/custom-tool.py`. This example defines a simple calculator tool to perform arithmetic operations such as add, subtract, multiply and divide.

Run the script:

```bash
python scripts/custom-tool.py
```
## **Run a wolfram-alpha powered Agent**

If you wish to test the Wolfram Alpha tool, you can follow the example in `tool_wolframAlpha.py`. This example is necessary to demonstrate how to build an agent based on Wolfram Alpha, as previous documentation examples are outdated. Run it through Podman following the same instructions.

Run the script:

```bash
python tool_wolframAlpha.py
```
---
## **Debugging Common Issues**
**Check if Podman is Running:**
```bash
podman ps
```

**Ensure the Virtual Environment is Activated:**
```bash
source llama-stack-env/bin/activate
```

**Reinstall the Client if Necessary:**
```bash
pip uninstall llama-stack-client
pip install llama-stack-client
```

**Test Importing the Client in Python:**
```bash
python -c "from llama_stack_client import LlamaStackClient; print(LlamaStackClient)"
```

---
