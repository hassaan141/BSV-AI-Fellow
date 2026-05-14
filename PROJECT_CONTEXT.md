# BSV AI Fellow Project Context

Last updated: 2026-05-14

This file is the shared working memory for the Basis Set Ventures AI Fellow project. Use it to re-enter the project quickly, understand the current direction, and avoid re-discovering decisions that have already been made.

## Assignment Snapshot

Basis Set Ventures asks for:

1. A ranked prioritization of the listed startups, with concise criteria and rationale.
2. A lightweight diligence writeup for one selected company, including hands-on testing.
3. One LLM conversation showing the real process of building, analyzing, critiquing, or exploring the product.

The guidance says "less is more" for the final writeup. They want evidence of judgment, experimentation, and how the candidate thinks through ambiguity, not a generic LLM-style company summary.

## Current Project Direction

The repo is currently focused on Track 1: Developer Tools.

Top-company deep dive appears to be Mem0, tested as a developer infrastructure product for persistent memory across LLM sessions and models. The core evaluation question is:

> Does Mem0 behave like a useful memory layer that materially changes agent behavior across sessions and model boundaries, or is it mostly a retrievable note store with extra friction?

This is a strong diligence angle because it uses the product in a real workflow instead of just reading docs. It also maps well to BSV's interest in productivity infrastructure and AI-native workflows.

## Repo Inventory

Root files:

- `README.md`: Current project README for the Mem0 deep dive. Explains the testing goal, setup, commands, and test suite.
- `CLAUDE_TASK.md`: A research brief for a Claude Code phase on VLA/world-model research. It frames an earlier memory-handoff experiment.
- `mem0_helper.py`: CLI helper that connects Mem0 with NVIDIA-hosted LLMs. It supports manual memory operations and an `agent` command that retrieves relevant memories, injects them into the system prompt, calls a selected model, and auto-stores new findings.
- `venv/`: Local virtual environment with dependencies.
- `task_1/`: Cross-model handoff test plan.
- `task_3/`: Debugging-across-sessions test plan plus a deliberately broken Python script.
- `task_4/`: Iterative research-loop test plan.

There is no `.git` directory in this workspace.

## Existing Technical Artifact

`mem0_helper.py` is the main artifact. It defines:

- `add`: store a memory for the fixed user id.
- `search`: retrieve memories relevant to a query.
- `list`: show all stored memories.
- `clear`: delete memories for the current user id.
- `agent`: retrieve memories, inject them into an LLM prompt, call Nemotron or Kimi through NVIDIA Build, and auto-store 3 to 5 extracted facts from the response.

Important implementation details:

- Fixed `USER_ID`: `vla-research-session`.
- Models:
  - `nemotron`: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`
  - `kimi`: `minimaxai/minimax-m2.7`
- Retrieval limit: 8 memories for agent context, 10 for search.
- Storage behavior: if the model output contains `STORE THESE FINDINGS`, the helper parses bullet-like lines from that section and stores up to 5 of them.

## Critical Hygiene Note

`mem0_helper.py` currently contains hardcoded API keys for Mem0 and NVIDIA. Before submitting or sharing the repo, move keys into environment variables or a local `.env` file and redact them from the code.

Suggested improvement:

- Use `os.getenv("MEM0_API_KEY")`
- Use `os.getenv("NVIDIA_NEMOTRON_API_KEY")`
- Use `os.getenv("NVIDIA_MINIMAX_API_KEY")`
- Add a short failure message if any key is missing.
- Do not commit or submit real keys.

## Test Plans Already Present

### Test 1: Cross-Model Memory Handoff

Files:

- `task_1/test1_nemotron.md`
- `task_1/test1_kimi.md`

Purpose:

Check whether Nemotron can research VLA/world-model topics, store useful memories, and then Kimi can pick up from that memory pool without starting cold.

What it measures:

- Whether Kimi can see Nemotron's memories.
- Whether Kimi references specific prior findings.
- Whether Kimi avoids repeating basics.
- Whether Kimi adds new information.
- Whether Kimi can challenge prior memories rather than passively agree.

Core judgment question:

Did switching from Nemotron to Kimi feel like handing notes to a colleague, or like starting a new chat with a context dump?

### Test 3: Debugging Across Sessions

Files:

- `task_3/test3_session1.md`
- `task_3/test3_session2.md`
- `task_3/test3_debug.py`

Purpose:

Check whether Mem0 can preserve debugging state across sessions and models.

The deliberately broken script drops one record from a 10-record batch. The real bug is an off-by-one error in `chunk_list()`:

```python
for i in range(0, len(items) - 1, chunk_size):
```

It should use:

```python
for i in range(0, len(items), chunk_size):
```

Red herrings:

- The async pattern in `process_batch()`.
- The regex normalization in `clean_record()`.
- The `defaultdict` use.

What it measures:

- Whether the second model retrieves the first model's debugging notes.
- Whether it skips already-ruled-out explanations.
- Whether it goes straight to the actual suspect area.
- Whether it can suggest the fix without seeing the code again.

Core judgment question:

Did memory save debugging time, or would it have been easier to paste the full code into the next model?

### Test 4: Iterative Research Loop

File:

- `task_4/test4_loop.md`

Purpose:

Check whether memory compounds across multiple research loops or merely accumulates noisy facts.

Structure:

1. Nemotron establishes VLA model foundations.
2. Nemotron goes deeper on world models for robotics.
3. Kimi synthesizes open problems and investment moats from the accumulated memory.

What it measures:

- Memory count growth.
- Duplicate or near-duplicate memories.
- Whether later loops reference earlier loops.
- Whether output quality improves, plateaus, or degrades.
- Whether Mem0's extraction preserves specifics or summarizes them away.

Core judgment question:

Is the final memory list a compounding research asset, or just a loose pile of facts a single strong prompt could have produced?

## Current Evidence Gap

The repo currently contains test plans and harness code, but not clearly labeled captured outputs from actual completed runs. The final BSV submission will be stronger if it includes:

- Raw or lightly cleaned transcripts from each test run.
- Memory counts after each phase.
- Examples of useful memories.
- Examples of vague, duplicate, or misleading memories.
- A short reflection on where Mem0 helped and where it added friction.

Recommended file additions:

- `task_1/results.md`
- `task_3/results.md`
- `task_4/results.md`
- `final/prioritization.md`
- `final/mem0_diligence.md`
- `final/llm_conversation.md`

## Likely Final Thesis

Working thesis, to revise after actual run outputs:

Mem0 is most compelling when memory is structured around explicit, reusable state such as "what was ruled out," "what the next agent should inspect," or "facts already established." It is less clearly differentiated when the task is one-shot research, where a long context window or a pasted summary may be enough.

The product's value depends on memory extraction quality. If extraction stores precise, atomic facts and caveats, it can make multi-agent work feel continuous. If it stores vague summaries or duplicates, the retrieval layer becomes another context-management burden.

## Prioritization Angle

For the ranked-company response, a good lens is "how much can this product become infrastructure for AI-native work?"

Possible criteria:

- Frequency and pain of the workflow.
- Strength of wedge into a developer or operator habit.
- Evidence of product-led adoption.
- Differentiation in an AI-infrastructure stack.
- Ability to create or own persistent context/data over time.
- Fit with BSV's thesis around productivity and transforming work.

Mem0 can rank high because persistent memory is a real pain in agentic workflows, and the hands-on test directly probes whether the product creates durable context across tools and models.

## Suggested Prioritization Direction

This is not final, but a plausible starting point:

1. Mem0: Persistent memory layer for AI apps and agents. Strong fit with agentic infrastructure; easy to test hands-on; clear question around whether memory quality compounds.
2. BAML: Developer tooling for structured LLM application development. Strong developer-experience wedge; likely high relevance as LLM apps need reliability and typed workflows.
3. Atuin: Shell history and developer productivity. Strong habit loop and open-source motion; less directly AI-native unless positioned around developer workflow data.
4. Rasa: Mature conversational AI platform. Credible but may feel less early-stage and less novel for this exercise.
5. Tigris Data: Data/storage infrastructure. Potentially useful but harder to evaluate quickly without broader market context.
6. Parasail: Needs more research; likely AI infrastructure angle, but current repo has not examined it.
7. Primitive: Needs more research; unclear thesis from current artifacts.
8. Entire: Needs more research; unclear thesis from current artifacts.

Do not treat this as final without doing at least quick public research on the non-Mem0 companies.

## Hands-On Commands

Setup:

```bash
pip install mem0ai openai python-dotenv
```

Core helper commands:

```bash
python mem0_helper.py clear
python mem0_helper.py list
python mem0_helper.py search "query"
python mem0_helper.py agent "prompt" --model nemotron
python mem0_helper.py agent "prompt" --model kimi
```

Debug test:

```bash
python task_3/test3_debug.py
```

Expected failure before fix:

```text
AssertionError: Record count mismatch: got 9, expected 10
```

## Submission Shape

Final submission should feel like a compact investor/product judgment memo, not a benchmark paper.

Suggested structure:

1. Prioritization framework and ranked list.
2. Mem0 diligence:
   - Why selected.
   - What was built/tested.
   - What worked.
   - What broke or felt fragile.
   - Product and market implications.
   - What to test next.
3. LLM conversation:
   - Include a real transcript or excerpt showing the back-and-forth with Codex/Claude/Kimi/Nemotron.
   - Preserve evidence of uncertainty, failed paths, and course corrections.

## Recommended Next Steps

1. Redact hardcoded keys in `mem0_helper.py`.
2. Run the three test suites and capture actual outputs.
3. Fill in `results.md` files with observations and screenshots if useful.
4. Do quick public research on the other listed companies before finalizing the ranked list.
5. Write the final Mem0 diligence around observed behavior, not just intended behavior.
6. Keep the final voice personal and judgment-driven: "I expected X, observed Y, and that changed my view because Z."

## Open Questions To Resolve

- Did Mem0's retrieval consistently surface the right memories for changed wording?
- Were stored memories atomic and specific enough to guide another model?
- Did the second model actually change behavior because of memory?
- How much setup friction exists for a developer integrating Mem0 into a real workflow?
- Are the strongest use cases debugging handoff, research handoff, customer-support memory, personal assistant memory, or agent workflow state?
- What would Mem0 need to prove to become durable infrastructure rather than a convenience layer?

