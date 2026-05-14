# Test 1 Evaluation: Cross-Model Memory Handoff

## What Is Test 1?

Test 1 checks whether Mem0 can carry useful context from one LLM to another.

The flow is:

1. Clear Mem0 memory.
2. Use Nemotron to research VLA models and world models across several prompts.
3. Let Mem0 auto-store key findings.
4. Switch to Kimi.
5. Ask Kimi to continue the work using only the memories Nemotron created.

The core question:

> Does Kimi behave like it inherited useful notes from Nemotron, or does it basically start from scratch?

## What Are We Trying To Learn?

We are testing whether Mem0 works as a real shared memory layer across models, not just as a passive note database.

Specifically:

- Can one model store useful research context?
- Can another model retrieve and use it?
- Does memory reduce repetition?
- Does the second model build on prior work?
- Can the second model critique or update previous findings?

## Evaluation Metrics

1. **Memory visibility**
   - Could Kimi access Nemotron's stored memories?

2. **Specificity of recall**
   - Did Kimi cite concrete prior findings, model names, claims, or open questions?

3. **Avoidance of repetition**
   - Did Kimi skip basic explanations already covered?

4. **Continuity**
   - Did Kimi's answer feel like a continuation of prior work?

5. **Novel contribution**
   - Did Kimi add new findings beyond Nemotron's output?

6. **Critical reasoning**
   - Could Kimi challenge stored claims instead of blindly accepting them?

7. **Memory quality**
   - Were stored memories specific, useful, and non-duplicative?

8. **Net workflow value**
   - Was this better than manually pasting a summary into Kimi?

