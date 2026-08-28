from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A5
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT_DIR = (ROOT.parent / "pdf").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "nadia_character_dossier.pdf"

PAGE_W, PAGE_H = A5
MARGIN = 34
INK = HexColor("#17243A")
MUTED = HexColor("#60708C")
PAPER = HexColor("#F5F7FB")
ICE = HexColor("#8ED7EF")
ICE_STRONG = HexColor("#398DBD")
NAVY = HexColor("#172D4A")
GOLD = HexColor("#C9A96B")
WARM = HexColor("#F4E7D6")

FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
pdfmetrics.registerFont(TTFont("NadiaCJK", FONT_PATH, subfontIndex=0))


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if paragraph == "":
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            trial = current + char
            if current and pdfmetrics.stringWidth(trial, font, size) > max_width:
                lines.append(current)
                current = char
            else:
                current = trial
        if current:
            lines.append(current)
    return lines


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, width: float,
              size: float = 9, leading: float | None = None,
              color=INK, font: str = "NadiaCJK") -> float:
    leading = leading or size * 1.62
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, width):
        if line:
            c.drawString(x, y, line)
        y -= leading
    return y


def draw_centered(c: canvas.Canvas, text: str, x: float, y: float, width: float,
                  size: float, color=INK) -> None:
    c.setFont("NadiaCJK", size)
    c.setFillColor(color)
    c.drawCentredString(x + width / 2, y, text)


def draw_image_cover(c: canvas.Canvas, path: Path, x: float, y: float,
                     width: float, height: float, opacity: float | None = None,
                     anchor: str = "center") -> None:
    image = ImageReader(str(path))
    iw, ih = image.getSize()
    scale = max(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    if anchor == "top":
        dx, dy = x + (width - dw) / 2, y + height - dh
    elif anchor == "bottom":
        dx, dy = x + (width - dw) / 2, y
    else:
        dx, dy = x + (width - dw) / 2, y + (height - dh) / 2
    c.saveState()
    path_obj = c.beginPath()
    path_obj.rect(x, y, width, height)
    c.clipPath(path_obj, stroke=0, fill=0)
    c.drawImage(image, dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    c.restoreState()
    if opacity is not None:
        c.saveState()
        if hasattr(c, "setFillAlpha"):
            c.setFillAlpha(opacity)
        c.setFillColor(NAVY)
        c.rect(x, y, width, height, stroke=0, fill=1)
        c.restoreState()


def footer(c: canvas.Canvas, page_no: int, dark: bool = False) -> None:
    color = HexColor("#DCEBFA") if dark else MUTED
    c.setStrokeColor(color)
    c.setLineWidth(0.45)
    c.line(MARGIN, 25, PAGE_W - MARGIN, 25)
    c.setFont("NadiaCJK", 6.5)
    c.setFillColor(color)
    c.drawString(MARGIN, 13, "娜蒂娅「两衡之间」 / ORIGINAL FAN CHARACTER DOSSIER")
    c.drawRightString(PAGE_W - MARGIN, 13, f"{page_no:02d}")


def section_title(c: canvas.Canvas, index: str, title: str, subtitle: str = "") -> float:
    y = PAGE_H - 52
    c.setFont("NadiaCJK", 7.5)
    c.setFillColor(ICE_STRONG)
    c.drawString(MARGIN, y, index.upper())
    c.setFont("NadiaCJK", 24)
    c.setFillColor(INK)
    c.drawString(MARGIN, y - 32, title)
    if subtitle:
        draw_text(c, subtitle, MARGIN, y - 55, PAGE_W - MARGIN * 2, 8.5, 13, MUTED)
        return y - 84
    return y - 64


def card(c: canvas.Canvas, x: float, y: float, width: float, height: float,
         fill=PAPER, stroke=HexColor("#D8E2F0"), radius: float = 12) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.6)
    c.roundRect(x, y, width, height, radius, stroke=1, fill=1)


def swatch(c: canvas.Canvas, x: float, y: float, color, label: str, label_color=MUTED) -> None:
    c.setFillColor(color)
    c.roundRect(x, y, 22, 12, 3, stroke=0, fill=1)
    c.setFont("NadiaCJK", 6.5)
    c.setFillColor(label_color)
    c.drawString(x + 28, y + 2, label)


def meter(c: canvas.Canvas, x: float, y: float, width: float) -> None:
    gap = 6
    cell_w = (width - gap * 4) / 5
    values = ["-2", "-1", "0", "+1", "+2"]
    for i, value in enumerate(values):
        fill = ICE_STRONG if value == "0" else HexColor("#DCEAF5")
        c.setFillColor(fill)
        c.setStrokeColor(HexColor("#B8CDE0"))
        c.roundRect(x + i * (cell_w + gap), y, cell_w, 18, 5, stroke=1, fill=1)
        c.setFont("NadiaCJK", 7)
        c.setFillColor(white if value == "0" else MUTED)
        c.drawCentredString(x + i * (cell_w + gap) + cell_w / 2, y + 5, value)
    c.setFont("NadiaCJK", 7)
    c.setFillColor(MUTED)
    c.drawString(x, y - 14, "轻端 / 普莎")
    c.drawRightString(x + width, y - 14, "伊嘉 / 重端")


def page_cover(c: canvas.Canvas) -> None:
    draw_image_cover(c, ASSETS / "nadia_splash.png", 0, 0, PAGE_W, PAGE_H, anchor="center")
    c.saveState()
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(.72)
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, 205, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 7.5)
    c.drawString(MARGIN, 171, "SNEZHNAYA / CRYO / CATALYST / ★★★★★")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 42)
    c.drawString(MARGIN, 122, "娜蒂娅")
    c.setFont("NadiaCJK", 18)
    c.drawString(MARGIN, 93, "「两衡之间」")
    c.setFont("NadiaCJK", 8)
    c.setFillColor(HexColor("#DCEBFA"))
    c.drawString(MARGIN, 55, "NADIA SADOVA / CHARACTER DOSSIER")
    c.drawString(MARGIN, 40, "原创同人角色设定 · 阅读版")
    c.showPage()


def page_profile(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "01 / PROFILE", "她先记录，再下结论", "一个温柔知性的至冬民间异常现象记录员。")
    quote = "外观看起来很重的东西，未必真的沉；看起来轻盈的东西，也未必能够被轻易抱起。至于人……我暂时还没有找到合适的称量方法。"
    card(c, MARGIN, y - 102, PAGE_W - MARGIN * 2, 94, fill=white)
    draw_text(c, quote, MARGIN + 18, y - 35, PAGE_W - MARGIN * 2 - 36, 10.5, 17, NAVY)
    y -= 128
    left_w = 158
    right_x = MARGIN + left_w + 18
    card(c, MARGIN, y - 205, left_w, 195, fill=white)
    c.setFont("NadiaCJK", 13)
    c.setFillColor(INK)
    c.drawString(MARGIN + 15, y - 31, "角色档案")
    rows = [
        ("姓名", "娜蒂娅·萨多娃"),
        ("地区", "至冬"),
        ("元素", "冰 / Cryo"),
        ("武器", "法器"),
        ("命之座", "双衡仪座"),
        ("身份", "民间记录员"),
    ]
    ry = y - 55
    for label, value in rows:
        c.setFont("NadiaCJK", 7.5)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 15, ry, label)
        c.setFillColor(INK)
        c.drawRightString(MARGIN + left_w - 15, ry, value)
        ry -= 22
    card(c, right_x, y - 205, PAGE_W - MARGIN - right_x, 195, fill=WARM, stroke=HexColor("#E2CFB2"))
    c.setFont("NadiaCJK", 13)
    c.setFillColor(INK)
    c.drawString(right_x + 15, y - 31, "她的工作方式")
    draw_text(c, "面对最违反常识的事情，她的第一反应通常不是惊叫，而是把眼镜推回去，再测一次。\n\n她会在正式报告里写“同行个体 A”和“同行个体 B”，在私人笔记里却写下普莎与伊嘉的名字。\n\n她一直以为自己只是观察者，直到第三条曲线也出现在记录里。", right_x + 15, y - 57, PAGE_W - MARGIN - right_x - 30, 8.3, 13, INK)
    footer(c, page_no)
    c.showPage()


def page_concept(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "02 / CONCEPT", "第三个对象", "她的故事不是让一切恢复原样，而是学习如何让变化继续稳定地存在。")
    card(c, MARGIN, y - 145, PAGE_W - MARGIN * 2, 137, fill=NAVY, stroke=NAVY)
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 18, y - 31, "ONE-LINE CONCEPT")
    draw_text(c, "一位带着两只异常家猫旅行的至冬记录员，最终发现自己才是维持两种相反锚定状态的第三个锚点。", MARGIN + 18, y - 59, PAGE_W - MARGIN * 2 - 36, 14, 22, white)
    y -= 176
    col_w = (PAGE_W - MARGIN * 2 - 16) / 2
    card(c, MARGIN, y - 218, col_w, 210, fill=PAPER)
    card(c, MARGIN + col_w + 16, y - 218, col_w, 210, fill=PAPER)
    c.setFillColor(ICE_STRONG)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 16, y - 32, "PERSONALITY")
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 17)
    c.drawString(MARGIN + 16, y - 61, "温柔知性")
    draw_text(c, "专业可靠，偶尔天然呆。她不轻易下结论，不知道的事情会直接说“这个我还没有证据”。\n\n对两只猫，她的专业性会明显松动：一边测量，一边给猫梳毛；一边写报告，一边担心普莎会被风带走。", MARGIN + 16, y - 88, col_w - 32, 8.5, 14, MUTED)
    c.setFillColor(ICE_STRONG)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + col_w + 32, y - 32, "THE THIRD ANCHOR")
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 17)
    c.drawString(MARGIN + col_w + 32, y - 61, "三体，而非双体")
    draw_text(c, "旧记录一直把研究对象写成两只猫。多年以后，娜蒂娅才发现第三条曲线来自自己。她不是旁观者，也不是世界中心，只是三个生命之间负责稳定关系的人。", MARGIN + col_w + 32, y - 88, col_w - 32, 8.5, 14, MUTED)
    footer(c, page_no)
    c.showPage()


def page_visual(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "03 / VISUAL LANGUAGE", "把她画成角色", "人物照片只提供灵感。最终呈现采用清晰线稿、赛璐璐分色和成人二次元比例。")
    image_x = MARGIN + 202
    draw_image_cover(c, ASSETS / "nadia_splash.png", image_x, 128, PAGE_W - MARGIN - image_x, y - 118, anchor="top")
    c.setFillColor(NAVY)
    c.rect(MARGIN, 84, 188, y - 84, stroke=0, fill=1)
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 16, y - 34, "DESIGN ANCHORS")
    draw_text(c, "圆形略偏椭圆的细金属框\n\n过肩深色轻波浪\n\n奶白高领与深灰蓝外层\n\n左腰后三层测量环\n\n一只向上，一只向下\n\n温柔但不幼态", MARGIN + 16, y - 61, 155, 9.3, 17, white)
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 16, 165, "PALETTE")
    swatch(c, MARGIN + 16, 143, HexColor("#172D4A"), "深海军蓝", HexColor("#DCEBFA"))
    swatch(c, MARGIN + 16, 121, HexColor("#8ED7EF"), "冰蓝光", HexColor("#DCEBFA"))
    swatch(c, MARGIN + 16, 99, HexColor("#F4E7D6"), "暖纸色", HexColor("#DCEBFA"))
    footer(c, page_no)
    c.showPage()


def page_cats(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "04 / COMPANIONS", "不要用外观判断重量", "它们是真实的家猫，不是使魔，也不是元素生命。")
    gap = 16
    card_w = (PAGE_W - MARGIN * 2 - gap) / 2
    for i, (name, en, label, body, fill, accent) in enumerate([
        ("普莎", "PUSHA", "轻相 / LIGHT PHASE", "圆润、奶油金、琥珀眼。看起来像一团很有分量的绒毛，实际上可能被风慢慢带走。长命锁和安全牵引绳首先是为了防止它飘离地面。", HexColor("#F7F0E7"), ICE_STRONG),
        ("伊嘉", "IGLA", "重相 / HEAVY PHASE", "修长、象牙色、冰蓝眼。走路依旧轻巧，却会让薄冰细裂、木板下陷。它已经完全适应自己的状态，只有第一次抱起它的人还没有。", HexColor("#E9EEF7"), NAVY),
    ]):
        x = MARGIN + i * (card_w + gap)
        card(c, x, y - 286, card_w, 278, fill=fill, stroke=HexColor("#D8E2F0"))
        c.setFillColor(accent)
        c.setFont("NadiaCJK", 7.5)
        c.drawString(x + 16, y - 32, label)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 24)
        c.drawString(x + 16, y - 67, name)
        c.setFont("NadiaCJK", 8)
        c.setFillColor(MUTED)
        c.drawString(x + 16, y - 84, en)
        c.setFillColor(accent)
        c.circle(x + card_w - 42, y - 63, 20, stroke=0, fill=1)
        c.setFillColor(white)
        c.circle(x + card_w - 50, y - 60, 4, stroke=0, fill=1)
        c.circle(x + card_w - 34, y - 60, 4, stroke=0, fill=1)
        draw_text(c, body, x + 16, y - 119, card_w - 32, 8.7, 14, INK)
        c.setStrokeColor(accent)
        c.setLineWidth(1)
        c.line(x + 16, y - 245, x + card_w - 16, y - 245)
        c.setFont("NadiaCJK", 7.5)
        c.setFillColor(accent)
        c.drawString(x + 16, y - 264, "真实家猫 / 异常锚定")
    footer(c, page_no)
    c.showPage()


def page_mechanic(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "05 / MECHANIC", "衡标", "她不把失衡当成错误，而是把它记录成一种可控的路径。")
    card(c, MARGIN, y - 100, PAGE_W - MARGIN * 2, 92, fill=white)
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 12)
    c.drawString(MARGIN + 16, y - 31, "五格状态")
    draw_text(c, "战技启动时，衡标从 0 开始。风与冰将它推向轻端，冰与雷将它推向重端；从任一端点返回中央时，触发归衡。", MARGIN + 16, y - 54, PAGE_W - MARGIN * 2 - 32, 8.6, 14, MUTED)
    meter(c, MARGIN + 22, y - 148, PAGE_W - MARGIN * 2 - 44)
    y -= 192
    col_w = (PAGE_W - MARGIN * 2 - 16) / 2
    for i, (title, body, fill, accent) in enumerate([
        ("向轻端", "Stellar Swirl 触发普莎响应：牵引、浮动、多目标控制。到达 -2 后进入轻端观测。", HexColor("#EDF8FC"), ICE_STRONG),
        ("向重端", "Stellar-Conduct 触发伊嘉响应：压制、迟滞、单目标稳定控制。到达 +2 后进入重端观测。", HexColor("#E9EEF7"), NAVY),
    ]):
        x = MARGIN + i * (col_w + 16)
        card(c, x, y - 150, col_w, 142, fill=fill)
        c.setFillColor(accent)
        c.setFont("NadiaCJK", 12)
        c.drawString(x + 16, y - 32, title)
        draw_text(c, body, x + 16, y - 58, col_w - 32, 8.5, 14, MUTED)
    card(c, MARGIN, 38, PAGE_W - MARGIN * 2, 72, fill=WARM, stroke=HexColor("#E2CFB2"))
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 10)
    c.drawString(MARGIN + 16, 82, "普通玩家与高阶玩家")
    draw_text(c, "普通玩家使用战技即可获得两只猫的基础协同；高阶玩家才需要主动把系统推向一端，再把它带回归衡。没有风或雷反应时，基础协同仍然存在。", MARGIN + 16, 60, PAGE_W - MARGIN * 2 - 32, 8.1, 12, INK)
    footer(c, page_no)
    c.showPage()


def page_skills(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "06 / ABILITIES", "两种响应，一次归衡", "技能描述保留玩家需要理解的体验，不写未经测试的倍率。")
    items = [
        ("E", "双相巡衡", "打开记录册，两只猫进入巡衡。技能本身提供低频基础冰元素协同；反应触发后，普莎或伊嘉响应。"),
        ("Q", "三体归零·雪原校准", "三点锁成冰蓝色测量结构，建立零点测区。轻中有重，重中有轻，战场短暂回到可控状态。"),
        ("A", "霜度测录", "四段远程冰元素攻击。动作像标点、记录、校正、结论，而不是挥舞一件巨大的法器。"),
        ("P", "误差本身也是记录", "从轻端或重端返回中央时，归衡响应得到强化。真正的高阶玩法不是永远停在某一边。"),
    ]
    box_h = 104
    for i, (key, title, body) in enumerate(items):
        row = i // 2
        col = i % 2
        x = MARGIN + col * ((PAGE_W - MARGIN * 2 - 16) / 2 + 16)
        top = y - row * (box_h + 14)
        w = (PAGE_W - MARGIN * 2 - 16) / 2
        card(c, x, top - box_h, w, box_h, fill=PAPER)
        c.setFillColor(ICE_STRONG)
        c.setFont("NadiaCJK", 15)
        c.drawString(x + 16, top - 29, key)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 12)
        c.drawString(x + 45, top - 28, title)
        draw_text(c, body, x + 16, top - 54, w - 32, 8.1, 13, MUTED)
    card(c, MARGIN, 90, PAGE_W - MARGIN * 2, 105, fill=NAVY, stroke=NAVY)
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 16, 167, "COMBAT PROMISE")
    draw_text(c, "通过 Stellar 反应改变战场控制方式，再把失衡带回可控状态。", MARGIN + 16, 141, PAGE_W - MARGIN * 2 - 32, 12, 19, white)
    footer(c, page_no)
    c.showPage()


def page_burst(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    draw_image_cover(c, ASSETS / "nadia_splash.png", PAGE_W - 218, 0, 218, PAGE_H, opacity=.62, anchor="center")
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN, PAGE_H - 53, "07 / ZERO-POINT CALIBRATION")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 26)
    c.drawString(MARGIN, PAGE_H - 97, "三体归零")
    c.setFont("NadiaCJK", 13)
    c.drawString(MARGIN, PAGE_H - 123, "雪原校准")
    draw_text(c, "普莎落在左侧测量盘，测量盘上升。\n伊嘉落在右侧，整个右侧下沉。\n指针左右摆动，直到画面中出现第三个点。", MARGIN, PAGE_H - 181, 190, 9.5, 16, HexColor("#DCEBFA"))
    c.setStrokeColor(ICE)
    c.setLineWidth(1)
    c.circle(MARGIN + 78, PAGE_H - 310, 55, stroke=1, fill=0)
    c.circle(MARGIN + 78, PAGE_H - 310, 26, stroke=1, fill=0)
    c.line(MARGIN + 78, PAGE_H - 365, MARGIN + 78, PAGE_H - 255)
    c.line(MARGIN + 23, PAGE_H - 310, MARGIN + 133, PAGE_H - 310)
    c.setFillColor(ICE)
    c.circle(MARGIN + 78, PAGE_H - 310, 4, stroke=0, fill=1)
    c.setFont("NadiaCJK", 9)
    c.setFillColor(white)
    c.drawString(MARGIN, PAGE_H - 410, "误差确认。重新归零。")
    draw_text(c, "零点测区不是全屏核爆。它的重点是两个完全不符合体型的质量现象，与她在中央保持绝对冷静。爆发结束时，数值仍然没有完全守恒。", MARGIN, PAGE_H - 454, 190, 8.5, 14, HexColor("#DCEBFA"))
    footer(c, page_no, dark=True)
    c.showPage()


def page_story(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "08 / STORY", "第三条曲线", "她过去一直把自己记作观察者，把两只猫记作两个样本。")
    draw_image_cover(c, ASSETS / "nadia_daily.png", MARGIN, y - 159, PAGE_W - MARGIN * 2, 151, anchor="center")
    y -= 184
    draw_text(c, "事故后的许多年里，两只猫适应了现在的生活。普莎学会慢慢落下，伊嘉找到了不会被它压坏的落脚处。娜蒂娅也逐渐停止使用“恢复”这个词，改用“稳定”。\n\n直到异常重新开始变化，旧记录才暴露出一个被遗漏的对象。她把“双体异常长期观测记录”改成“三体异常长期观测记录”。", MARGIN, y, PAGE_W - MARGIN * 2, 8.8, 14, INK)
    card(c, MARGIN, 88, PAGE_W - MARGIN * 2, 100, fill=WARM, stroke=HexColor("#E2CFB2"))
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 14)
    c.drawString(MARGIN + 16, 159, "此前样本数量统计错误。")
    draw_text(c, "不是崩溃，也不是突然怀疑人生。这就是她。", MARGIN + 16, 132, PAGE_W - MARGIN * 2 - 32, 8.8, 14, MUTED)
    footer(c, page_no)
    c.showPage()


def page_quest(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "09 / QUEST", "比雪更轻，比承诺更重", "双衡之章·第一幕 / 猫、砝码与第三个数字")
    stages = [
        ("01", "屋顶上的猫", "一只猫被暴风送上屋顶，另一只猫让旧木板发出危险的呻吟。看似轻松的委托，开始变得不再轻松。"),
        ("02", "重新运行的设施", "旧观测设施启动，过去被拆散的记录重新指向两只猫和一个被遗漏的第三对象。"),
        ("03", "拒绝强制复原", "系统试图把三者校准成事故以前的样子。娜蒂娅必须回答：复原究竟是为了它们，还是为了让自己安心？"),
        ("04", "继续测量", "她选择稳定现在的三者。她没有得到治好它们的答案，却找到了继续和它们一起生活的方法。"),
    ]
    line_x = MARGIN + 22
    c.setStrokeColor(HexColor("#C6D7E9"))
    c.setLineWidth(1)
    c.line(line_x, y - 25, line_x, 116)
    for i, (num, title, body) in enumerate(stages):
        top = y - 14 - i * 92
        c.setFillColor(ICE_STRONG if i < 3 else GOLD)
        c.circle(line_x, top, 15, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("NadiaCJK", 7)
        c.drawCentredString(line_x, top - 3, num)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 12)
        c.drawString(MARGIN + 52, top + 4, title)
        draw_text(c, body, MARGIN + 52, top - 19, PAGE_W - MARGIN - 64, 8.1, 13, MUTED)
    card(c, MARGIN, 64, PAGE_W - MARGIN * 2, 45, fill=NAVY, stroke=NAVY)
    draw_centered(c, "继续测量。还有……继续养。", MARGIN, 81, PAGE_W - MARGIN * 2, 11, white)
    footer(c, page_no)
    c.showPage()


def page_daily(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "10 / DAILY LIFE", "严谨记录之外", "她仍然会被猫毛、风和一只太重的猫打断。")
    quotes = [
        "“这个我还没有证据。”",
        "“异常并不等于错误。很多时候，它只是我们还没有找到正确的解释。”",
        "“以前我一直觉得自己只是观察者。后来发现，第三条曲线原来是我的。”",
    ]
    for i, q in enumerate(quotes):
        top = y - i * 87
        card(c, MARGIN, top - 68, PAGE_W - MARGIN * 2, 61, fill=white, stroke=HexColor("#D8E2F0"))
        c.setFillColor(GOLD)
        c.rect(MARGIN, top - 68, 3, 61, stroke=0, fill=1)
        draw_text(c, q, MARGIN + 17, top - 35, PAGE_W - MARGIN * 2 - 34, 9, 14, INK)
    card(c, MARGIN, 92, PAGE_W - MARGIN * 2, 102, fill=WARM, stroke=HexColor("#E2CFB2"))
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 12)
    c.drawString(MARGIN + 16, 166, "待机片段")
    draw_text(c, "普莎被风慢慢带离地面，她一边看笔记，一边抓住安全带把它拉回来。\n\n伊嘉走到脚边。她准备单手抱起，停顿后改成双手，并在本子上写：“今天也是稳定状态。”", MARGIN + 16, 141, PAGE_W - MARGIN * 2 - 32, 8.3, 13, INK)
    footer(c, page_no)
    c.showPage()


def page_constellations(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "11 / CONSTELLATION", "双衡仪座", "命之座把“管理天平”逐步推向“让两端不断碰撞”。")
    names = [
        ("一", "第一条：不要相信眼睛", "更快进入轻端或重端观测。"),
        ("二", "第二条：重新称量", "强化轻相牵引与重相压制。"),
        ("三", "第三条：记录直到一致", "元素战技等级提高。"),
        ("四", "第四条：误差从不是零", "归衡后打开短暂 Stellar 反应强化窗口。"),
        ("五", "第五条：零点只是起点", "元素爆发等级提高。"),
        ("六", "最后一条：我们三个都在这里", "零点测区期间，两只猫都以完整协同响应。"),
    ]
    for i, (n, title, body) in enumerate(names):
        row = i // 2
        col = i % 2
        x = MARGIN + col * ((PAGE_W - MARGIN * 2 - 16) / 2 + 16)
        top = y - row * 86
        w = (PAGE_W - MARGIN * 2 - 16) / 2
        card(c, x, top - 72, w, 66, fill=PAPER)
        c.setFillColor(ICE_STRONG if i < 5 else GOLD)
        c.setFont("NadiaCJK", 15)
        c.drawString(x + 13, top - 29, n)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 8.5)
        c.drawString(x + 40, top - 26, title)
        draw_text(c, body, x + 40, top - 47, w - 53, 7.1, 11, MUTED)
    card(c, MARGIN, 89, PAGE_W - MARGIN * 2, 84, fill=NAVY, stroke=NAVY)
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 16, 145, "THE EMOTIONAL CONCLUSION")
    draw_text(c, "第六命的名字不是口号，而是剧情结论：她们三个都在这里。", MARGIN + 16, 119, PAGE_W - MARGIN * 2 - 32, 10.5, 16, white)
    footer(c, page_no)
    c.showPage()


def page_weapon(c: canvas.Canvas, page_no: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    y = section_title(c, "12 / OBJECTS", "零点之外", "一本会自行翻页的野外调查记录册，与两组悬浮测量环组成的组合式法器。")
    card(c, MARGIN, y - 125, PAGE_W - MARGIN * 2, 117, fill=white)
    c.setFillColor(GOLD)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN + 16, y - 31, "FIVE-STAR CATALYST")
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 18)
    c.drawString(MARGIN + 16, y - 61, "零点不是答案")
    draw_text(c, "书页灰白，边缘有冰蓝元素纹。攻击时，环展开，页面自行翻动，刻度在空气中形成冰晶坐标。她更像在校准装置，而不是挥舞武器。", MARGIN + 16, y - 89, PAGE_W - MARGIN * 2 - 32, 8.4, 13, MUTED)
    y -= 154
    col_w = (PAGE_W - MARGIN * 2 - 16) / 2
    card(c, MARGIN, y - 158, col_w, 150, fill=WARM, stroke=HexColor("#E2CFB2"))
    card(c, MARGIN + col_w + 16, y - 158, col_w, 150, fill=white)
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 12)
    c.drawString(MARGIN + 16, y - 34, "角色料理")
    draw_text(c, "两端之间\n\n圆形和细长的小点心，外观与实际的蓬松度、重量恰好相反。\n\n“有些事情只靠看，是永远猜不准的。”", MARGIN + 16, y - 61, col_w - 32, 8.2, 13, INK)
    c.drawString(MARGIN + col_w + 32, y - 34, "玩家印象曲线")
    draw_text(c, "第一次看到：一个戴圆框眼镜、带两只猫的至冬记录员。\n\n玩一段时间：原来技能真的在算轻重状态。\n\n做完传说任务：她研究的从来不只是猫。", MARGIN + col_w + 32, y - 61, col_w - 32, 8.2, 13, MUTED)
    card(c, MARGIN, 72, PAGE_W - MARGIN * 2, 58, fill=NAVY, stroke=NAVY)
    draw_text(c, "零点不是答案，只是决定从哪里开始记录。", MARGIN + 16, 98, PAGE_W - MARGIN * 2 - 32, 10, 16, white)
    footer(c, page_no)
    c.showPage()


def page_end(c: canvas.Canvas, page_no: int) -> None:
    draw_image_cover(c, ASSETS / "nadia_daily.png", 0, 0, PAGE_W, PAGE_H, anchor="center")
    c.saveState()
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(.72)
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, 215, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 8)
    c.drawString(MARGIN, 176, "13 / LAST RECORD")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 19)
    c.drawString(MARGIN, 133, "她没有把一切变回过去。")
    draw_text(c, "她想弄明白，怎样才能让已经改变的一切继续稳定地走向未来。", MARGIN, 99, PAGE_W - MARGIN * 2, 11, 18, white)
    c.setFont("NadiaCJK", 7.5)
    c.setFillColor(HexColor("#DCEBFA"))
    c.drawString(MARGIN, 49, "原创同人角色档案 / 7.0 语境基线 / 非官方资料")
    c.drawString(MARGIN, 35, "NADIA SADOVA / THE THIRD ANCHOR")
    footer(c, page_no, dark=True)
    c.showPage()


def main() -> None:
    c = canvas.Canvas(str(OUT), pagesize=A5, pageCompression=1)
    c.setTitle("娜蒂娅「两衡之间」角色档案")
    c.setAuthor("Original fan character dossier")
    page_cover(c)
    page_profile(c, 2)
    page_concept(c, 3)
    page_visual(c, 4)
    page_cats(c, 5)
    page_mechanic(c, 6)
    page_skills(c, 7)
    page_burst(c, 8)
    page_story(c, 9)
    page_quest(c, 10)
    page_daily(c, 11)
    page_constellations(c, 12)
    page_weapon(c, 13)
    page_end(c, 14)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
