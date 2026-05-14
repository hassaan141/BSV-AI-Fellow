# Test 3 — Session 1: Nemotron Debugs
## Debugging Across Sessions

---

## Clear memory first
```bash
python mem0_helper.py clear
```

---

## Step 1: Reproduce the bug yourself

```bash
python test3_debug.py
```

You'll see an AssertionError — input 10 records, output 9.

---

## Step 2: Feed the code + error to Nemotron

Copy the FULL contents of `test3_debug.py` and paste it into this prompt.
The agent will auto-store its debugging findings to memory.

```bash
python mem0_helper.py agent "I am debugging this Python script. It processes 10 records but only 9 come out. Here is the full code:

[PASTE test3_debug.py CONTENTS HERE]

The error is: AssertionError: Record count mismatch: got 9, expected 10.

Investigate the async pattern in process_batch() first — the await asyncio.sleep(0) looks suspicious. Then check the regex usage in clean_record(). Tell me what you rule out and what you suspect." --model nemotron
```

**Important:** Nemotron might find the real bug immediately. That's fine —
what matters is whether it stores its reasoning process, not just the answer.

---

## Step 3: Check what got stored

```bash
python mem0_helper.py list
```

Note:
- Did it store what was ruled out?
- Did it store the suspected cause?
- Are the memories specific enough for another model to use?

**Do NOT clear memory.** Kimi reads these next.