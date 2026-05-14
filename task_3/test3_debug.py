"""
data_pipeline.py — deliberately broken script for Test 3

There are multiple suspicious-looking things in this file.
Only ONE is the actual bug. The others are red herrings.

Red herrings (these are fine, do not fix):
  - The async pattern in process_batch() looks unusual but is correct
  - The re import and usage looks odd but works fine
  - The defaultdict usage looks overcomplicated but is not the bug

Real bug:
  - Off-by-one error in chunk_list() causes the last item to always be dropped
"""

import asyncio
import re
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chunk_list(items: list[Any], chunk_size: int) -> list[list[Any]]:
    """Split a list into chunks of chunk_size. BUG IS HERE."""
    chunks = []
    # Bug: range should be len(items) not len(items) - 1
    # This silently drops the last item every time
    for i in range(0, len(items) - 1, chunk_size):
        chunks.append(items[i : i + chunk_size])
    return chunks


def clean_record(record: dict[str, Any]) -> dict[str, Any]:
    """Clean whitespace and normalize keys. Looks suspicious, actually fine."""
    pattern = re.compile(r"\s+")
    return {
        re.sub(pattern, "_", k.strip().lower()): v
        for k, v in record.items()
    }


async def process_batch(
    batch: list[dict[str, Any]],
    results: dict[str, list],
) -> None:
    """Async batch processor. Unusual pattern but correct."""
    await asyncio.sleep(0)  # yield control — intentional, not a bug
    for record in batch:
        cleaned = clean_record(record)
        status = cleaned.get("status", "unknown")
        results[status].append(cleaned)


async def run_pipeline(records: list[dict[str, Any]]) -> dict[str, list]:
    """Main pipeline entry point."""
    results: dict[str, list] = defaultdict(list)
    chunks = chunk_list(records, chunk_size=3)
    logger.info(f"Processing {len(chunks)} chunks from {len(records)} records")

    tasks = [process_batch(chunk, results) for chunk in chunks]
    await asyncio.gather(*tasks)

    return dict(results)


if __name__ == "__main__":
    # Test data — 10 items, last one always gets dropped due to the bug
    test_records = [
        {"Status": "active", "Name": f"user_{i}"}
        for i in range(10)
    ]

    result = asyncio.run(run_pipeline(test_records))

    total_processed = sum(len(v) for v in result.values())
    logger.info(f"Input: {len(test_records)} records")
    logger.info(f"Output: {total_processed} records")

    # This will print 9 not 10 — the bug
    assert total_processed == len(test_records), (
        f"Record count mismatch: got {total_processed}, "
        f"expected {len(test_records)}"
    )