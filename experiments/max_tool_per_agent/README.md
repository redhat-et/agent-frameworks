# Evaluating Tool Selection and Scalability in LlamaStack
## Objective
Assess LlamaStack’s ability to handle an increasing number of tools, evaluate tool selection accuracy, and determine whether providing a subset of relevant tools as input improves performance. Also how model series, model size affect performance.
## Key Research Questions
* Scalability: What is the maximum number of tools an agent can handle before performance degrades?
* Tool Selection Accuracy: How well does the agent pick the correct tool for a given query?
* Guided Tool Selection: Does providing a relevant subset of tools in the prompt improve accuracy?
* Model factor: How does model architecture (series, size, temperature type of hyperparameter) affect LlamaStack's tool execution and selection performance?
## Methodology
* Tools:  
  - 3 built-in tools (websearch, wolfram_alpha, code_interpreter). (less priority)
  - Dynamically generated N client tools to test scalability (N = 5, 10, 20, 50).
  - also mcp tools (less priority)
* Queries:  
A diverse set of tasks designed to require specific tools.
* **Metrics**:  
  - Scalability Limit (max tool count before performance drops).  
  - Tool Selection Accuracy (% correct, incorrect, or missing tool calls by assert response.steps).  
  - Context size vs tool count. (token size is a strict limitation.)
  - Latency (response time vs. tool count).
  
* Logging:  
Structured logs in CSV format capturing the query, available tools, selected tool, expected tool, execution success, and latency.

Currently, we have multiple built-in tool scripts available. A more systematic evaluation is still a work in progress.

## TODOs
- [ ] Identify and summarize suitable benchmark datasets.
- [ ] Calculate accuracy using appropriate benchmarks.
- [ ] Continue refining metrics and identifying influencing factors.
- [ ] Develop a suitable system prompt wrapper for user queries to ensure the correct tool is executed.

## Simple test of max client tool experiment
This `faketooltest.py` script tests how well LlamaStack handles increasing numbers of tools by measuring **tool selection accuracy, execution success, and latency**. 
#### Experiment Setup
- **5 Real Tools**: Weather info, word count, string reversal, uppercase conversion, insurance scoring.
- **Fake Tools**: Dynamically generated tools with random outputs (up to 40 additional tools).
- **5 Fixed Queries**: Each mapped to a ground truth tool.
- **Scaling**: Start with 5 tools, increase by 5 up to 45.
- **Metrics Logged**:
  - Exception Rate (how many exception occurs out of 5 queries)
  - Tool Execution Success Rate (how many time tools are actually executed out of 5 queries)
  - Correct Tool Selection Rate  (how many time correct tool is selected out of 5 queries)
  - Average Latency (average time taken to respond 5 queries)

#### Run the Experiment
```bash
python faketooltest.py
```
Results are saved in `experiment_results.csv` for analysis.

#### Conclusion
current test conclude, llama 3B model can deal with max 25 tools. Latency per query 0.178s (serverd locally)

#### Limitations
- **Fake tools are highly similar**, making them easy to distinguish from real tools, also no parameter.
- **Only 5 queries**, limiting diversity in tool usage.
- **Model may perform better here** than in real-world scenarios with more diverse tools.

#### Next Steps
- Move to a **proper benchmark** with a broader toolset.
- Incorporate **realistic tool diversity** to stress test selection accuracy.
- Compare results across **different model sizes** to assess generalization.

## Test multi-builtin-tool
This is a initial test about having multiple buildin tools configed for one agent. 
The current version works with 0.1.6. If running with previous versions, ensure that `run.yaml` has all three tools configured. 
step 1. `ollama run llama3.2:3b-instruct-fp16 --keepalive 60m`  
step 2.
```
export INFERENCE_MODEL="meta-llama/Llama-3.2-3B-Instruct"
export LLAMA_STACK_PORT=8321
```  
step 3: `llama stack run --image-type conda ~/llama-stack/llama_stack/templates/ollama/run.yaml` (I'm using conda env, follow this(https://llama-stack.readthedocs.io/en/latest/distributions/building_distro.html) if not using conda)  
step 4: run `python multi-builtintools.py`