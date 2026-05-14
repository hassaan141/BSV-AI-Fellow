#!/usr/bin/env python3
"""
mem0_helper.py — Mem0 memory layer + NVIDIA Build LLM agent

Usage:
  python mem0_helper.py add "your finding here"
  python mem0_helper.py search "what you want to recall"
  python mem0_helper.py list
  python mem0_helper.py clear
  python mem0_helper.py agent "your prompt" --model nemotron
  python mem0_helper.py agent "your prompt" --model kimi
"""

import sys
from openai import OpenAI
from mem0 import MemoryClient

# ── Config ────────────────────────────────────────────────────────────────────

USER_ID = "vla-research-session"

# Put your real keys here locally.
MEM0_API_KEY = "m0-k6WnFRRZWPO5skpDIDL7RvtFcRiaxLvCfmA1urr7"
NVIDIA_NEMOTRON_API_KEY = "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"
NVIDIA_MINIMAX_API_KEY = "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"

NVIDIA_BASE = "https://integrate.api.nvidia.com/v1"

MODELS = {
    "nemotron": {
        "id": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        "client": OpenAI(
            base_url=NVIDIA_BASE,
            api_key=NVIDIA_NEMOTRON_API_KEY,
        ),
    },
    "kimi": {
        "id": "minimaxai/minimax-m2.7",
        "client": OpenAI(
            base_url=NVIDIA_BASE,
            api_key=NVIDIA_MINIMAX_API_KEY,
        ),
    },
}

mem = MemoryClient(api_key=MEM0_API_KEY)


# ── Result normalization ──────────────────────────────────────────────────────

def normalize_results(response):
    """
    Mem0 SDK versions can return:
    - list[dict]
    - dict with results/memories/data
    - dict with nested memory list

    This makes list/search robust.
    """
    if response is None:
        return []

    if isinstance(response, list):
        return response

    if isinstance(response, dict):
        for key in ["results", "memories", "data"]:
            value = response.get(key)
            if isinstance(value, list):
                return value

        # Fallback: sometimes dict values contain the actual list.
        for value in response.values():
            if isinstance(value, list):
                return value

    return []


def get_memory_text(item):
    if isinstance(item, dict):
        return (
            item.get("memory")
            or item.get("text")
            or item.get("content")
            or item.get("value")
            or str(item)
        )

    return str(item)


def get_created_at(item):
    if isinstance(item, dict):
        created_at = item.get("created_at") or item.get("created") or ""
        return str(created_at)[:10]

    return ""


# ── Memory helpers ────────────────────────────────────────────────────────────

def add(content: str):
    mem.add(
        [{"role": "assistant", "content": content}],
        user_id=USER_ID,
    )
    print(f"✅ Stored: {content[:80]}...")


def search(query: str):
    response = mem.search(
        query,
        filters={"user_id": USER_ID},
        limit=10,
    )
    results = normalize_results(response)

    if not results:
        print("No memories found.")
        return

    print(f"\n📚 Memories relevant to: '{query}'\n")

    for i, item in enumerate(results, 1):
        created_at = get_created_at(item)
        memory_text = get_memory_text(item)
        print(f"  {i}. [{created_at}] {memory_text}")


def list_all():
    response = mem.get_all(filters={"user_id": USER_ID})
    results = normalize_results(response)

    if not results:
        print("Memory is empty.")
        return

    print(f"\n📋 All stored memories ({len(results)} total):\n")

    for i, item in enumerate(results, 1):
        created_at = get_created_at(item)
        memory_text = get_memory_text(item)
        print(f"  {i}. [{created_at}] {memory_text}")


def clear():
    try:
        mem.delete_all(filters={"user_id": USER_ID})
    except Exception:
        mem.delete_all(user_id=USER_ID)

    print(f"Cleared memories for user_id={USER_ID}")


# ── Agent ─────────────────────────────────────────────────────────────────────

def agent(prompt: str, model_key: str = "nemotron"):
    if model_key not in MODELS:
        valid = ", ".join(MODELS.keys())
        print(f"Invalid model '{model_key}'. Valid models: {valid}")
        sys.exit(1)

    cfg = MODELS[model_key]
    client = cfg["client"]
    model = cfg["id"]

    # 1. Retrieve relevant memories.
    response = mem.search(
        prompt,
        filters={"user_id": USER_ID},
        limit=8,
    )
    memories = normalize_results(response)

    memory_block = ""

    if memories:
        memory_block = "\n".join(
            f"- {get_memory_text(item)}"
            for item in memories
        )
        print(f"\n🧠 Retrieved {len(memories)} relevant memories\n")
    else:
        print("\n🧠 No prior memories found\n")

    # 2. Build prompt with memory.
    system = f"""
You are a research agent specializing in robotics, Vision-Language-Action models,
and world models for embodied AI.

Prior memory:
{memory_block if memory_block else "Nothing stored yet."}

Instructions:
- Do not repeat findings already in memory.
- Be specific: model names, paper titles, lab names, datasets, numbers, and dates where relevant.
- If memory is empty, establish foundational facts first.
- End with a section titled exactly: STORE THESE FINDINGS
- Under STORE THESE FINDINGS, list 3 to 5 atomic facts that should be saved to memory.
"""

    # 3. Call LLM.
    print(f"🤖 Calling {model_key} ({model})...\n")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )

    output = response.choices[0].message.content or ""
    print(output)

    # 4. Auto-store findings.
    if "STORE THESE FINDINGS" in output:
        section = output.split("STORE THESE FINDINGS", 1)[-1].strip()

        lines = []
        for raw_line in section.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            line = line.lstrip("-•* ")
            line = line.lstrip("0123456789. )").strip()

            if len(line) > 20:
                lines.append(line)

        stored = 0

        for line in lines[:5]:
            mem.add(
                [{"role": "assistant", "content": line}],
                user_id=USER_ID,
            )
            stored += 1

        print(f"\n✅ Auto-stored {stored} findings to Mem0")
    else:
        fallback = output[:600].strip()

        if fallback:
            mem.add(
                [{"role": "assistant", "content": fallback}],
                user_id=USER_ID,
            )
            print("\n✅ Response stored to Mem0")
        else:
            print("\n⚠️ Empty response, nothing stored")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "add" and len(sys.argv) >= 3:
        add(" ".join(sys.argv[2:]))

    elif cmd == "search" and len(sys.argv) >= 3:
        search(" ".join(sys.argv[2:]))

    elif cmd == "list":
        list_all()

    elif cmd == "clear":
        clear()

    elif cmd == "agent" and len(sys.argv) >= 3:
        args = sys.argv[2:]
        model = "nemotron"

        if "--model" in args:
            idx = args.index("--model")

            if idx + 1 >= len(args):
                print("Missing model name after --model")
                sys.exit(1)

            model = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

        prompt = " ".join(args).strip()

        if not prompt:
            print("Missing prompt.")
            sys.exit(1)

        agent(prompt, model)

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()