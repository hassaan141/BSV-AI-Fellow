# Test 3 Evaluation: Debugging Across Sessions

## What Is Test 3?

Test 3 checks whether Mem0 can preserve debugging context across model sessions.

The flow is:

1. Clear Mem0 memory.
2. Reproduce a bug in `test3_debug.py`.
3. Ask Nemotron to investigate the bug and store what it ruled out.
4. Switch to Kimi without pasting the code again.
5. Ask Kimi to continue from memory and identify the actual bug.

The core question:

> Does Mem0 help the second model continue debugging from prior reasoning, or would it be easier to paste the code again?

## What Are We Trying To Learn?

We are testing whether Mem0 stores useful debugging state, not just final answers.

Specifically:

- Can it preserve what was already ruled out?
- Can it preserve the suspected bug location?
- Can another model retrieve that reasoning?
- Can the second model avoid repeating dead-end analysis?
- Can the second model find the fix without seeing the code again?

## Expected Bug

The script processes 10 records but outputs only 9.

The real bug is in `chunk_list()`:

```python
for i in range(0, len(items) - 1, chunk_size):
```

It should be:

```python
for i in range(0, len(items), chunk_size):
```

The `len(items) - 1` creates an off-by-one error and drops the final record.

## Evaluation Metrics

| Metric | What To Check |
|---|---|
| Memory visibility | Did Kimi retrieve Nemotron's debugging memories? |
| Ruled-out paths | Did memory preserve that async and regex were not the bug? |
| Focus | Did Kimi go directly to `chunk_list()` or range logic? |
| Correctness | Did Kimi identify the off-by-one bug? |
| Fix quality | Did Kimi propose `range(0, len(items), chunk_size)`? |
| Code-free continuation | Could Kimi solve it without seeing the code again? |
| Net workflow value | Was this faster/better than pasting the full code into Kimi? |

## Commands

```bash
python mem0_helper.py clear
python task_3/test3_debug.py
```

Then run the Nemotron debugging prompt from `test3_session1.md`.

After Nemotron:

```bash
python mem0_helper.py list
```

Then run the two Kimi prompts from `test3_session2.md`.

After Kimi:

```bash
python mem0_helper.py list
```

