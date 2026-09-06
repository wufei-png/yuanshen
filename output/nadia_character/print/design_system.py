from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUTPUT_DIR = ROOT.parent / "pdf"
TMP_DIR = ROOT.parents[1] / "tmp" / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)
MM = 72 / 25.4

NAVY = HexColor("#122B4B")
NIGHT = HexColor("#071426")
INK = HexColor("#17243A")
MUTED = HexColor("#667C99")
PAPER = HexColor("#F3F7FB")
ICE = HexColor("#99E4FA")
ICE_STRONG = HexColor("#3EA4CF")
GOLD = HexColor("#D2B36D")
WARM = HexColor("#F4E7D6")
LINE = HexColor("#CAD9E8")

FONT_PATHS = [
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
]
FONT_SANS = Path("/System/Library/Fonts/STHeiti Medium.ttc")
FONT_SERIF = Path("/System/Library/Fonts/Supplemental/Songti.ttc")
FONT_LATIN = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")
FONT_LATIN_BOLD = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")


def register_fonts() -> None:
    cjk_path: Path | None = None
    for path in FONT_PATHS:
        if path.exists():
            pdfmetrics.registerFont(TTFont("NadiaCJK", str(path), subfontIndex=0))
            cjk_path = path
            break
    if cjk_path is None:
        raise FileNotFoundError("No supported CJK font was found")

    # The postcard HTML deliberately separates sans display labels from its
    # Songti editorial copy. Register the same families for the print build.
    if FONT_SANS.exists():
        pdfmetrics.registerFont(
            TTFont("NadiaSans", str(FONT_SANS), subfontIndex=1)
        )
    else:
        pdfmetrics.registerFont(TTFont("NadiaSans", str(cjk_path), subfontIndex=0))
    if FONT_SERIF.exists():
        pdfmetrics.registerFont(
            TTFont("NadiaSerif", str(FONT_SERIF), subfontIndex=6)
        )
        pdfmetrics.registerFont(
            TTFont("NadiaSerifBold", str(FONT_SERIF), subfontIndex=1)
        )
    else:
        pdfmetrics.registerFont(TTFont("NadiaSerif", str(cjk_path), subfontIndex=0))
        pdfmetrics.registerFont(
            TTFont("NadiaSerifBold", str(cjk_path), subfontIndex=0)
        )
    if FONT_LATIN.exists():
        pdfmetrics.registerFont(TTFont("NadiaLatin", str(FONT_LATIN)))
    if FONT_LATIN_BOLD.exists():
        pdfmetrics.registerFont(TTFont("NadiaLatinBold", str(FONT_LATIN_BOLD)))


def mm(value: float) -> float:
    return value * MM


def alpha_color(color: Color, alpha: float) -> Color:
    return Color(color.red, color.green, color.blue, alpha=alpha)


def image_size(path: Path) -> tuple[float, float]:
    return ImageReader(str(path)).getSize()


@lru_cache(maxsize=None)
def pdf_asset(path: Path) -> Path:
    """Embed original artwork without a second lossy JPEG compression pass."""
    return path


def draw_image_cover(
    c: canvas.Canvas,
    path: Path,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    anchor: str = "center",
) -> None:
    image = ImageReader(str(pdf_asset(path)))
    iw, ih = image.getSize()
    scale = max(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (width - dw) / 2
    if anchor == "top":
        dy = y + height - dh
    elif anchor == "bottom":
        dy = y
    else:
        dy = y + (height - dh) / 2
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(image, dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    c.restoreState()


def draw_image_contain(
    c: canvas.Canvas,
    path: Path,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    padding: float = 0,
) -> None:
    image = ImageReader(str(pdf_asset(path)))
    iw, ih = image.getSize()
    inner_w = max(1, width - padding * 2)
    inner_h = max(1, height - padding * 2)
    scale = min(inner_w / iw, inner_h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (width - dw) / 2
    dy = y + (height - dh) / 2
    c.drawImage(image, dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
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


def draw_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    size: float = 9,
    leading: float | None = None,
    color: Color = INK,
    font: str = "NadiaCJK",
    align: str = "left",
) -> float:
    leading = leading or size * 1.55
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, width):
        if line:
            if align == "center":
                c.drawCentredString(x + width / 2, y, line)
            elif align == "right":
                c.drawRightString(x + width, y, line)
            else:
                c.drawString(x, y, line)
        y -= leading
    return y


def draw_card(
    c: canvas.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    fill: Color = white,
    stroke: Color = LINE,
    radius: float = 10,
    line_width: float = 0.7,
) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(line_width)
    c.roundRect(x, y, width, height, radius, stroke=1, fill=1)


def draw_footer(
    c: canvas.Canvas,
    page_w: float,
    page_no: int,
    *,
    dark: bool = False,
    margin: float = 34,
) -> None:
    color = HexColor("#D9E8F5") if dark else MUTED
    c.setStrokeColor(color)
    c.setLineWidth(0.45)
    c.line(margin, 25, page_w - margin, 25)
    c.setFillColor(color)
    c.setFont("NadiaCJK", 6.3)
    c.drawString(margin, 13, "娜蒂娅「两衡之间」 / 原创同人角色档案")
    c.drawRightString(page_w - margin, 13, f"{page_no:02d}")


def draw_section_header(
    c: canvas.Canvas,
    page_h: float,
    index: str,
    title: str,
    subtitle: str,
    *,
    dark: bool = False,
    margin: float = 34,
) -> float:
    accent = ICE if dark else ICE_STRONG
    main = white if dark else INK
    secondary = HexColor("#C7D9EA") if dark else MUTED
    y = page_h - 51
    c.setFillColor(accent)
    c.setFont("NadiaCJK", 7.2)
    c.drawString(margin, y, index)
    c.setFillColor(main)
    c.setFont("NadiaCJK", 23)
    c.drawString(margin, y - 32, title)
    return draw_text(
        c,
        subtitle,
        margin,
        y - 55,
        c._pagesize[0] - margin * 2,
        size=8.2,
        leading=12.4,
        color=secondary,
    )


POSTCARDS = [
    {
        "num": 1,
        "group": "角色登场",
        "kicker": "开场记录",
        "title": "两衡之间",
        "subtitle": "在无法被称量之物中，找到第三条曲线。",
        "back_title": "娜蒂娅·萨多娃",
        "back_body": "在雪原上记录无法被称量之物的人，也在不知不觉间成为了记录中的第三个对象。",
        "tag": "角色封面",
        "image": "nadia_splash_v4_canonical_refined.png",
        "mode": "contain",
    },
    {
        "num": 2,
        "group": "角色登场",
        "kicker": "角色档案",
        "title": "角色档案",
        "subtitle": "至冬 · 冰 · 法器 · 五星",
        "back_title": "双衡仪座",
        "back_body": "民间异常现象记录员、野外调查研究者。战斗定位是后台冰元素协同、控场与双路线状态管理。",
        "tag": "基础信息",
        "image": "nadia_portrait_v1_ingame.png",
        "mode": "cover",
    },
    {
        "num": 3,
        "group": "角色登场",
        "kicker": "性格",
        "title": "再测一次",
        "subtitle": "温柔知性，专业可靠，偶尔天然呆。",
        "back_title": "她的工作方式",
        "back_body": "面对最违反常识的事情，她的第一反应不是惊叫，而是把眼镜推回去，再测一次。没有证据时，她会直接承认。",
        "tag": "性格记录",
        "image": "nadia_character_v3_canonical.png",
        "mode": "contain",
    },
    {
        "num": 4,
        "group": "角色登场",
        "kicker": "观测装置",
        "title": "冰蓝测量环",
        "subtitle": "悬浮、倾斜、归衡，都是可读的状态。",
        "back_title": "衡标在她手中",
        "back_body": "圆框眼镜看见细微偏差，三层测量环记下风与锚定负荷。指针总会越过正常刻度，因为仪器从未量出三人的极限。",
        "tag": "视觉锚点",
        "image": "nadia_measurement_ring_v2_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 5,
        "group": "同行者",
        "kicker": "同行者",
        "title": "不要相信外观",
        "subtitle": "一只向上，一只向下。",
        "back_title": "普莎与伊嘉",
        "back_body": "它们是真实的家猫，不是使魔，也不是元素生命。只是与地面、空气以及彼此的锚定方式发生了改变。",
        "tag": "关系总览",
        "image": "nadia_companions_v3_canonical_ingame.png",
        "mode": "cover",
    },
    {
        "num": 6,
        "group": "同行者",
        "kicker": "轻相",
        "title": "普莎 Pusha",
        "subtitle": "圆润、奶油金、琥珀眼。",
        "back_title": "看起来很重",
        "back_body": "它像一团很有分量的绒毛，实际上可能被风慢慢带走。长命锁与安全牵引绳，首先是为了防止它飘离地面。",
        "tag": "普莎",
        "image": "nadia_pusha_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 7,
        "group": "同行者",
        "kicker": "重相",
        "title": "伊嘉 Igla",
        "subtitle": "修长、象牙色、冰蓝眼。",
        "back_title": "看起来很轻",
        "back_body": "它走路依旧轻巧，却会让薄冰细裂、木板下陷。它已经适应自己的状态，只有第一次抱起它的人还没有。",
        "tag": "伊嘉",
        "image": "nadia_igla_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 8,
        "group": "同行者",
        "kicker": "第三锚点",
        "title": "第三条曲线",
        "subtitle": "她并不是旁观者。",
        "back_title": "三体，而非双体",
        "back_body": "轻与重不是两只猫之间封闭守恒的交换。娜蒂娅一直是让两种异常保持在可生活范围内的第三锚点。",
        "tag": "三体关系",
        "image": "nadia_h_zero_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 9,
        "group": "战斗方式",
        "kicker": "核心机制",
        "title": "衡标 H",
        "subtitle": "-2 · -1 · 0 · +1 · +2",
        "back_title": "从归衡开始",
        "back_body": "元素战技启动时 H = 0。Stellar 原生反应先按自身规则结算，再把它推向轻端或重端；再次施放战技与爆发都能主动回中。",
        "tag": "机制总览",
        "image": "nadia_balance_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 10,
        "group": "战斗方式",
        "kicker": "轻端",
        "title": "向轻端",
        "subtitle": "浮动、牵引、多目标。",
        "back_title": "普莎响应",
        "back_body": "触发 Stellar Swirl 时，衡标向轻端移动。普莎缓缓离地，雪粒反常地向上飘动，为战场带来牵引与浮动。",
        "tag": "轻端响应",
        "image": "nadia_h_light_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 11,
        "group": "战斗方式",
        "kicker": "重端",
        "title": "向重端",
        "subtitle": "压制、迟滞、单目标。",
        "back_title": "伊嘉响应",
        "back_body": "触发 Stellar-Conduct 时，衡标向重端移动。伊嘉落地，造成低沉冰裂，为战场带来迟滞与稳定压制。",
        "tag": "重端响应",
        "image": "nadia_h_heavy_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 12,
        "group": "战斗方式",
        "kicker": "归衡",
        "title": "回到中央",
        "subtitle": "轻与重不互相抵消。",
        "back_title": "归衡响应",
        "back_body": "再次施放战技或施放爆发，可以让衡标主动回到中央。轻与重的轨迹交汇，共同稳定战场。",
        "tag": "归衡",
        "image": "nadia_h_zero_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 13,
        "group": "战斗方式",
        "kicker": "元素战技",
        "title": "双相巡衡",
        "subtitle": "记录册打开，同行者入场。",
        "back_title": "稳定的基础协同",
        "back_body": "技能本身提供稳定的后台冰元素协同；Stellar 原生反应自身的场地、伤害、能量与 Radiance 照常结算，H 只记录轻端或重端路线，不是让技能开始工作的前提。",
        "tag": "战技",
        "image": "nadia_action_v2_ingame.png",
        "mode": "cover",
    },
    {
        "num": 14,
        "group": "战斗方式",
        "kicker": "元素爆发",
        "title": "三体归零",
        "subtitle": "轻中有重，重中有轻。",
        "back_title": "雪原校准",
        "back_body": "爆发先让衡标回到中央，再建立零点测区。触发一种路线时，另一只猫也会提供较弱的伴随响应。",
        "tag": "爆发",
        "image": "nadia_splash_v4_canonical_refined.png",
        "mode": "contain",
    },
    {
        "num": 15,
        "group": "战斗方式",
        "kicker": "固有天赋",
        "title": "误差也是记录",
        "subtitle": "真正的高阶玩法不是永远停在某一边。",
        "back_title": "把失衡带回来",
        "back_body": "连续同类反应会稳定对应的端点观测；把衡标从端点带回中央，则让归衡响应得到强化。",
        "tag": "天赋",
        "image": "nadia_h_zero_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 16,
        "group": "故事与日常",
        "kicker": "故事起点",
        "title": "事故之后",
        "subtitle": "她把自己写成观察者。",
        "back_title": "旧观测设施",
        "back_body": "暴风雪中的设施重新启动，所有仪器同时归零。醒来以后，两只猫仍然健康，却不再受到同一种方式的锚定。",
        "tag": "故事",
        "image": "nadia_story_after_v1_ingame.png",
        "mode": "cover",
    },
    {
        "num": 17,
        "group": "故事与日常",
        "kicker": "传说任务",
        "title": "比雪更轻",
        "subtitle": "比承诺更重。",
        "back_title": "猫、砝码与第三个数字",
        "back_body": "重新运行的旧设施要求三者强制复原。娜蒂娅必须回答：复原是为了它们，还是为了让自己安心？",
        "tag": "任务日志",
        "image": "nadia_quest_v2_canonical_refined.png",
        "mode": "cover",
    },
    {
        "num": 18,
        "group": "故事与日常",
        "kicker": "故事选择",
        "title": "稳定现在",
        "subtitle": "拒绝强制复原。",
        "back_title": "复原不是唯一答案",
        "back_body": "她没有把生活退回事故以前，而是关闭旧系统的强制校准，选择让已经改变的三者继续稳定地走向未来。",
        "tag": "剧情结论",
        "image": "nadia_choice_v1_ingame.png",
        "mode": "cover",
    },
    {
        "num": 19,
        "group": "故事与日常",
        "kicker": "专属法器",
        "title": "零点不是答案",
        "subtitle": "只是决定从哪里开始记录。",
        "back_title": "组合式记录册",
        "back_body": "书页、防水封皮与悬浮测量环组成法器。攻击时页面自行翻动，刻度在空气中形成冰晶坐标。",
        "tag": "法器",
        "image": "nadia_catalyst_v2_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 20,
        "group": "故事与日常",
        "kicker": "角色料理",
        "title": "两端之间",
        "subtitle": "只靠看，永远猜不准。",
        "back_title": "暖烤点心与热奶油酱",
        "back_body": "盘子两侧分别放着圆形和细长的小点心，外观与实际的蓬松度、重量恰好相反。",
        "tag": "料理",
        "image": "nadia_dish_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 21,
        "group": "故事与日常",
        "kicker": "日常与语音",
        "title": "至少刚才没有",
        "subtitle": "远处传来一声猫叫。",
        "back_title": "猫毛、风与秤",
        "back_body": "“这个我还没有证据。”\n“记录，并不是为了证明自己最开始是对的。”",
        "tag": "语音",
        "image": "nadia_companions_v3_canonical_ingame.png",
        "mode": "cover",
    },
    {
        "num": 22,
        "group": "故事与日常",
        "kicker": "命之座",
        "title": "双衡仪座",
        "subtitle": "我们三个都在这里。",
        "back_title": "从第一条到最后一条",
        "back_body": "六条命之座逐步强化轻端、重端、归衡与零点测区，最后把剧情结论写进机制：三者都在这里。",
        "tag": "命之座",
        "image": "nadia_h_zero_v1_ingame.png",
        "mode": "right_contain",
    },
    {
        "num": 23,
        "group": "故事与日常",
        "kicker": "最后记录",
        "title": "第三条曲线",
        "subtitle": "她们三个都在这里。",
        "back_title": "继续测量。还有……继续养。",
        "back_body": "她没有把一切变回过去。她想弄明白，怎样才能让已经改变的一切继续稳定地走向未来。",
        "tag": "结语",
        "image": "nadia_quest_v2_canonical_refined.png",
        "mode": "cover",
    },
    {
        "num": 24,
        "group": "故事与日常",
        "kicker": "现场记录",
        "title": "异常不等于错误",
        "subtitle": "一份可以继续写下去的记录。",
        "back_title": "记录仍在继续",
        "back_body": "这不是对过去的修复报告，而是一份关于三名同行者如何共同生活的持续观察。",
        "tag": "收束卡",
        "image": "nadia_field_note_v1_ingame.png",
        "mode": "cover",
    },
]


def validate_assets(names: Iterable[str]) -> None:
    missing = [name for name in names if not (ASSETS / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing assets: {missing}")
