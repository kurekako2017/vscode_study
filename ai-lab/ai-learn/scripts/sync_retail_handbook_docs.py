#!/usr/bin/env python3
"""Synchronize paired retail-insight-ai and handbook markdown docs.

This keeps a small sync block in every mapped file. The block is intentionally
append-only and local to a fenced marker so that project-specific prose stays
independent while the shared sync metadata stays in lockstep.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import time
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "doc-sync.manifest.json"


@dataclasses.dataclass(frozen=True)
class SyncFile:
    group: str
    relpath: str
    path: Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_sync_block(content: str, group: str) -> tuple[str, str | None, str]:
    start_marker = f"<!-- DOC-SYNC:START group={group} -->"
    end_marker = f"<!-- DOC-SYNC:END group={group} -->"
    start = content.find(start_marker)
    end = content.find(end_marker)
    if start == -1 or end == -1 or end < start:
        return content.rstrip(), None, ""
    end += len(end_marker)
    before = content[:start].rstrip()
    block = content[start:end].rstrip()
    after = content[end:].lstrip()
    return before, block, after


def extract_excerpt(text: str, limit: int = 4) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("<!-- DOC-SYNC:"):
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    if not lines:
        return "（空文档）"
    excerpt = " / ".join(lines)
    return excerpt[:220]


def render_block(
    group: str,
    file: SyncFile,
    peers: Iterable[SyncFile],
    own_text: str,
    peer_texts: dict[str, str],
) -> str:
    peer_rows = []
    for peer in peers:
        peer_text = peer_texts[peer.relpath]
        peer_rows.append(
            f"- `{peer.relpath}` | sha256={sha256_text(peer_text)} | {extract_excerpt(peer_text)}"
        )
    own_hash = sha256_text(own_text)
    block_lines = [
        f"<!-- DOC-SYNC:START group={group} -->",
        f"## 文档同步块",
        "",
        f"- group: `{group}`",
        f"- file: `{file.relpath}`",
        f"- self_sha256: `{own_hash}`",
        "- peers:",
        *peer_rows,
        "",
        "说明：",
        "- 这个块由 `scripts/sync_retail_handbook_docs.py` 自动维护。",
        "- 只同步这个块，不覆盖各自正文。",
        "- 任一组内文档正文变化时，整组文档的同步块都会一起刷新。",
        f"<!-- DOC-SYNC:END group={group} -->",
    ]
    return "\n".join(block_lines).rstrip() + "\n"


def update_file(file: SyncFile, peers: list[SyncFile], peer_texts: dict[str, str]) -> bool:
    original = peer_texts[file.relpath]
    before, _, after = split_sync_block(original, file.group)
    block = render_block(file.group, file, peers, original, peer_texts)
    parts = [before.rstrip()]
    if before.strip():
        parts.append("")
    parts.append(block.rstrip())
    if after.strip():
        parts.append("")
        parts.append(after.lstrip())
    new_content = "\n".join(parts).rstrip() + "\n"
    if new_content != original:
        write_text(file.path, new_content)
        return True
    return False


def load_manifest() -> list[tuple[str, list[str]]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    groups = manifest.get("groups", [])
    result: list[tuple[str, list[str]]] = []
    for group in groups:
        name = group["name"]
        paths = group["paths"]
        result.append((name, paths))
    return result


def build_files() -> list[tuple[str, list[SyncFile]]]:
    groups: list[tuple[str, list[SyncFile]]] = []
    for group_name, relpaths in load_manifest():
        files: list[SyncFile] = []
        for relpath in relpaths:
            path = ROOT / relpath
            if not path.exists():
                raise FileNotFoundError(f"Missing mapped file: {relpath}")
            files.append(SyncFile(group=group_name, relpath=relpath, path=path))
        groups.append((group_name, files))
    return groups


def sync_once(groups: list[tuple[str, list[SyncFile]]]) -> int:
    peer_texts = {
        file.relpath: read_text(file.path)
        for _, files in groups
        for file in files
    }
    changed = 0
    for _, files in groups:
        for file in files:
            peers = [peer for peer in files if peer.path != file.path]
            if update_file(file, peers, peer_texts):
                changed += 1
    return changed


def snapshot(groups: list[tuple[str, list[SyncFile]]]) -> dict[str, str]:
    state: dict[str, str] = {}
    for _, files in groups:
        for file in files:
            state[file.relpath] = sha256_text(read_text(file.path))
    return state


def watch(groups: list[tuple[str, list[SyncFile]]], interval: float) -> None:
    last = snapshot(groups)
    while True:
        time.sleep(interval)
        current = snapshot(groups)
        if current == last:
            continue
        sync_once(groups)
        last = snapshot(groups)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watch", action="store_true", help="Keep syncing in a polling loop.")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds.")
    args = parser.parse_args()

    groups = build_files()
    sync_once(groups)
    if args.watch:
        watch(groups, args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
