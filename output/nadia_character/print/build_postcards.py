from __future__ import annotations

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

from design_system import (
    ASSETS,
    GOLD,
    ICE,
    ICE_STRONG,
    INK,
    LINE,
    MUTED,
    NAVY,
    NIGHT,
    OUTPUT_DIR,
    PAPER,
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


def draw_front(c: canvas.Canvas, card: dict[str, object]) -> None:
    c.setFillColor(NIGHT)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    image = ASSETS / str(card["image"])
    if card["mode"] in {"contain", "right_contain"}:
        c.setFillColor(HexColor("#102B50"))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setStrokeColor(HexColor("#3A6B96"))
        c.setLineWidth(0.55)
        for radius in (mm(18), mm(29), mm(40)):
            c.circle(PAGE_W * 0.68, PAGE_H * 0.52, radius, stroke=1, fill=0)
        if card["mode"] == "right_contain":
            draw_image_contain(
                c,
                image,
                mm(78),
                mm(8),
                PAGE_W - mm(82),
                PAGE_H - mm(16),
            )
        else:
            draw_image_contain(c, image, 0, 0, PAGE_W, PAGE_H, padding=mm(2.5))
    else:
        draw_image_cover(c, image, 0, 0, PAGE_W, PAGE_H)

    c.saveState()
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(0.78)
    c.setFillColor(NIGHT)
    c.rect(0, 0, mm(77), PAGE_H, stroke=0, fill=1)
    c.restoreState()

    x = SAFE
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 7.2)
    c.drawString(x, PAGE_H - SAFE - mm(2), f"{int(card['num']):02d} / {card['kicker']}")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 22)
    c.drawString(x, PAGE_H - SAFE - mm(14), str(card["title"]))
    draw_text(
        c,
        str(card["subtitle"]),
        x,
        PAGE_H - SAFE - mm(25),
        mm(57),
        size=8.4,
        leading=12.8,
        color=HexColor("#D7E8F6"),
    )
    c.setFillColor(GOLD)
    c.setFont("NadiaCJK", 6.8)
    c.drawString(x, SAFE, "NADIA SADOVA / FIELD RECORD")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 6.8)
    c.drawRightString(PAGE_W - SAFE, SAFE, str(card["group"]))
    c.showPage()


def draw_back(c: canvas.Canvas, card: dict[str, object]) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(HexColor("#DDEAF5"))
    c.rect(0, 0, mm(5), PAGE_H, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#B9D1E4"))
    c.setLineWidth(0.55)
    for radius in (mm(14), mm(24), mm(34)):
        c.circle(PAGE_W - mm(19), PAGE_H / 2, radius, stroke=1, fill=0)

    x = SAFE
    width = PAGE_W - SAFE * 2
    c.setFillColor(ICE_STRONG)
    c.setFont("NadiaCJK", 7.4)
    c.drawString(x, PAGE_H - SAFE - mm(1), f"{int(card['num']):02d} / {card['kicker']}")
    c.setFillColor(INK)
    title = str(card["back_title"])
    title_size = 19 if len(title) <= 11 else 16.5
    c.setFont("NadiaCJK", title_size)
    c.drawString(x, PAGE_H - SAFE - mm(14), title)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    c.line(x, PAGE_H - SAFE - mm(19), x + mm(23), PAGE_H - SAFE - mm(19))
    body = str(card["back_body"])
    body_size = 10.4 if len(body.replace("\n", "")) < 62 else 9.6
    draw_text(
        c,
        body,
        x,
        PAGE_H - SAFE - mm(27),
        mm(105),
        size=body_size,
        leading=body_size * 1.65,
        color=HexColor("#355574"),
    )
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(x, SAFE + mm(4), PAGE_W - SAFE, SAFE + mm(4))
    c.setFillColor(MUTED)
    c.setFont("NadiaCJK", 6.8)
    c.drawString(x, SAFE, "NADIA SADOVA / COLLECTOR POSTCARD")
    c.setFillColor(ICE_STRONG)
    c.drawRightString(PAGE_W - SAFE, SAFE, str(card["tag"]))
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
