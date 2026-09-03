"""Build the offline character-notes reading page from the player-edition Markdown.

Runs from the repository root without third-party dependencies:

    python3 output/nadia_character/print/build_character_notes.py

Outputs:

- ``output/nadia_character/character-notes.html`` (styled reading page, links
  rewritten to in-package pages)
- ``output/nadia_character/docs/nadia_character_player_edition.md`` (packaged
  copy of the source document, links rewritten to in-package pages)
"""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGE_DIR = REPO_ROOT / "output" / "nadia_character"
SOURCE_DOC = REPO_ROOT / "docs" / "nadia_character_player_edition.md"
PACKAGED_DOC = PACKAGE_DIR / "docs" / "nadia_character_player_edition.md"
NOTES_PAGE = PACKAGE_DIR / "character-notes.html"

#: Link rewrites for the reading page (sibling files at package root).
PAGE_REWRITES = (
    (r"[nadia_gameplay_system.md](nadia_gameplay_system.md)", "[完整玩法规格](gameplay.html)"),
    (r"[nadia_voice_script.md](nadia_voice_script.md)", "[语音台词与文件名](index.html#voice)"),
)
#: Link rewrites for the packaged Markdown copy (one directory level up).
MD_REWRITES = (
    (r"[nadia_gameplay_system.md](nadia_gameplay_system.md)", "[完整玩法规格](../gameplay.html)"),
    (r"[nadia_voice_script.md](nadia_voice_script.md)", "[语音台词与文件名](../index.html#voice)"),
)

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
_ORDERED_RE = re.compile(r"^(\d+)\.\s+(.*)$")
_BLOCK_STARTER_RE = re.compile(
    r"^(#{1,3}\s|\||---$|```|>\s|\d+\.\s|-\s)"
)


def render_inline(text: str) -> str:
    """Convert bold and link spans in one escaped inline chunk."""
    text = html_lib.escape(text, quote=False)
    text = _BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    return text


def convert_blocks(markdown: str) -> str:
    """Convert the constrained Markdown subset used by the player-edition doc."""
    lines = markdown.splitlines()
    out: list[str] = []
    index = 0
    total = len(lines)

    def current() -> str:
        return lines[index].strip()

    while index < total:
        line = current()
        if not line:
            index += 1
            continue

        if line.startswith("```"):
            buffer: list[str] = []
            index += 1
            while index < total and not current().startswith("```"):
                buffer.append(lines[index])
                index += 1
            index += 1  # closing fence
            out.append("<pre>" + html_lib.escape("\n".join(buffer), quote=False) + "</pre>")
            continue

        if line == "---":
            out.append("<hr>")
            index += 1
            continue

        heading = _HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            body = render_inline(heading.group(2))
            out.append(f"<h{level}>{body}</h{level}>")
            index += 1
            continue

        if line.startswith("|"):
            rows: list[list[str]] = []
            while index < total and current().startswith("|"):
                cells = [cell.strip() for cell in current().strip().strip("|").split("|")]
                rows.append(cells)
                index += 1
            data = [row for row in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in row)]
            head, *body = data
            table = ["<div class=\"notes-table-wrap\"><table>", "<thead><tr>"]
            table += [f"<th>{render_inline(c)}</th>" for c in head]
            table.append("</tr></thead><tbody>")
            for row in body:
                table.append("<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in row) + "</tr>")
            table.append("</tbody></table></div>")
            out.append("".join(table))
            continue

        if line.startswith("> "):
            paragraphs: list[list[str]] = [[]]
            while index < total:
                stripped = current()
                if stripped.startswith("> "):
                    paragraphs[-1].append(stripped[2:].strip())
                    index += 1
                elif stripped == "":
                    lookahead = index
                    while lookahead < total and lines[lookahead].strip() == "":
                        lookahead += 1
                    if lookahead < total and lines[lookahead].strip().startswith("> "):
                        paragraphs.append([])
                        index = lookahead
                    else:
                        break
                else:
                    break
            inner = "".join(
                f"<p>{render_inline(' '.join(part))}</p>" for part in paragraphs if part
            )
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        ordered = _ORDERED_RE.match(line)
        if ordered:
            items: list[str] = []
            while index < total:
                match = _ORDERED_RE.match(current())
                if not match:
                    break
                items.append(match.group(2))
                index += 1
            out.append("<ol>" + "".join(f"<li>{render_inline(item)}</li>" for item in items) + "</ol>")
            continue

        if line.startswith("- "):
            items = []
            while index < total and current().startswith("- "):
                items.append(current()[2:].strip())
                index += 1
            out.append("<ul>" + "".join(f"<li>{render_inline(item)}</li>" for item in items) + "</ul>")
            continue

        paragraph = [line]
        index += 1
        while index < total and current() and not _BLOCK_STARTER_RE.match(current()):
            paragraph.append(current())
            index += 1
        out.append("<p>" + render_inline(" ".join(paragraph)) + "</p>")

    return "\n".join(out)


def build_notes_page(markdown: str) -> str:
    """Wrap converted blocks in the shared theme shell."""
    body = convert_blocks(markdown)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="娜蒂娅「两衡之间」纯文字版角色档案">
  <title>娜蒂娅｜两衡之间 · 文字档案</title>
  <link rel="stylesheet" href="theme.css">
</head>
<body>
  <div class="ambient" aria-hidden="true">
    <div class="ambient-glow ambient-glow--one"></div>
    <div class="ambient-glow ambient-glow--two"></div>
    <div class="ambient-snow-drift"><div class="ambient-snow"></div></div>
  </div>
  <header class="topbar">
    <div class="shell topbar-inner">
      <div class="brand">NADIA SADOVA / TEXT ARCHIVE</div>
      <nav aria-label="页面导航">
        <a href="index.html">返回档案</a>
        <a href="docs/nadia_character_player_edition.md">原文 Markdown</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="section notes-section">
      <div class="shell notes-shell">
{body}
      </div>
    </section>
  </main>

  <footer>
    <div class="shell footer-line">
      <span>娜蒂娅「两衡之间」 / ORIGINAL FAN CHARACTER</span>
      <span>文字档案 · 由角色设定文档生成</span>
    </div>
  </footer>
</body>
</html>
"""


def rewrite_links(markdown: str, rewrites: tuple[tuple[str, str], ...]) -> str:
    """Apply in-package link rewrites to the document text."""
    for pattern, replacement in rewrites:
        markdown = markdown.replace(pattern, replacement)
    return markdown


def main() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")

    PACKAGED_DOC.parent.mkdir(parents=True, exist_ok=True)
    PACKAGED_DOC.write_text(rewrite_links(source, MD_REWRITES), encoding="utf-8")
    NOTES_PAGE.write_text(build_notes_page(rewrite_links(source, PAGE_REWRITES)), encoding="utf-8")
    print(f"wrote {NOTES_PAGE.relative_to(REPO_ROOT)}")
    print(f"wrote {PACKAGED_DOC.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
