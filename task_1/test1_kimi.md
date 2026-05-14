# Test 1 — Phase 2: Kimi
## Cross-Model Memory Handoff

Nemotron has done 3 rounds of VLA research. Memory is populated.
Now Kimi picks up with a DIFFERENT model reading the SAME memory pool.

---

## First: verify Nemotron's memories are visible

```bash
python mem0_helper.py list
python mem0_helper.py search "VLA architectures"
```

If empty — the handoff already failed. Document that.

---

## Run 3 prompts — Kimi should build on Nemotron's work

### Prompt 1 — Does Kimi know what Nemotron found?
```bash
python mem0_helper.py agent "What has already been established about VLA models and world models in prior research? Summarise what you know from memory, then identify what gaps remain." --model kimi
```

**Watch for:** Does Kimi cite specific findings from Nemotron's session?
Or does it ignore memory and start fresh?

### Prompt 2 — Go deeper on a gap
```bash
python mem0_helper.py agent "Focus on the data moat problem in VLA research. How much robot demonstration data do leading models actually need? Who controls the data advantage — Google DeepMind, Physical Intelligence, or academic labs? Is co-training on web data sustainable?" --model kimi
```

**Watch for:** Does Kimi avoid re-explaining what VLAs are?
It should already know from memory.

### Prompt 3 — Cross-check and contradict
```bash
python mem0_helper.py agent "Challenge the findings stored in memory. What claims from prior research sessions might be wrong, outdated, or overly optimistic? Be specific about which stored claims you disagree with and why." --model kimi
```

**Watch for:** This is the hardest test. Can Kimi read stored memories
and push back on them? Or does it just agree with everything?

---

## After all prompts, inspect the full memory

```bash
python mem0_helper.py list
```

### Evaluation checklist:

| Question | Answer |
|----------|--------|
| Could Kimi see Nemotron's memories? | Yes / No / Partial |
| Did Kimi reference specific Nemotron findings? | Yes / No |
| Did Kimi avoid repeating VLA basics? | Yes / No |
| Did Kimi add genuinely new findings? | Yes / No |
| Did Kimi challenge any stored claims? | Yes / No |
| Total memories now vs after Nemotron phase? | ___ vs ___ |
| Any duplicates between Nemotron and Kimi memories? | Yes / No |

---

## The Core Question

> Did switching from Nemotron to Kimi feel like a genuine handoff —
> like passing notes to a colleague? Or did Kimi essentially start
> a new conversation that happened to have some context injected?

The difference matters. A real handoff means the second agent's output
is materially different than if it had started cold. Document which one
you observed.