from __future__ import annotations

import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("output")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def describe_json(path: Path) -> None:
    data = load_json(path)

    print("=" * 80)
    print(f"FILE: {path.name}")
    print(f"TYPE: {type(data).__name__}")

    if isinstance(data, dict):
        print(f"KEYS: {list(data.keys())}")
        print("SAMPLE:")
        sample = {k: data.get(k) for k in list(data.keys())[:10]}
        print(json.dumps(sample, ensure_ascii=False, indent=2)[:1500])

    elif isinstance(data, list):
        print(f"COUNT: {len(data)}")
        if data:
            first = data[0]
            print(f"FIRST_TYPE: {type(first).__name__}")
            if isinstance(first, dict):
                print(f"FIRST_KEYS: {list(first.keys())}")
                print("FIRST_SAMPLE:")
                print(json.dumps(first, ensure_ascii=False, indent=2)[:1500])
            else:
                print(str(first)[:1500])
    else:
        print(str(data)[:1500])


def main() -> None:
    policy_files = sorted(OUTPUT_DIR.glob("*_policy.json"))
    chunk_files = sorted(OUTPUT_DIR.glob("*_chunks.json"))
    raw_files = sorted(OUTPUT_DIR.glob("*_raw.json"))

    print(f"policy_files: {len(policy_files)}")
    print(f"chunk_files: {len(chunk_files)}")
    print(f"raw_files: {len(raw_files)}")

    print("\n--- POLICY SAMPLES ---")
    for path in policy_files[:2]:
        describe_json(path)

    print("\n--- CHUNK SAMPLES ---")
    for path in chunk_files[:2]:
        describe_json(path)


if __name__ == "__main__":
    main()