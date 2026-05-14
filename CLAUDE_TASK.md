# Phase 1 — Claude Code Research Brief
## Topic: Vision-Language-Action Models & World Models

You are the first research agent on this project. Your job is to investigate
the current state of VLA models and world models in robotics, then store your
findings to shared memory so the next agent (Codex) can continue without
starting from scratch.

---

## Your Research Questions

1. **What are the leading VLA architectures right now?**
   - Key models: RT-2, OpenVLA, π0 (pi-zero), Octo — what makes each distinct?
   - Who are the leading labs? (Google DeepMind, Physical Intelligence, Stanford, CMU)
   - What's the dominant training approach — co-training on web + robot data?

2. **Where do world models fit in?**
   - What role do world models play in current VLA pipelines?
   - Are any VLAs using explicit world models, or is it mostly implicit?
   - Key projects: GAIA-1, DreamerV3, DIAMOND — which are relevant to robotics?

3. **What's the honest state of sim-to-real transfer?**
   - What actually works in the real world vs. only in simulation?
   - What are the main failure modes?

4. **What open questions should the next agent dig into?**

---

## How to Store Your Findings

After researching each question, store your findings using the helper script.
Be specific — model names, paper titles, concrete claims, not summaries.

```bash
# Store a finding
python mem0_helper.py add "RT-2 from Google DeepMind co-trains on web data and robot demonstrations, uses a PaLI-X backbone, key insight is that web-scale vision-language pretraining transfers to robot control"

python mem0_helper.py add "Physical Intelligence's pi-zero uses a flow-matching policy on top of a VLM, notable because it achieves dexterous manipulation across 68 tasks with a single model"

python mem0_helper.py add "Main open question: no VLA has convincingly solved long-horizon task planning beyond 3-4 step sequences in unstructured environments"

# Store gaps and open questions explicitly
python mem0_helper.py add "OPEN QUESTION for Codex: what is the evidence that world models actually help VLA performance, or is this mostly theoretical right now?"
```

Store at least 8-10 specific findings before handing off.

---

## Output

After storing memories, write a brief `PHASE1_NOTES.md` summarising:
- What you found
- What you stored to memory
- What you're leaving for Codex to investigate

Then run:
```bash
python mem0_helper.py list
```
to verify everything was stored correctly.
