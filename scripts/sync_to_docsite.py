#!/usr/bin/env python3
"""Sync approved screenshot and GIF assets into genkit-docsite repository."""

import argparse
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_FILE = REPO_ROOT / "registry.json"

def sync_assets(shots_dir: Path, docsite_dir: Path):
    if not REGISTRY_FILE.exists():
        print("Error: registry.json not found.")
        return

    registry = json.loads(REGISTRY_FILE.read_text())
    print(f"▶ Syncing {len(registry)} assets to {docsite_dir}...")

    synced = 0
    for item in registry:
        sid = item["id"]
        fmt = item.get("format", "png")
        src_file = shots_dir / f"{sid}.{fmt}"
        target_path = docsite_dir / item["targetDocPath"]

        if not src_file.exists():
            print(f"  ⚠ Missing source file: {src_file.name}")
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, target_path)
        print(f"  ✓ Copied {src_file.name} -> {item['targetDocPath']}")
        synced += 1

    print(f"\n✨ Successfully synced {synced} assets into docsite.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync assets to docsite")
    parser.add_argument("--shots-dir", default=str(Path.home() / "Desktop/genkit-docsite-shots/proposed"), help="Source shots directory")
    parser.add_argument("--docsite-dir", default=str(Path.home() / "Desktop/genkit-docsite"), help="Target docsite directory")
    args = parser.parse_args()

    sync_assets(Path(args.shots_dir), Path(args.docsite_dir))
