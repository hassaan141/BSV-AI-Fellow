# Test 4 — Iterative Research Loop
## Does memory compound across loops or just accumulate noise?

---

## Clear memory first
```bash
python mem0_helper.py clear
```

---

## Loop 1 — Foundations (Nemotron)

```bash
python mem0_helper.py agent "What are the leading Vision-Language-Action model architectures in 2025-2026? Cover RT-2, OpenVLA, pi-zero, Octo, and any newer models. For each: who built it, key architectural choices, training data used, and benchmark results if known." --model nemotron
```

Check what was stored:
```bash
python mem0_helper.py list
```

Note the count: ___ memories after Loop 1.

---

## Loop 2 — Go Deeper (Nemotron)

Same model, same memory pool. The agent should automatically see Loop 1 findings.

```bash
python mem0_helper.py agent "Go deeper on world models for robotics. How do DreamerV3, GAIA-1, DIAMOND, and UniSim connect to VLA research? Is there hard benchmark evidence that world models improve real robot performance, or is this mostly theoretical? Focus on what has NOT been covered yet." --model nemotron
```

Check memory growth:
```bash
python mem0_helper.py list
```

Note: ___ memories after Loop 2.
- Did it add new memories or duplicate Loop 1?
- Did the response reference Loop 1 findings?

---

## Loop 3 — Synthesis (Switch to Kimi)

Different model reads the accumulated memory from Loops 1-2.

```bash
python mem0_helper.py agent "Synthesise everything established across prior research sessions. What are the genuine open problems in VLA and world models? Where are investment moats forming — data, compute, architecture, or talent? Which companies or labs are best positioned? Be specific and build on what is already known from memory." --model kimi
```

Final memory check:
```bash
python mem0_helper.py list
```

Note: ___ memories after Loop 3.

---

## Evaluation

After all 3 loops:

```bash
python mem0_helper.py list
```

| Question | Answer |
|----------|--------|
| Total memories stored across all loops | |
| Duplicates or near-duplicates | |
| Did Loop 2 reference Loop 1 findings? | Yes / No |
| Did Loop 2 cover NEW territory? | Yes / No |
| Did Loop 3 (Kimi) synthesise across both loops? | Yes / No |
| Did output quality increase each loop? | Yes / No / Plateaued |
| Any memories stored vaguely or incorrectly? | Examples |

---

## The Two Core Questions

**1. Compounding test:**
> Read the final memory list end to end. Is this a compounding research
> asset — genuinely richer than any single prompt could produce? Or is it
> just a list of facts that one good prompt would have surfaced anyway?

**2. Extraction quality test:**
> Compare what the agent SAID in its response vs what Mem0 actually STORED.
> Did Mem0's auto-extraction preserve the important details? Or did it
> summarise away the specifics and keep only vague claims?

Both answers belong in the BSV writeup.