from __future__ import annotations

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

from design_system import (
    ASSETS,
    GOLD,
    ICE,
    ICE_STRONG,
    INK,
    MUTED,
    NAVY,
    NIGHT,
    OUTPUT_DIR,
    PAPER,
    WARM,
    draw_card,
    draw_footer,
    draw_image_contain,
    draw_image_cover,
    draw_section_header,
    draw_text,
    register_fonts,
    validate_assets,
)


OUT = OUTPUT_DIR / "nadia_character_dossier.pdf"
PAGE_W, PAGE_H = A5
MARGIN = 34


REQUIRED_ASSETS = [
    "nadia_splash_v4_canonical_refined.png",
    "nadia_character_v3_canonical.png",
    "nadia_companions_v3_canonical_ingame.png",
    "nadia_quest_v2_canonical_refined.png",
    "nadia_pusha_v1_ingame.png",
    "nadia_igla_v1_ingame.png",
    "nadia_story_after_v1_ingame.png",
    "nadia_balance_v1_ingame.png",
    "nadia_h_light_v1_ingame.png",
    "nadia_h_heavy_v1_ingame.png",
    "nadia_h_zero_v1_ingame.png",
    "nadia_action_v2_ingame.png",
    "nadia_measurement_ring_v2_ingame.png",
    "nadia_catalyst_v2_ingame.png",
    "nadia_field_notebook_v1_ingame.png",
    "nadia_dish_v1_ingame.png",
]


def start_page(c: canvas.Canvas, *, dark: bool = False) -> None:
    c.setFillColor(NIGHT if dark else PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)


def finish_page(c: canvas.Canvas, page_no: int, title: str, *, dark: bool = False) -> None:
    key = f"page-{page_no}"
    c.bookmarkPage(key)
    c.addOutlineEntry(f"{page_no:02d} {title}", key, level=0, closed=False)
    if page_no > 1:
        draw_footer(c, PAGE_W, page_no, dark=dark, margin=MARGIN)
    c.showPage()


def label(c: canvas.Canvas, text: str, x: float, y: float, *, dark: bool = False) -> None:
    c.setFillColor(ICE if dark else ICE_STRONG)
    c.setFont("NadiaCJK", 7.2)
    c.drawString(x, y, text)


def page_cover(c: canvas.Canvas) -> None:
    draw_image_cover(c, ASSETS / "nadia_splash_v4_canonical_refined.png", 0, 0, PAGE_W, PAGE_H, anchor="top")
    c.saveState()
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(0.88)
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, 198, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 7.5)
    c.drawString(MARGIN, 167, "至冬 / 冰 / 法器 / 五星")
    c.setFillColor(white)
    c.setFont("NadiaCJK", 39)
    c.drawString(MARGIN, 119, "娜蒂娅")
    c.setFont("NadiaCJK", 18)
    c.drawString(MARGIN, 89, "「两衡之间」")
    c.setFillColor(HexColor("#DCEBFA"))
    c.setFont("NadiaCJK", 7.5)
    c.drawString(MARGIN, 51, "NADIA SADOVA / CHARACTER DOSSIER")
    c.drawString(MARGIN, 35, "原创同人角色 · 玩家档案 · 2026")
    finish_page(c, 1, "封面", dark=True)


def page_profile(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "01 / PROFILE", "她先记录，再下结论", "温柔知性的至冬民间异常现象记录员。")
    draw_card(c, MARGIN, y - 93, PAGE_W - MARGIN * 2, 84)
    draw_text(c, "“外观看起来很重的东西，未必真的沉；看起来轻盈的东西，也未必能够被轻易抱起。至于人……我还没有找到合适的称量方法。”", MARGIN + 17, y - 31, PAGE_W - MARGIN * 2 - 34, size=9.6, leading=15.5, color=NAVY)
    y -= 119
    gap = 16
    col_w = (PAGE_W - MARGIN * 2 - gap) / 2
    draw_card(c, MARGIN, 111, col_w, y - 121)
    draw_card(c, MARGIN + col_w + gap, 111, col_w, y - 121, fill=WARM, stroke=HexColor("#E2CFB2"))
    label(c, "CHARACTER RECORD", MARGIN + 15, y - 28)
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 14)
    c.drawString(MARGIN + 15, y - 52, "角色档案")
    rows = [("姓名", "娜蒂娅·萨多娃"), ("地区", "至冬"), ("元素", "冰 / Stellar Linchpin"), ("武器", "法器"), ("身份", "民间异常记录员"), ("命之座", "双衡仪座")]
    ry = y - 80
    for key, value in rows:
        c.setFont("NadiaCJK", 7.2)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 15, ry, key)
        c.setFillColor(INK)
        c.drawRightString(MARGIN + col_w - 15, ry, value)
        ry -= 23
    label(c, "FIRST IMPRESSION", MARGIN + col_w + gap + 15, y - 28)
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 14)
    c.drawString(MARGIN + col_w + gap + 15, y - 52, "工作方式")
    draw_text(c, "面对异常，她会把眼镜推回去，再测一次。\n\n她不轻易下结论。没有证据时，会直接说不知道。\n\n她一直以为自己只是观察者，直到第三条曲线出现在记录里。", MARGIN + col_w + gap + 15, y - 79, col_w - 30, size=8.1, leading=13.1, color=INK)
    finish_page(c, 2, "角色档案")


def page_concept(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "02 / CONCEPT", "三体，而非双体", "她的故事不是恢复原样，而是让变化继续稳定地存在。")
    draw_card(c, MARGIN, y - 113, PAGE_W - MARGIN * 2, 104, fill=NAVY, stroke=NAVY)
    label(c, "ONE-LINE CONCEPT", MARGIN + 17, y - 31, dark=True)
    draw_text(c, "一位带着两只异常家猫旅行的至冬记录员，最终发现自己才是维持两种相反锚定状态的第三个锚点。", MARGIN + 17, y - 61, PAGE_W - MARGIN * 2 - 34, size=12.3, leading=20, color=white)
    y -= 143
    cards = [("轻相", "普莎", "容易脱离地面；负责浮动、牵引与多目标控制。", HexColor("#EAF8FC")), ("第三锚点", "娜蒂娅", "不是旁观者；让两种异常保持在可生活的范围内。", WARM), ("重相", "伊嘉", "接触时施加异常负荷；负责压制与稳定控制。", HexColor("#E7EDF6"))]
    gap = 10
    card_w = (PAGE_W - MARGIN * 2 - gap * 2) / 3
    for i, (phase, name, body, fill) in enumerate(cards):
        x = MARGIN + i * (card_w + gap)
        draw_card(c, x, 124, card_w, y - 134, fill=fill)
        label(c, phase, x + 13, y - 30)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 16)
        c.drawString(x + 13, y - 59, name)
        draw_text(c, body, x + 13, y - 86, card_w - 26, size=7.8, leading=12.6, color=MUTED)
    draw_card(c, MARGIN, 62, PAGE_W - MARGIN * 2, 44, fill=white)
    draw_text(c, "异常不是宇宙真理，也不是命运特权。它只是三个普通生命之间，一段必须被长期照顾的关系。", MARGIN + 15, 86, PAGE_W - MARGIN * 2 - 30, size=8.2, leading=13, color=INK, align="center")
    finish_page(c, 3, "核心概念")


def page_visual(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "03 / VISUAL MODEL", "至冬野外调查员", "成熟、实用、温柔；所有宣传图与游戏内图共用这一模型。")
    left_w = 154
    draw_card(c, MARGIN, 79, left_w, y - 89, fill=NAVY, stroke=NAVY, radius=8)
    label(c, "CANONICAL ANCHORS", MARGIN + 16, y - 31, dark=True)
    draw_text(c, "过肩但不到腰的黑色轻波浪\n\n暖银灰圆框眼镜\n\n奶白高领与深灰蓝调查服\n\n右长左短的不对称短披肩\n\n哑光深石板蓝保暖打底\n\n平底中筒调查靴\n\n左腰后三层测量环", MARGIN + 16, y - 60, left_w - 32, size=8.2, leading=14.2, color=white)
    label(c, "PALETTE", MARGIN + 16, 143, dark=True)
    for i, (color, text) in enumerate([(NAVY, "深灰蓝"), (ICE_STRONG, "冰蓝"), (WARM, "暖纸色")]):
        sy = 118 - i * 21
        c.setFillColor(color)
        c.roundRect(MARGIN + 16, sy, 22, 11, 3, stroke=0, fill=1)
        c.setFillColor(HexColor("#DCEBFA"))
        c.setFont("NadiaCJK", 6.5)
        c.drawString(MARGIN + 45, sy + 2, text)
    image_x = MARGIN + left_w + 14
    draw_image_contain(c, ASSETS / "nadia_character_v3_canonical.png", image_x, 63, PAGE_W - MARGIN - image_x, y - 73, padding=4)
    finish_page(c, 4, "标准视觉")


def page_cats(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "04 / COMPANIONS", "不要用外观判断重量", "它们是真实的家猫，不是使魔，也不是元素生命。")
    gap = 14
    card_w = (PAGE_W - MARGIN * 2 - gap) / 2
    cats = [("nadia_pusha_v1_ingame.png", "轻相 / LIGHT PHASE", "普莎", "圆润、奶油金、琥珀眼。看起来很有分量，实际上可能被风慢慢带走。", HexColor("#EDF8FC")), ("nadia_igla_v1_ingame.png", "重相 / HEAVY PHASE", "伊嘉", "修长、象牙色、冰蓝眼。行动依旧轻巧，接触地面时却会让薄冰细裂。", HexColor("#E8EEF7"))]
    for i, (asset, phase, name, body, fill) in enumerate(cats):
        x = MARGIN + i * (card_w + gap)
        draw_card(c, x, 84, card_w, y - 94, fill=fill)
        c.saveState()
        clip = c.beginPath()
        clip.roundRect(x + 9, y - 178, card_w - 18, 154, 7)
        c.clipPath(clip, stroke=0, fill=0)
        draw_image_cover(c, ASSETS / asset, x + 9, y - 178, card_w - 18, 154)
        c.restoreState()
        label(c, phase, x + 14, y - 202)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 19)
        c.drawString(x + 14, y - 230, name)
        draw_text(c, body, x + 14, y - 257, card_w - 28, size=8.2, leading=13.2, color=INK)
    finish_page(c, 5, "同行者")


def page_relationship(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "05 / THREE COMPANIONS", "同行不是召唤", "她只是翻开记录册，让两名真实的同行者进入巡衡范围。")
    draw_card(c, MARGIN, y - 251, PAGE_W - MARGIN * 2, 242, fill=NAVY, stroke=NAVY, radius=8)
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(MARGIN + 7, y - 244, PAGE_W - MARGIN * 2 - 14, 228, 6)
    c.clipPath(clip, stroke=0, fill=0)
    draw_image_cover(c, ASSETS / "nadia_companions_v3_canonical_ingame.png", MARGIN + 7, y - 244, PAGE_W - MARGIN * 2 - 14, 228)
    c.restoreState()
    draw_card(c, MARGIN, 85, PAGE_W - MARGIN * 2, 135, fill=white)
    label(c, "THE THIRD ANCHOR", MARGIN + 16, 194)
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 14)
    c.drawString(MARGIN + 16, 169, "锚定负荷，而非真实质量")
    draw_text(c, "普莎更容易脱离地面，伊嘉在接触时施加异常承重；它们的生理机能与基本动作没有被重写。娜蒂娅的 Linchpin 长期兜住了这段关系，所以早年的读数才看起来近似守恒。", MARGIN + 16, 143, PAGE_W - MARGIN * 2 - 32, size=8.3, leading=13.4, color=MUTED)
    finish_page(c, 6, "三体关系")


def page_incident(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "06 / INCIDENT", "事故之后", "旧观测设施重新启动，所有仪器在同一时刻归零。")
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(MARGIN, y - 212, PAGE_W - MARGIN * 2, 201, 8)
    c.clipPath(clip, stroke=0, fill=0)
    draw_image_cover(c, ASSETS / "nadia_story_after_v1_ingame.png", MARGIN, y - 212, PAGE_W - MARGIN * 2, 201)
    c.restoreState()
    y -= 237
    draw_text(c, "醒来以后，两只猫仍然健康，却不再受到同一种方式的锚定。普莎会被强风带离地面，伊嘉会让薄冰与木板承受不合体型的负荷。", MARGIN, y, PAGE_W - MARGIN * 2, size=8.8, leading=14.5, color=INK)
    draw_card(c, MARGIN, 73, PAGE_W - MARGIN * 2, 83, fill=WARM, stroke=HexColor("#E2CFB2"))
    c.setFillColor(INK)
    c.setFont("NadiaCJK", 13)
    c.drawString(MARGIN + 16, 128, "她停止使用“恢复”，改用“稳定”。")
    draw_text(c, "改变已经发生。她真正需要照顾的是现在。", MARGIN + 16, 101, PAGE_W - MARGIN * 2 - 32, size=8.3, color=MUTED)
    finish_page(c, 7, "事故之后")


def page_curve(c: canvas.Canvas) -> None:
    start_page(c, dark=True)
    y = draw_section_header(c, PAGE_H, "07 / THIRD CURVE", "第三条曲线", "她过去把自己记作观察者，把两只猫记作两个样本。", dark=True)
    cx, cy = PAGE_W / 2, 313
    points = [(cx - 105, cy + 54, "普莎", "轻相"), (cx + 105, cy + 54, "伊嘉", "重相"), (cx, cy - 78, "娜蒂娅", "第三锚点")]
    c.setStrokeColor(HexColor("#5CBFE1"))
    c.setLineWidth(1.2)
    c.line(points[0][0], points[0][1], points[2][0], points[2][1])
    c.line(points[1][0], points[1][1], points[2][0], points[2][1])
    c.line(points[0][0], points[0][1], points[1][0], points[1][1])
    for i, (px, py, name, phase) in enumerate(points):
        c.setFillColor(GOLD if i == 2 else ICE_STRONG)
        c.circle(px, py, 27, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("NadiaCJK", 10)
        c.drawCentredString(px, py + 1, name)
        c.setFillColor(HexColor("#BDD4E8"))
        c.setFont("NadiaCJK", 7)
        c.drawCentredString(px, py - 42, phase)
    draw_card(c, MARGIN, 82, PAGE_W - MARGIN * 2, 94, fill=NAVY, stroke=HexColor("#274A70"))
    draw_text(c, "她把“双体异常长期观测记录”划掉，改成“三体异常长期观测记录”。样本数量写错只是她理解自己位置时的反应，不是异常开始失稳的原因。", MARGIN + 17, 143, PAGE_W - MARGIN * 2 - 34, size=8.5, leading=14, color=white, align="center")
    finish_page(c, 8, "第三条曲线", dark=True)


def page_mechanic(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "08 / CORE MECHANIC", "衡标 H", "五格状态把失衡写成一条普通玩家可忽略、高阶玩家可管理的路径。")
    draw_image_contain(c, ASSETS / "nadia_balance_v1_ingame.png", MARGIN, y - 231, PAGE_W - MARGIN * 2, 220, padding=4)
    y -= 250
    c.setFillColor(MUTED)
    c.setFont("NadiaCJK", 7)
    c.drawString(MARGIN, y - 2, "轻端 / 普莎")
    c.drawRightString(PAGE_W - MARGIN, y - 2, "伊嘉 / 重端")
    gap = 7
    cell_w = (PAGE_W - MARGIN * 2 - gap * 4) / 5
    for i, value in enumerate(["-2", "-1", "0", "+1", "+2"]):
        x = MARGIN + i * (cell_w + gap)
        draw_card(c, x, y - 44, cell_w, 25, fill=ICE_STRONG if value == "0" else white, radius=6)
        c.setFillColor(white if value == "0" else MUTED)
        c.setFont("NadiaCJK", 8)
        c.drawCentredString(x + cell_w / 2, y - 36, value)
    draw_card(c, MARGIN, 70, PAGE_W - MARGIN * 2, 103, fill=WARM, stroke=HexColor("#E2CFB2"))
    draw_text(c, "战技启动时 H = 0。Stellar Swirl 向轻端移动，Stellar-Conduct 向重端移动；再次施放战技或施放爆发都能主动回中。只到达 ±1 是普通归衡，曾到达 ±2 后回中才是完整归衡。", MARGIN + 16, 143, PAGE_W - MARGIN * 2 - 32, size=8.3, leading=13.4, color=INK)
    finish_page(c, 9, "衡标")


def page_phase(c: canvas.Canvas, page_no: int, index: str, title: str, subtitle: str, asset: str, phase_title: str, body: str, quote: str) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, index, title, subtitle)
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(MARGIN, y - 242, PAGE_W - MARGIN * 2, 232, 8)
    c.clipPath(clip, stroke=0, fill=0)
    draw_image_cover(c, ASSETS / asset, MARGIN, y - 242, PAGE_W - MARGIN * 2, 232)
    c.restoreState()
    draw_card(c, MARGIN, 88, PAGE_W - MARGIN * 2, 142, fill=white)
    label(c, phase_title, MARGIN + 16, 202)
    draw_text(c, body, MARGIN + 16, 174, PAGE_W - MARGIN * 2 - 32, size=8.5, leading=13.8, color=INK)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.line(MARGIN + 16, 113, MARGIN + 16, 143)
    draw_text(c, quote, MARGIN + 28, 134, PAGE_W - MARGIN * 2 - 44, size=8.3, leading=13, color=MUTED)
    finish_page(c, page_no, title)


def page_skill(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "12 / ELEMENTAL SKILL", "双相巡衡", "记录册一开，冰元素协同就已经开始；反应负责选择路线。")
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(MARGIN, y - 224, PAGE_W - MARGIN * 2, 214, 8)
    c.clipPath(clip, stroke=0, fill=0)
    draw_image_cover(c, ASSETS / "nadia_action_v2_ingame.png", MARGIN, y - 224, PAGE_W - MARGIN * 2, 214)
    c.restoreState()
    y -= 245
    gap = 12
    col_w = (PAGE_W - MARGIN * 2 - gap) / 2
    for i, (name, body) in enumerate([("基础协同", "技能提供低频后台冰元素协同，没有风或雷队友时也不会失去基本功能。"), ("归衡校读", "再次施放战技可以把非零 H 主动带回 0，让单路线队也能完成归衡循环。")]):
        x = MARGIN + i * (col_w + gap)
        draw_card(c, x, 81, col_w, y - 91, fill=white)
        label(c, f"0{i + 1}", x + 14, y - 28)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 12)
        c.drawString(x + 14, y - 52, name)
        draw_text(c, body, x + 14, y - 77, col_w - 28, size=7.9, leading=12.8, color=MUTED)
    finish_page(c, 13, "元素战技")


def page_burst(c: canvas.Canvas) -> None:
    start_page(c, dark=True)
    y = draw_section_header(c, PAGE_H, "13 / ELEMENTAL BURST", "三体归零·雪原校准", "零点不是终点，只是决定从哪里重新开始记录。", dark=True)
    draw_image_contain(c, ASSETS / "nadia_measurement_ring_v2_ingame.png", MARGIN + 8, y - 250, PAGE_W - MARGIN * 2 - 16, 236, padding=4)
    draw_card(c, MARGIN, 86, PAGE_W - MARGIN * 2, 132, fill=NAVY, stroke=HexColor("#274A70"))
    label(c, "ZERO-POINT FIELD", MARGIN + 16, 191, dark=True)
    draw_text(c, "爆发先将非零 H 归零，再建立零点测区。触发任一路线时，另一只猫也会提供一次较弱的伴随响应：轻中有重，重中有轻。", MARGIN + 16, 161, PAGE_W - MARGIN * 2 - 32, size=8.5, leading=13.8, color=white)
    c.setFillColor(ICE)
    c.setFont("NadiaCJK", 10)
    c.drawCentredString(PAGE_W / 2, 105, "“误差确认。重新归零。”")
    finish_page(c, 14, "元素爆发", dark=True)


def page_talents(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "14 / TALENTS", "误差本身也是记录", "端点停留提供稳定收益，完整归衡奖励主动操作。")
    items = [("外观不可作为量值", "连续触发同一路线，会稳定并刷新对应的端点观测状态。"), ("误差本身也是记录", "从端点完成完整归衡时，轻与重共同稳定战场并打开强化窗口。"), ("雪原札记", "在至冬探索时更容易发现部分区域特产，并改善雪原行进体验。")]
    for i, (title, body) in enumerate(items):
        top = y - i * 113
        draw_card(c, MARGIN, top - 98, PAGE_W - MARGIN * 2, 89, fill=white)
        c.setFillColor(ICE_STRONG if i < 2 else GOLD)
        c.circle(MARGIN + 28, top - 44, 14, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("NadiaCJK", 8)
        c.drawCentredString(MARGIN + 28, top - 47, str(i + 1))
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 12)
        c.drawString(MARGIN + 54, top - 35, title)
        draw_text(c, body, MARGIN + 54, top - 59, PAGE_W - MARGIN * 2 - 72, size=8.1, leading=12.7, color=MUTED)
    finish_page(c, 15, "固有天赋")


def page_constellations(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "15 / CONSTELLATION", "双衡仪座", "六条命之座让管理天平逐步走向完整的三体协同。")
    items = [("一", "不要相信眼睛", "更快进入端点观测。"), ("二", "重新称量", "强化牵引与压制。"), ("三", "记录直到一致", "元素战技等级提高。"), ("四", "误差从不是零", "归衡后打开强化窗口。"), ("五", "零点只是起点", "元素爆发等级提高。"), ("六", "我们三个都在这里", "零点测区内完整协同。")]
    gap_x, gap_y = 12, 11
    box_w = (PAGE_W - MARGIN * 2 - gap_x) / 2
    box_h = 92
    for i, (n, title, body) in enumerate(items):
        row, col = divmod(i, 2)
        x = MARGIN + col * (box_w + gap_x)
        top = y - row * (box_h + gap_y)
        draw_card(c, x, top - box_h, box_w, box_h, fill=white)
        c.setFillColor(GOLD if i == 5 else ICE_STRONG)
        c.setFont("NadiaCJK", 15)
        c.drawString(x + 14, top - 29, n)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 9.2)
        c.drawString(x + 43, top - 27, title)
        draw_text(c, body, x + 43, top - 50, box_w - 57, size=7.2, leading=11.3, color=MUTED)
    draw_card(c, MARGIN, 57, PAGE_W - MARGIN * 2, 47, fill=NAVY, stroke=NAVY)
    draw_text(c, "第六条不是口号，而是剧情结论：她们三个都在这里。", MARGIN + 15, 83, PAGE_W - MARGIN * 2 - 30, size=8.5, color=white, align="center")
    finish_page(c, 16, "命之座")


def page_quest(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "16 / LEGEND QUEST", "比雪更轻，比承诺更重", "双衡之章·第一幕 / 猫、砝码与第三个数字")
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(MARGIN, y - 236, PAGE_W - MARGIN * 2, 226, 8)
    c.clipPath(clip, stroke=0, fill=0)
    draw_image_cover(c, ASSETS / "nadia_quest_v2_canonical_refined.png", MARGIN, y - 236, PAGE_W - MARGIN * 2, 226)
    c.restoreState()
    y -= 254
    stages = [("01", "屋顶上的猫", "看似轻松的委托暴露异常再次变化。"), ("02", "重新运行的设施", "旧记录指向被遗漏的第三个对象。"), ("03", "拒绝强制复原", "她关闭旧系统的强制校准。"), ("04", "继续测量", "稳定现在，让三者继续共同生活。")]
    for i, (num, title, body) in enumerate(stages):
        col, row = i % 2, i // 2
        x = MARGIN + col * ((PAGE_W - MARGIN * 2) / 2)
        top = y - row * 68
        c.setFillColor(GOLD if i == 3 else ICE_STRONG)
        c.circle(x + 13, top - 13, 11, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("NadiaCJK", 6.5)
        c.drawCentredString(x + 13, top - 16, num)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 9.2)
        c.drawString(x + 32, top - 9, title)
        draw_text(c, body, x + 32, top - 30, (PAGE_W - MARGIN * 2) / 2 - 42, size=7.1, leading=10.8, color=MUTED)
    finish_page(c, 17, "传说任务")


def page_daily(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "17 / DAILY & VOICE", "严谨记录之外", "她仍然会被猫毛、风和一只太重的猫打断。")
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(MARGIN, y - 222, PAGE_W - MARGIN * 2, 212, 8)
    c.clipPath(clip, stroke=0, fill=0)
    draw_image_cover(c, ASSETS / "nadia_companions_v3_canonical_ingame.png", MARGIN, y - 222, PAGE_W - MARGIN * 2, 212)
    c.restoreState()
    for i, quote in enumerate(["“这个我还没有证据。”", "“记录，并不是为了证明自己最开始是对的。”", "“抱伊嘉之前，最好先活动一下腰。”"]):
        qy = y - 254 - i * 58
        draw_card(c, MARGIN, qy - 45, PAGE_W - MARGIN * 2, 42, fill=white)
        c.setFillColor(GOLD)
        c.rect(MARGIN, qy - 45, 3, 42, stroke=0, fill=1)
        draw_text(c, quote, MARGIN + 16, qy - 20, PAGE_W - MARGIN * 2 - 32, size=8.5, color=INK)
    finish_page(c, 18, "日常与语音")


def page_objects(c: canvas.Canvas) -> None:
    start_page(c)
    y = draw_section_header(c, PAGE_H, "18 / OBJECTS", "零点之外", "记录册、悬浮环与料理，都把“看起来”和“实际读数”放在一起。")
    items = [("nadia_catalyst_v2_ingame.png", "组合式法器", "零点不是答案"), ("nadia_field_notebook_v1_ingame.png", "野外记录册", "写下未解之物"), ("nadia_dish_v1_ingame.png", "角色料理", "两端之间")]
    gap = 10
    box_w = (PAGE_W - MARGIN * 2 - gap * 2) / 3
    for i, (asset, kicker, title) in enumerate(items):
        x = MARGIN + i * (box_w + gap)
        draw_card(c, x, y - 238, box_w, 229, fill=white)
        draw_image_contain(c, ASSETS / asset, x + 7, y - 160, box_w - 14, 142, padding=3)
        label(c, kicker, x + 11, y - 183)
        c.setFillColor(INK)
        c.setFont("NadiaCJK", 10.2)
        c.drawString(x + 11, y - 207, title)
    draw_card(c, MARGIN, 78, PAGE_W - MARGIN * 2, 146, fill=NAVY, stroke=NAVY)
    label(c, "PLAYER IMPRESSION", MARGIN + 16, 196, dark=True)
    draw_text(c, "第一次看到：戴圆框眼镜、带两只猫的至冬记录员。\n\n玩一段时间：技能真的在管理轻端、重端与归衡。\n\n做完传说任务：她研究的从来不只是猫。", MARGIN + 16, 168, PAGE_W - MARGIN * 2 - 32, size=8.6, leading=14.1, color=white)
    finish_page(c, 19, "法器与日常物件")


def page_end(c: canvas.Canvas) -> None:
    draw_image_cover(c, ASSETS / "nadia_splash_v4_canonical_refined.png", 0, 0, PAGE_W, PAGE_H, anchor="top")
    c.saveState()
    if hasattr(c, "setFillAlpha"):
        c.setFillAlpha(0.9)
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, 222, stroke=0, fill=1)
    c.restoreState()
    label(c, "19 / LAST RECORD", MARGIN, 190, dark=True)
    c.setFillColor(white)
    c.setFont("NadiaCJK", 19)
    c.drawString(MARGIN, 149, "她没有把一切变回过去。")
    draw_text(c, "她想弄明白，怎样才能让已经改变的一切继续稳定地走向未来。", MARGIN, 117, PAGE_W - MARGIN * 2, size=10.5, leading=17, color=white)
    c.setFillColor(HexColor("#DCEBFA"))
    c.setFont("NadiaCJK", 7.2)
    c.drawString(MARGIN, 53, "原创同人角色 / 基于《原神》7.0 世界观语汇 / 非官方资料")
    c.drawString(MARGIN, 37, "NADIA SADOVA / THE THIRD ANCHOR")
    finish_page(c, 20, "最后记录", dark=True)


def main() -> None:
    register_fonts()
    validate_assets(REQUIRED_ASSETS)
    c = canvas.Canvas(str(OUT), pagesize=A5, pageCompression=1)
    c.setTitle("娜蒂娅「两衡之间」正式角色档案")
    c.setAuthor("Original fan character dossier")
    c.setSubject("Public-safe original Genshin-inspired fan character dossier")
    c.setKeywords("Nadia Sadova, character dossier, Snezhnaya, fan character")
    page_cover(c)
    page_profile(c)
    page_concept(c)
    page_visual(c)
    page_cats(c)
    page_relationship(c)
    page_incident(c)
    page_curve(c)
    page_mechanic(c)
    page_phase(c, 10, "09 / LIGHT PHASE", "向轻端", "Stellar Swirl 让衡标向普莎一侧移动。", "nadia_h_light_v1_ingame.png", "PUSHA RESPONSE", "普莎缓缓离地，雪粒反常地向上飘动。轻端强调牵引、浮动与多目标控制；到达 -2 后进入轻端观测。", "“普莎，慢一点。”")
    page_phase(c, 11, "10 / HEAVY PHASE", "向重端", "Stellar-Conduct 让衡标向伊嘉一侧移动。", "nadia_h_heavy_v1_ingame.png", "IGLA RESPONSE", "伊嘉依旧轻巧跃起，却在落地时造成低沉冰裂。重端强调压制、迟滞与单目标稳定控制。", "“伊嘉，落点确认。”")
    page_phase(c, 12, "11 / RETURN TO ZERO", "归衡", "再次施放战技或施放爆发，主动把非零 H 带回中央。", "nadia_h_zero_v1_ingame.png", "RETURN RESPONSE", "普莎从上方缓缓下降，伊嘉从下方跃起。轻与重不互相抵消，而是在同一位置短暂共同稳定战场。", "“从一端回到中央。很好，归衡。”")
    page_skill(c)
    page_burst(c)
    page_talents(c)
    page_constellations(c)
    page_quest(c)
    page_daily(c)
    page_objects(c)
    page_end(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
