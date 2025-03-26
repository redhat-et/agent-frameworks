# Evaluating Tool Selection and Scalability in LlamaStack
## Objective
Assess LlamaStack’s ability to handle an increasing number of tools, evaluate tool selection accuracy, and determine whether providing a subset of relevant tools as input improves performance. Also how model series, model size affect performance.
## Key Research Questions
* Scalability: What is the maximum number of tools an agent can handle before performance degrades?
* Tool Selection Accuracy: How well does the agent pick the correct tool for a given query?
* Model factor: How does model architecture (series, size, context length, temperature type of hyperparameter) affect LlamaStack's tool execution and selection performance?
  * Guided Tool Selection: Does providing a relevant subset of tools in the prompt improve accuracy?

## Definition Of Done:
Must: Visualise results about max tool number over a range of models.
optional: A blog at https://next.redhat.com/blog/

## Methodology
* Scope:  
  - focus on client tools.

`maxtool.ipynb` script tests how well LlamaStack handles increasing numbers of tools by measuring **tool selection accuracy, execution success, and latency**. 
### Experiment Setup
- **5 Real Tools**: Weather info, word count, string reversal, uppercase conversion, insurance scoring.
- **Fake Tools**: Dynamically generated tools with random outputs.
- **5 Fixed Queries**: Each mapped to a ground truth tool.
- **Scaling**: Start with 5 tools, increase 1 each time until model fail to select correct tool.
- **Metrics Logged**:
  - Exception Rate (how many exception occurs out of 5 queries)
  - Tool Execution Success Rate (how many time tools are actually executed out of 5 queries)
  - Correct Tool Selection Rate  (how many time correct tool is selected out of 5 queries)
  - Average Latency (average time taken to respond 5 queries)

## 📁 Structure
- `maxtool.ipynb`: Automates multi-run tool testing.
- `experiment_logs/`: Contains CSVs, logs for each model run with timestamp and key hyperparameters.
- `count_token.ipynb`: early attemp in counting tool set tokens.
- `README.md`: This document.

## 💡 Key Insights So Far
- (**26 Mar**) Ruled out temperature as a factor. Even with the temperature set to 0.001, we observed a maximum of 11, 16, and 15 tools in three runs. Temporarily shifting focus to MCP tasks. Will wrap up updates and revisit later.

- (**24 Mar**) The 3B model last week consistently handled 24 tools. However, this week with v0.1.8, it handled 11, 18, and 23 tools in three different runs. Suspect temperature-related parameters were changed for the 3B model. The 8B model will be tested to see if it follows the same pattern. A draft token count script `count_token.ipynb` has been created.
  - Findings: Currently, v1.8 supports token metrics but only for the `client.inference.chat_completion` function. It is only the first step out of 3 for `response = agent.create_turn(` when involving tool calls
  - still working on how to proper count token used for tool sets following llamastack way. 

- (**20 Mar**) 
  - Improved the maxtool test script with a diverse fake tool generation method. 
  - Refined the script for later scale experiments with logs and switched to an IPython notebook for better visualization.
  - findings:  
    - LLaMA-8B can handle around **21 tools** (3B is about 24) before misidentifying the correct one.
    - **Extending tool descriptions** reduced that number to **18**, suggesting performance is bound by docstring.
    - **Extending tool name** reduced that number further to **17**, suggesting performance is bound by tool name.
    - **Extending tool return message** does not affect.
    - (suspect) Models may either:
      - Prioritize **later tools** in prompt context (due to recency bias).
      - Or, after exceeding a threshold, **fail to abstract and match** any tools, even among the first few.
    - Even when inference still returns a response, the selected tool may be incorrect or invalid.
    - leading to investigate token size for tools.
    - **Local vs. cluster-hosted models** (e.g., on NERC) behave differently—even for identical 3B models—likely due to variations in runtime or configuration (e.g., token limit in VLLM's `run.yaml`).

- (**by 11 Mar**) Developed the initial max tool test script. However, the fake tools lacked diversity, resulting in overly optimistic max tool counts. Spent time reading and finding existing benchmark literature.

## TODOs 
- [ ] Add token usage tracking to confirm max tool tokens for each model. (its not the token budge for model like max context length, its the max token size that model can call correct tool from a tool set.)
- [ ] Draw graphs comparing model size vs. tool capacity vs. tool token budget.
- [ ] Expand testing to additional models (e.g., 13B, possibly 70B via cluster).
- [ ] Compare local vs. hosted model behavior in a controlled setting.
less priority
- [ ] investigate if given similar tools how this affect?
- [ ] whats the minimum token size for describing a tool?
- [ ] Identify and summarize suitable benchmark datasets.
- [ ] Calculate accuracy using appropriate benchmarks.
- [ ] Continue refining metrics and identifying influencing factors.
- [ ] Develop a suitable system prompt wrapper for user queries to ensure the correct tool is executed.

#### Limitations
- **Fake tools are highly similar**, making them easy to distinguish from real tools, also no parameter.
- **Only 5 queries**, limiting diversity in tool usage.
- **Model may perform better here** than in real-world scenarios with more diverse tools.

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