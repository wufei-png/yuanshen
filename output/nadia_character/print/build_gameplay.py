"""Synchronize the public gameplay section from the canonical Markdown spec."""
from __future__ import annotations

import re
from pathlib import Path

from build_character_notes import convert_blocks

ROOT = Path(__file__).resolve().parents[3]
PAGE = ROOT / "output/nadia_character/gameplay.html"
SOURCE = ROOT / "docs/nadia_gameplay_system.md"
START = "<!-- gameplay-spec:start -->"
END = "<!-- gameplay-spec:end -->"
ANCHORS = {1: "identity", 2: "linchpin", 3: "skills", 4: "state", 5: "rules", 6: "burst", 7: "talents", 8: "constellations", 9: "build", 10: "teams", 11: "validation"}


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8").split("## 12. 开发验收契约", 1)[0]
    sections = re.split(r"(?=^## \d+\.)", text, flags=re.MULTILINE)[1:]
    rendered: list[str] = []
    for index, section in enumerate(sections, 1):
        body = convert_blocks(section)
        body = body.replace("<table>", '<div class="spec-table-wrap"><table class="spec-table">').replace("</table>", "</table></div>")
        rendered.append(f'    <section class="section{ " alt" if index % 2 == 0 else ""}" id="{ANCHORS[index]}"><div class="shell spec-copy">{body}</div></section>')
    page = PAGE.read_text(encoding="utf-8")
    a = page.index(START) + len(START)
    b = page.index(END, a)
    PAGE.write_text(page[:a] + "\n" + "\n".join(rendered) + "\n    " + page[b:], encoding="utf-8")
    print(PAGE)


if __name__ == "__main__":
    main()
