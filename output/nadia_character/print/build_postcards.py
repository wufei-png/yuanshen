from __future__ import annotations

from functools import lru_cache

from PIL import Image, ImageChops, ImageDraw
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from design_system import (
    ASSETS,
    ICE,
    NIGHT,
    OUTPUT_DIR,
    POSTCARDS,
    TMP_DIR,
    draw_image_contain,
    draw_image_cover,
    draw_text,
    mm,
    register_fonts,
    validate_assets,
)


PAGE_W = mm(156)
PAGE_H = mm(106)
TRIM = mm(3)
SAFE = mm(8)
RAW = TMP_DIR / "nadia_postcards_raw.pdf"
OUT = OUTPUT_DIR / "nadia_postcard_collection_48p.pdf"
CSS_PX = mm(150) / 378
BACK_INSET = TRIM
BACK_W = PAGE_W - BACK_INSET * 2
BACK_H = PAGE_H - BACK_INSET * 2


@lru_cache(maxsize=1)
def front_overlay() -> ImageReader:
    """Smooth HTML-style darkening for legible copy without hiding artwork."""
    width, height = 1560, 1060
    horizontal = Image.new("L", (width, 1))
    horizontal.putdata(
        [
            int(10 + 188 * (1 - x / (width - 1)) ** 1.7)
            for x in range(width)
        ]
    )
    horizontal = horizontal.resize((width, height))
    bottom = Image.new("L", (1, height))
    bottom.putdata(
        [int(132 * (y / (height - 1)) ** 1.65) for y in range(height)]
    )
    bottom = bottom.resize((width, height))
    alpha = ImageChops.screen(horizontal, bottom)
    overlay = Image.new("RGBA", (width, height), (7, 20, 38, 0))
    overlay.putalpha(alpha)
    return ImageReader(overlay)


@lru_cache(maxsize=1)
def back_background() -> ImageReader:
    """Render the rounded, pale HTML postcard face at print resolution."""
    width, height = 1560, 1060
    inset = 30
    inner_w, inner_h = width - inset * 2, height - inset * 2
    light = (244, 247, 251)
    shade = (223, 234, 245)
    gradient = Image.new("RGB", (inner_w, inner_h))
    gradient_draw = ImageDraw.Draw(gradient)
    for y in range(inner_h):
        mix = y / max(1, inner_h - 1)
        color = tuple(round(a + (b - a) * mix) for a, b in zip(light, shade))
        gradient_draw.line((0, y, inner_w, y), fill=color)

    mask = Image.new("L", (inner_w, inner_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, inner_w - 1, inner_h - 1), radius=40, fill=255
    )
    background = Image.new("RGB", (width, height), (7, 20, 38))
    background.paste(gradient, (inset, inset), mask)
    return ImageReader(background)


def tracked_width(text: str, font: str, size: float, tracking: float) -> float:
    return pdfmetrics.stringWidth(text, font, size) + tracking * max(0, len(text) - 1)


def draw_tracked(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    *,
    font: str,
    size: float,
    color: HexColor,
    tracking: float = 0,
    align: str = "left",
) -> None:
    width = tracked_width(text, font, size, tracking)
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    text_object = c.beginText(x, y)
    text_object.setFont(font, size)
    text_object.setFillColor(color)
    text_object.setCharSpace(tracking)
    text_object.textOut(text)
    c.drawText(text_object)


def wrap_balanced(
    text: str,
    font: str,
    size: float,
    tracking: float,
    max_width: float,
) -> list[str]:
    """Approximate CSS text-wrap:balance for short CJK collector-card copy."""
    paragraphs = text.splitlines() or [text]
    output: list[str] = []
    closing = set("，。；：！？、）》】」』”’")
    opening = set("《【「『“‘（(")

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            output.append("")
            continue

        greedy: list[str] = []
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and tracked_width(candidate, font, size, tracking) > max_width:
                greedy.append(current.strip())
                current = char.lstrip()
            else:
                current = candidate
        if current:
            greedy.append(current.strip())
        line_count = len(greedy)
        if line_count <= 1:
            output.extend(greedy)
            continue

        target = tracked_width(paragraph, font, size, tracking) / line_count

        @lru_cache(maxsize=None)
        def solve(start: int, remaining: int) -> tuple[float, tuple[str, ...]]:
            while start < len(paragraph) and paragraph[start].isspace():
                start += 1
            if remaining == 1:
                line = paragraph[start:].strip()
                if not line or tracked_width(line, font, size, tracking) > max_width:
                    return float("inf"), ()
                penalty = (tracked_width(line, font, size, tracking) - target) ** 2
                if line[0] in closing:
                    penalty += max_width**2
                return penalty, (line,)

            best: tuple[float, tuple[str, ...]] = (float("inf"), ())
            max_end = len(paragraph) - (remaining - 1)
            for end in range(start + 1, max_end + 1):
                line = paragraph[start:end].strip()
                if not line:
                    continue
                width = tracked_width(line, font, size, tracking)
                if width > max_width:
                    break
                rest_cost, rest = solve(end, remaining - 1)
                if not rest:
                    continue
                penalty = (width - target) ** 2
                if line[-1] in opening or rest[0][0] in closing:
                    penalty += max_width**2
                if (
                    end < len(paragraph)
                    and paragraph[end - 1].isascii()
                    and paragraph[end].isascii()
                    and paragraph[end - 1].isalnum()
                    and paragraph[end].isalnum()
                ):
                    # Browser line breaking keeps an ASCII word intact. A CJK
                    # character-level optimizer must explicitly protect it.
                    penalty += max_width**2 * 10
                candidate = (penalty + rest_cost, (line,) + rest)
                if candidate[0] < best[0]:
                    best = candidate
            return best

        _, balanced = solve(0, line_count)
        output.extend(list(balanced) if balanced else greedy)
    return output


def draw_front(c: canvas.Canvas, card: dict[str, object]) -> None:
    # Match the established postcards.html front: full-card artwork with a
    # translucent readability gradient. Portrait/diagram cards use contain so
    # their subjects stay complete; landscape scenes use cover at card ratio.
    c.setFillColor(NIGHT)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    image = ASSETS / str(card["image"])
    if card["mode"] in {"contain", "right_contain"}:
        c.setFillColor(HexColor("#102B50"))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        draw_image_contain(c, image, 0, 0, PAGE_W, PAGE_H, padding=mm(2.5))
    else:
        draw_image_cover(c, image, 0, 0, PAGE_W, PAGE_H)

    c.drawImage(
        front_overlay(),
        0,
        0,
        PAGE_W,
        PAGE_H,
        preserveAspectRatio=False,
        mask="auto",
    )

    x = SAFE
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 7.2)
    c.drawString(x, mm(31), f"{int(card['num']):02d} / {card['kicker']}")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 22)
    c.drawString(x, mm(20), str(card["title"]))
    draw_text(
        c,
        str(card["subtitle"]),
        x,
        mm(12),
        mm(90),
        size=8.4,
        leading=12.8,
        color=HexColor("#D7E8F6"),
    )
    c.showPage()


def draw_back(c: canvas.Canvas, card: dict[str, object]) -> None:
    c.drawImage(
        back_background(),
        0,
        0,
        PAGE_W,
        PAGE_H,
        preserveAspectRatio=False,
        mask="auto",
    )
    c.setStrokeColor(HexColor("#7FC9E5"))
    c.setLineWidth(0.75)
    c.roundRect(
        BACK_INSET,
        BACK_INSET,
        BACK_W,
        BACK_H,
        mm(4),
        stroke=1,
        fill=0,
    )

    number = f"{int(card['num']):02d}"
    eyebrow = f"{number} / {card['kicker']}"
    title = str(card["back_title"])
    body = str(card["back_body"])
    title_length = len("".join(title.split()))
    body_length = len("".join(body.split()))
    title_css = max(18, min(25, 27 - max(0, title_length - 5) * 0.38))
    body_css = max(12.5, min(17, 17.5 - max(0, body_length - 24) * 0.105))
    title_size = title_css * CSS_PX
    body_size = body_css * CSS_PX
    eyebrow_size = 9 * CSS_PX
    content_width = 322 * 0.88 * CSS_PX
    title_tracking = title_size * 0.08
    body_tracking = body_size * 0.04
    title_lines = wrap_balanced(
        title, "NadiaSerifBold", title_size, title_tracking, content_width
    )
    body_lines = wrap_balanced(
        body, "NadiaSerifBold", body_size, body_tracking, content_width
    )

    eyebrow_leading = eyebrow_size * 1.4
    title_leading = title_size * 1.28
    body_leading = body_size * 1.72
    gap_after_eyebrow = 11 * CSS_PX
    gap_after_title = 10 * CSS_PX
    block_height = (
        eyebrow_leading
        + gap_after_eyebrow
        + len(title_lines) * title_leading
        + gap_after_title
        + len(body_lines) * body_leading
    )
    block_top = PAGE_H / 2 + block_height / 2
    center_x = PAGE_W / 2

    def baseline(top: float, size: float, leading: float) -> float:
        return top - ((leading - size) / 2 + size * 0.82)

    draw_tracked(
        c,
        eyebrow,
        center_x,
        baseline(block_top, eyebrow_size, eyebrow_leading),
        font="NadiaSans",
        size=eyebrow_size,
        color=HexColor("#4EB7DF"),
        tracking=eyebrow_size * 0.25,
        align="center",
    )
    line_top = block_top - eyebrow_leading - gap_after_eyebrow
    for line in title_lines:
        draw_tracked(
            c,
            line,
            center_x,
            baseline(line_top, title_size, title_leading),
            font="NadiaSerifBold",
            size=title_size,
            color=HexColor("#17375E"),
            tracking=title_tracking,
            align="center",
        )
        line_top -= title_leading
    line_top -= gap_after_title
    for line in body_lines:
        draw_tracked(
            c,
            line,
            center_x,
            baseline(line_top, body_size, body_leading),
            font="NadiaSerifBold",
            size=body_size,
            color=HexColor("#365879"),
            tracking=body_tracking,
            align="center",
        )
        line_top -= body_leading

    muted = HexColor("#8A98AA")
    top_baseline = PAGE_H - BACK_INSET - 21 * CSS_PX
    draw_tracked(
        c,
        "NADIA SADOVA / FIELD RECORD",
        PAGE_W - BACK_INSET - 16 * CSS_PX,
        top_baseline,
        font="NadiaLatin",
        size=8 * CSS_PX,
        color=muted,
        tracking=8 * CSS_PX * 0.13,
        align="right",
    )
    bottom_baseline = BACK_INSET + 15 * CSS_PX
    draw_tracked(
        c,
        number,
        BACK_INSET + 18 * CSS_PX,
        bottom_baseline,
        font="NadiaLatinBold",
        size=10 * CSS_PX,
        color=muted,
    )
    draw_tracked(
        c,
        str(card["tag"]),
        PAGE_W - BACK_INSET - 16 * CSS_PX,
        bottom_baseline,
        font="NadiaSans",
        size=9 * CSS_PX,
        color=HexColor("#4EB7DF"),
        tracking=9 * CSS_PX * 0.10,
        align="right",
    )
    c.showPage()


def add_print_boxes() -> None:
    reader = PdfReader(str(RAW))
    if len(reader.pages) != 48:
        raise ValueError(f"Expected 48 postcard pages, got {len(reader.pages)}")
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    trim_box = RectangleObject((TRIM, TRIM, PAGE_W - TRIM, PAGE_H - TRIM))
    bleed_box = RectangleObject((0, 0, PAGE_W, PAGE_H))
    for page in writer.pages:
        page.trimbox = trim_box
        page.bleedbox = bleed_box
        page.cropbox = bleed_box
    writer.add_metadata(
        {
            "/Title": "娜蒂娅「两衡之间」48页明信片收藏套组",
            "/Author": "Original fan character postcard collection",
            "/Subject": "24 collector postcards, front and back on separate pages",
            "/Keywords": "Nadia Sadova, postcard, collector set, fan character",
        }
    )
    with OUT.open("wb") as stream:
        writer.write(stream)
    RAW.unlink(missing_ok=True)


def main() -> None:
    register_fonts()
    validate_assets(str(card["image"]) for card in POSTCARDS)
    if len(POSTCARDS) != 24:
        raise ValueError(f"Expected 24 postcards, got {len(POSTCARDS)}")
    c = canvas.Canvas(str(RAW), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("娜蒂娅「两衡之间」48页明信片收藏套组")
    c.setAuthor("Original fan character postcard collection")
    for card in POSTCARDS:
        draw_front(c, card)
        draw_back(c, card)
    c.save()
    add_print_boxes()
    print(OUT)


if __name__ == "__main__":
    main()
