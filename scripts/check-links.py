#!/usr/bin/env python3
"""Check Mintlify navigation entries and local Markdown/MDX links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)|href=[\"']([^\"']+)[\"']")


def iter_nav_pages(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "pages" and isinstance(value, list):
                for page in value:
                    if isinstance(page, str):
                        yield page
                    else:
                        yield from iter_nav_pages(page)
            else:
                yield from iter_nav_pages(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_nav_pages(item)


def strip_anchor_and_query(link: str) -> str:
    return link.split("#", 1)[0].split("?", 1)[0]


def is_external_or_anchor(link: str) -> bool:
    return (
        not link
        or link.startswith("#")
        or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) is not None
    )


def candidates_for(source: Path, link: str) -> list[Path]:
    target = strip_anchor_and_query(link)
    if is_external_or_anchor(target):
        return []

    if target.startswith("/"):
        rel = target.lstrip("/")
        return [ROOT / rel, ROOT / f"{rel}.mdx", ROOT / rel / "index.mdx"]

    base = source.parent / target
    return [base, Path(f"{base}.mdx"), base / "index.mdx"]


def main() -> int:
    errors: list[str] = []

    docs = json.loads((ROOT / "docs.json").read_text())
    for page in iter_nav_pages(docs.get("navigation", {})):
        if not (ROOT / f"{page}.mdx").exists():
            errors.append(f"docs.json references missing page: {page}")

    for source in sorted(ROOT.rglob("*")):
        if ".git" in source.parts or source.suffix not in {".md", ".mdx"}:
            continue
        text = source.read_text(errors="ignore")
        for match in LOCAL_LINK_RE.findall(text):
            link = match[0] or match[1]
            cands = candidates_for(source, link)
            if cands and not any(path.exists() for path in cands):
                errors.append(f"{source.relative_to(ROOT)} links to missing local target: {link}")

    if errors:
        for error in errors:
            print(error)
        print(f"\n{len(errors)} link/navigation error(s) found.", file=sys.stderr)
        return 1

    print("All docs navigation entries and local links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
