# Test 1 — Phase 1: Nemotron
## Cross-Model Memory Handoff

---

## Clear memory first
```bash
python mem0_helper.py clear
python mem0_helper.py list   # should say "Memory is empty"
```

---

## Run 3 prompts in sequence

Each call auto-retrieves prior memories and auto-stores new findings.
Just run them and watch.

### Prompt 1 — VLA Landscape
```bash
python mem0_helper.py agent "What are the leading Vision-Language-Action model architectures right now? Cover RT-2, OpenVLA, pi-zero, and Octo. Who built each, what makes them architecturally distinct, and what training data do they use?" --model nemotron
```

### Prompt 2 — World Models
```bash
python mem0_helper.py agent "How do world models connect to VLA research in robotics? Cover DreamerV3, GAIA-1, and DIAMOND. Is there hard evidence world models actually improve robot performance or is it mostly theoretical?" --model nemotron
```

### Prompt 3 — Open Questions
```bash
python mem0_helper.py agent "Based on everything established so far about VLAs and world models, what are the 3-5 biggest genuinely unresolved questions in this field? What would you want answered before making an early-stage investment?" --model nemotron
```

---

## After all 3 prompts, inspect memory

```bash
python mem0_helper.py list
```

### What to note:
- How many memories were auto-stored?
- Are they specific (model names, claims) or vague summaries?
- Did Prompt 3 acknowledge what Prompts 1-2 established?
- Any duplicates?

**Do NOT clear memory.** Kimi needs to read these in the next phase.