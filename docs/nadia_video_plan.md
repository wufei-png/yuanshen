# 娜蒂娅介绍视频制作规格（MVP）

> 状态：V01/V03 两条 720p 试片已生成且视觉检查通过；V04/V05 两条 720p 试片已导入并完成文件与抽帧核验；V07/V08 已从 Downloads 导入并完成文件与抽帧核验；六条当前 720p 视频已复制到公开 HTML 资源目录并完成挂载。V06 视频已放弃，K10/K11 仅保留为静态动作板参考；音频/技术验收待完成。
> 角色：娜蒂娅「两衡之间」
> 依赖：`docs/genshin_character_full_design.md`（身份与故事）、`docs/nadia_skill_presentation.md`（技能逐镜）、`docs/nadia_voice_script.md`（对白 MP3）、现有 canonical 静帧。
> 本轮执行单：[`docs/nadia_video_pilot.md`](nadia_video_pilot.md)

---

## 0. 当前决策基线

| 项       | 选择                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| 去处     | HTML 分享包的当前 720p 预览 + 后续一条横屏叙事 PV，共用同一套成片                                      |
| 模型     | Seedance 2.0；试片优先标准模型，1080p 定稿不用 Fast（若入口提供该变体）                                      |
| 画幅     | 16:9；关键帧 1920×1080；不直接把现有 3:2 / 2:3 图当首尾帧                                                    |
| 批次     | 原 MVP 规划 8 条；V06 视频放弃，当前挂载 V01、V03–V05、V07、V08 六条                                  |
| 出图本轮 | 首轮 K01、K01E、K04、K05 已生成；K06、K07、K08 v3、K09 v9 已生成且视觉确认；K10–K15 已生成并完成初步视觉检查 |
| 视频试跑 | V01/V03 各 6s、V04/V05 各 5s、V07 约 8s、V08 约 6s 的 720p 已导入；保留源文件编码/水印状态，待技术/音频验收 |
| 声音     | 开启模型环境音/动作音效；提示词禁止模型对白；后期叠现有 MP3                                                  |
| 模式     | V01 用 K01→K01E 首尾帧；V03 用 K04→K05 首尾帧。canonical 图只用于关键帧/身份参考，不写死未确认的接口参数     |
| 实战边界 | 无队友、无官方 HUD、无伤害数字；目标只用抽象冰晶剪影或画外受击                                               |
| Q        | 视频暂不制作；K10/K11 仍保留为 BOARD 06 的静态爆发动作板参考，12 秒场地循环留后续批次                   |
| 生活     | 「风」+「抱错了」                                                                                            |
| PV       | 叙事剪辑：V01 → V07 → V08 → V03 → V04 → V05；V02 只进技能页，V06 视频不进 PV                           |

隐私：禁止使用 `xiting/*.jpg` 或任何真人/真猫照片。风格参考只用仓库内已生成的 canonical PNG。

---

## 1. 阶段

| 阶段 | 产物                                                                             | 本轮              |
| ---- | -------------------------------------------------------------------------------- | ----------------- |
| A    | 本文总规划 + [`docs/nadia_video_pilot.md`](nadia_video_pilot.md) 试片执行单      | **做**            |
| B    | 试片关键帧 K01/K04/K05 → `tmp/video_stills/`；K06–K09 已生成                     | **已完成**        |
| C    | V01、V03–V05 试片来自 `tmp/video_trials/`，V07/V08 来自 Downloads；当前副本已进入公开资源 | **已完成/待验收** |
| D    | 通过验收的镜头制作 1080p 定稿 → `output/nadia_character/assets/video/`          | 试片通过后        |
| E    | 叙事 PV 混音剪辑；HTML 挂载                                                     | HTML 已挂载      |

当前公开 HTML 使用六条 720p 试片；公开资源副本保留原始编码及源文件水印状态，不等同于 1080p 定稿。现有分享 ZIP 暂不重打包，待音频与完整技术验收完成后再决定。Git 已精确忽略 `tmp/video_stills/` 和 `tmp/video_trials/`。

### 1.1 本轮硬边界

- 试片只验证角色身份、首尾连续性、动作落点和模型环境声；不宣称已经完成完整技能展示。
- `nadia_character_v3_canonical.png` 是人物身份主参考；其他图片按 `docs/nadia_video_pilot.md` 的优先级使用，不能把互相冲突的版本全部并列塞入同一请求。
- 生成声音开启只代表模型生成环境音/动作音效，不允许生成对白；娜蒂娅台词仍使用仓库已有 MP3。
- 视频入口没有明确提供的字段（例如 `camera_fixed`、`watermark`）不写成必填 API 参数；镜头运动写进提示词，实际开关按当前界面记录。

---

## 2. 共用锁：全量制作阶段参考

> 试片不机械地把本节所有文字和所有参考图同时粘贴。V01/V03 必须优先遵循 §1.1 和 [`docs/nadia_video_pilot.md`](nadia_video_pilot.md) 的公开 canonical 参考层级；本节中与公开参考图冲突的细节不覆盖参考图。

### 2.1 身份锁（中文）

成年女性冰雪调查员角色，约 27 岁气质，身高感 162 cm。黑色过肩轻波浪，发尾内收，刘海轻度不对称，不是齐肩短发，也不是齐腰长发。暖银色细金属圆椭圆框眼镜，无眼镜链，镜片不挡眼。脑后双环测量夹：一环悬极轻银白羽片，一环悬小型深色金属坠。右长左短的不对称深灰蓝调查短披肩，细绒滚边，不是大毛领。乳白高领内搭，修身石墨蓝调查服，胸腹不裸露。不透明哑光深石板蓝保暖裤，无透肤、无黑丝、无蕾丝。深灰蓝平底中筒调查靴，不是高跟鞋。左腰稍后三层可转动冰蓝测量环。表情温柔知性，几乎不露齿，专业可靠，偶有一点天然呆。不是少女、不是御姐战姬、不是猫娘。

两只真实家猫，不是使魔、不是元素生命、不是机械体。圆润奶油金长毛猫：头顶、耳缘、背部和尾部为奶油金或淡黄色，胸腹与四爪为清楚的白色分区，毛发蓬松且层次稳定；琥珀色圆眼，神情温和、亲和、好奇，嘴角自然放松；佩戴银蓝色空心长命锁，锁体中心镂空清晰可见，轮廓、尺寸和位置固定，不能变成实心菱形。修长象牙色短毛猫：耳鼻尾有极淡奶茶色，冰蓝色眼睛，动作轻巧；佩戴炭灰蓝厚项圈，下面一颗哑光冰石。两只猫体型必须明显不同，禁止画成一对双胞胎或一只双头猫。提交给模型的提示词只使用这些外观、饰品和位置描述，不使用项目专有名。

### 2.2 Identity lock (English, for GPT Image)

Stylized anime game adult female ice-field surveyor, mid-20s impression, 162 cm impression. Dark wavy hair just past the shoulders, tapered ends, slightly asymmetrical bangs. Thin warm-silver oval-round glasses, no glasses chain. Dual-ring hair clip: one ring with a tiny silver-white feather, one with a small dark metal weight. Asymmetric short survey cloak, longer on her right, shorter on her left, graphite-blue, thin fleece trim, not a fur collar. Cream high-collar inner layer, fitted dark gray-blue coat, no cleavage. Opaque matte slate-blue winter leggings, no stockings, no translucency. Flat practical mid-calf boots, not heels. Three-layer ice-blue measuring rings at the left-rear waist. Gentle intellectual expression, almost no teeth. Not a loli, not an icy queen, not a catgirl.

Two real house cats, not familiars. One is a round cream-gold long-haired cat with cream-gold or pale-yellow fur on the crown, ear edges, back, and tail, clearly separated white fur on the chest and all four paws, stable fluffy layers, round open amber eyes, a soft friendly curious expression, a relaxed small cat mouth, and a hollow silver-blue lock charm with a clearly visible open center. The charm's shape, scale, and placement stay fixed; it must not become a solid diamond. The other is a slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone. They must remain two distinct cats. In model prompts, use these visual, accessory, expression, and position descriptions instead of project-specific names.

### 2.3 两套风格

**宣传风（仅 V01 / K01）**
提高冰晶、风雪与体积光密度，电影感，接近 `nadia_splash_v4_canonical_refined.png`。仍锁定发长、服装、眼镜、两猫品种。

**游戏内风（V02–V08）**
清晰克制，剪影可读，少炫光，接近 `nadia_action_v2_ingame.png`、`nadia_character_v3_canonical.png`。先让人读到「谁在上、谁在下、有没有回中」，再给特效。

### 2.4 共用负面

中文：文字、字幕、水印、LOGO、技能图标、血条、伤害数字、任何官方游戏 UI、任何现成角色、敌方角色面具、猫耳、猫尾长在人身上、裸露、透肤黑丝、高跟鞋、齐腰长发、齐刘海幼态、机甲、魔法少女法杖、把猫收进法器、单只猫、三只以上的猫、照片写实、真人脸。

English: text, subtitles, watermark, UI, HUD, damage numbers, any official game interface, recognizable existing characters, enemy masks, cat ears on the human, catgirl, translucent tights, high heels, photoreal, extra limbs, merged cats, kittens, armor, logos.

### 2.5 画面技术

- 画幅 16:9，输出 1920×1080 PNG。
- 脸、两只猫、测量环离边至少 8%。
- 首尾帧必须保持同一场景逻辑、人物身份、服装和光线方向；固定机位镜头保持同一机位，V03 允许按提示词从扣锁近景连续拉到正面中景。
- 现有 3:2 / 2:3 图只作风格参考，不要直接裁成 16:9 当首尾帧。

---

## 3. 镜头总表

| ID  | 内容             | Seedance 模式 | 时长 | 风格       | 关键帧   | HTML                                   | PV       | 后期对白    |
| --- | ---------------- | ------------- | ---- | ---------- | -------- | -------------------------------------- | -------- | ----------- |
| V01 | 登场「两衡之间」 | 首尾帧        | 6s   | 宣传       | K01→K01E | `index.html` hero                      | 开场     | 语音 01     |
| V02 | 普攻「霜度测录」 | 首尾帧        | 6s   | 游戏内     | K02→K03  | `skills.html` `#boards` BOARD 01       | 不进     | 无          |
| V03 | 战技「双相巡衡」 | 首尾帧        | 6s   | 游戏内     | K04→K05  | BOARD 02                               | 中段     | 语音 06     |
| V04 | 轻相·普莎        | 首尾帧        | 5s   | 游戏内     | K06→K07  | BOARD 03                               | 中段     | 语音 07     |
| V05 | 重相·伊嘉        | 首尾帧        | 5s   | 游戏内     | K08→K09  | BOARD 04                               | 中段     | 语音 08     |
| V06 | 爆发起手→锁环    | 首尾帧        | 6s   | 游戏内     | K10→K11  | **放弃视频；BOARD 06 保留静态图**      | 不进     | 不叠加     |
| V07 | 生活「风」       | 首尾帧        | 8s   | 游戏内日常 | K12→K13  | `index.html` `#companions` 生活片段区  | 开场后   | 语音 03     |
| V08 | 生活「抱错了」   | 首尾帧        | 6s   | 游戏内日常 | K14→K15  | `index.html` `#companions` 生活片段区  | 紧接 V07 | 语音 05     |

BOARD 05 归衡校读本批不做视频。

建议成片文件名：

```text
output/nadia_character/assets/video/stills/nadia_video_k01_v01_intro_start_1920x1080.png
output/nadia_character/assets/video/nadia_video_v01_intro_720p_a01.mp4
output/nadia_character/assets/video/nadia_video_v03_skill_720p_a01.mp4
output/nadia_character/assets/video/nadia_video_v04_light_720p_a01.mp4
output/nadia_character/assets/video/nadia_video_v05_heavy_720p_a01.mp4
output/nadia_character/assets/video/nadia_video_v07_wind_720p_a01.mp4
output/nadia_character/assets/video/nadia_video_v08_hug_720p_a01.mp4
```

试跑用 `tmp/video_stills/`、`tmp/video_trials/`，文件名加 `_720p`。

---

## 4. 关键帧出图提示词

每张都先贴 §2.1 或 §2.2，再贴风格句，再贴下面的构图段。参考图按列表作为 image reference，不要当控制网乱改五官。

### 共用参考图

| 用途       | 路径                                                                           |
| ---------- | ------------------------------------------------------------------------------ |
| 宣传风全身 | `output/nadia_character/assets/nadia_splash_v4_canonical_refined.png`          |
| 标准立绘   | `output/nadia_character/assets/nadia_character_v3_canonical.png`               |
| 游戏内战斗 | `output/nadia_character/assets/nadia_action_v2_ingame.png`                     |
| 爆发构图   | `output/nadia_character/assets/nadia_action_v3_ingame.png`                     |
| 普莎       | `output/nadia_character/assets/nadia_pusha_v1_ingame.png`                      |
| 伊嘉       | `output/nadia_character/assets/nadia_igla_v1_ingame.png`                       |
| 日常观测站 | `output/nadia_character/assets/nadia_companions_v3_canonical_ingame.png`       |
| 眼镜近景   | `output/nadia_character/assets/portraits/nadia_portrait_study_01_observer.png` |

---

### 4.1 试片参考图优先级

当前采用“公开 canonical 一致性优先”，而不是让文字身份锁覆盖所有现有图的细节。人物、双猫关系和机制图的职责分开：

| 层级 | 参考图                                                              | 用法                                             | 不应承担的职责                  |
| ---- | ------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------- |
| 1    | `nadia_character_v3_canonical.png`                                  | 人物脸、发型、眼镜、服装比例与整体轮廓           | 不单独决定双猫动作              |
| 2    | `nadia_companions_v3_canonical_ingame.png`                          | 两只猫同时出现时的体型差、相处关系与室内生活质感 | 不直接当雪原战斗场景            |
| 3    | `nadia_pusha_v1_ingame.png` / `nadia_igla_v1_ingame.png`            | 当某一只猫是镜头主角时校正体型、毛色和眼睛       | 不把单猫背景复制进最终场景      |
| 4    | `nadia_splash_v4_canonical_refined.png`                             | V01 的宣传光线、雪原与观测站氛围                 | 不覆盖人物主参考的细节          |
| 5    | `nadia_action_v2_ingame.png` / `nadia_field_notebook_v1_ingame.png` | V03 的游戏内光线、记录册和战斗道具语言           | 不作为 K04/K05 的同一机位首尾帧 |
| 6    | `nadia_h_zero_v1_ingame.png`                                        | 只借测量盘、中心零点和对称结构的图形语义         | 不直接作为人物场景或视频首尾帧  |

首批关键帧基线只使用以下组合，出现身份错误时按层级逐项补图，不一次加入全部参考：

- K01：`nadia_character_v3_canonical.png` + `nadia_splash_v4_canonical_refined.png` + `nadia_companions_v3_canonical_ingame.png`。
- K04：`nadia_character_v3_canonical.png` + `nadia_field_notebook_v1_ingame.png` + `nadia_action_v2_ingame.png`。
- K05：`nadia_character_v3_canonical.png` + `nadia_companions_v3_canonical_ingame.png` + `nadia_balance_v1_ingame.png`；`nadia_h_zero_v1_ingame.png` 仅在零点结构不清楚时作为补充图形参考。

关键帧生成阶段可以使用这些参考图；视频阶段只上传选定的首帧或首尾帧，避免把室内、宣传和机制插画的构图要求同时交给视频模型。

### K01 · V01 首帧 · 登场

- 文件：`nadia_video_k01_v01_intro_start_refined.png`
- 参考：splash_v4、character_v3、pusha、igla
- 风格：宣传风
- 验收：16:9 里仍能同时看见她、左上普莎、右下伊嘉；眼镜在；不是竖图裁切。

**中文构图**

16:9 横版电影构图。寒冷北境雪原黄昏，被雪盖住的旧观测设施远景轮廓。成年女性调查员站在画面中央略偏右，身体微侧，一手扶打开的记录册，另一手让三层测量环浮在身侧。指针停在零点附近，却并未真正重合。左上：圆润奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、佩戴银蓝色空心长命锁）缓缓离地，四爪微张，雪粒反向上升。右下：修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）立在薄冰上，触地点细密冰裂。巨大半透明双环测量结构在人物身后，不要淹没人物。轻微笑意，风扬起黑发。高密度体积光与冰晶，但仍是同一套服装。无文字。

**English**

Cinematic 16:9 stylized anime game splash-art widescreen. Cold northern snowfield at dusk, faint snow-buried observatory on the horizon. An adult female surveyor stands center-right in a slight three-quarter pose, holding an open field notebook with three measuring rings floating nearby. Huge translucent dual rings behind her, pointer near but not on zero. Upper left: the round cream-gold long-haired cat with a white chest and paws, round amber eyes, and a hollow silver-blue lock charm, drifting off the snow with rising snowflakes. Lower right: the slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone, standing on thin ice with hairline cracks. Soft closed-mouth smile, wind in dark hair. Painterly refined lighting, not photoreal. No text.

---

### K01E · V01 尾帧 · 稳定落版

- 文件：`nadia_video_k01_v01_intro_end_v2_1920x1080.png`
- 来源：以 K01 为唯一编辑目标的保守编辑；当前采用自然动作 v2，保持同一场景、机位、镜头尺度和人物/双猫位置。
- 验收：普莎下落着地、伊嘉抬爪转头；人物脸、眼镜、双猫和双脚同时可见；测量环是低亮度次要配饰；无腰部特写、文字或 UI。

---

### K02 · V02 首帧 · 普攻起手

- 文件：`nadia_video_k02_v02_na_start_ingame.png`
- 参考：action_v2_ingame、character_v3
- 风格：游戏内
- 验收：记录册未展开攻击、环在胸前待机；两猫在背景，未入盘；看不见 H 读数。

**中文构图**

16:9 游戏内战斗镜头，近中景。雪原浅色冰面，无 UI。成年女性调查员正面略偏左，拇指压住合着的记录册书脊，三层测量环收在胸前尚未翻出。表情专注。圆润奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、佩戴银蓝色空心长命锁）和修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）在人物身后左右远处站着，不漂、不压冰。光线平实，克制。无文字。

**English**

16:9 in-game mid shot with clear, restrained game lighting. An adult female surveyor keeps her thumb on the spine of a still-closed field notebook; measuring rings are idle at her chest. The round cream-gold long-haired cat with a white chest and paws and the slim ivory short-haired cat with faint warm points on the ears, nose, and tail stand far behind her, not on discs and not floating. No UI, no attack VFX yet.

---

### K03 · V02 尾帧 · 普攻第四段

- 文件：`nadia_video_k03_v02_na_end_ingame.png`
- 参考：同 K02，必须同一机位
- 验收：合册再展开后的冰面折光；两猫看向中心；仍无 H 刻度、猫不入盘。

**中文构图**

与已上传的起始参考帧保持同一机位、同一角色比例。成年女性调查员正面中景，记录册刚合上半册再展开，测量环在胸前闭合成一轮。身前大一块冰面折光，像一页冰晶书页碎成光。圆润奶油金长毛猫与修长象牙色短毛猫同时转头看向画面中心，仍站在地面，不触发任何额外响应。无 UI、无数字。

**English**

Use the same camera and character scale as the provided starting reference frame. An adult female surveyor half-closes then opens the notebook while the rings close at her chest. A larger ice-page refraction bursts in front of her. The round cream-gold long-haired cat and the slim ivory short-haired cat both look toward the center, still on the ground. No balance meter, no UI.

---

### K04 · V03 首帧 · 战技起手

- 文件：`tmp/video_stills/nadia_video_k04_v03_skill_start_v3_1920x1080.png`
- 参考：action_v2_ingame、catalyst / field_notebook
- 风格：游戏内；起手特效克制
- 验收：近景是书扣，读数空白；背景是与尾帧连续的柱廊内景；扣锁只有细冷光、短弧和少量霜粒；猫不在画内或仅在画外边缘。

**中文构图**

16:9 近景。镜头顶在记录册金属扣锁上，她的手刚要打开。书页中央冰蓝读数位置还是空白，没有 0、没有正负。扣锁接缝沿一条极细的冰蓝冷光亮起，扣锁附近漂浮少量细小霜粒；书后只出现一小段不闭合、低亮度的冷光短弧，不形成完整大环；手套只接收极弱的冷色反光。背景是与尾帧连续的封闭冰晶观测厅：左右边缘可见高大的蓝灰色柱体，后方有深蓝拱形墙体、室内冰面地坪和高处冷光窗；建筑可以虚化，但必须读作室内柱廊，不能让开阔雪原、山脉或树林成为主要背景。看不到完整的两只猫。无 UI。

**English**

16:9 close-up on the metal clasp of the adult female surveyor's field notebook, her fingers about to open it. The ice-blue readout area on the page is empty, with no zero, plus sign, minus sign, or readable numbers. A very thin ice-blue glow traces the clasp seam, a few tiny frost motes hover close to it, and one short broken cold reflection appears behind the notebook without forming a complete ring. The gloves receive only a faint cool reflection. The background is the same enclosed icy observatory hall as the ending frame: softly blurred tall blue-gray columns at the sides, dark blue arched interior walls, an icy stone floor, and cool high windows. It must read as an indoor columned hall, not an open snowfield, mountain, or forest. Cats stay out of frame. No UI.

---

### K05 · V03 尾帧 · 巡衡建立

- 文件：`tmp/video_stills/nadia_video_k05_v03_skill_end_v3_1920x1080.png`
- 参考：action_v2_ingame、h_zero、pusha、igla
- 风格：游戏内；建立态冰效克制
- 验收：正面中景；左盘普莎、右盘伊嘉；三体三角清楚；三层环、中心脉冲、薄地面波纹和双盘接触闪光可辨；两盘尚未明显倾斜。

**中文构图**

16:9 正面中景，游戏内。画面必须形成稳定、可一眼读出的三体三角，而不是把三者排成同一水平线：成年女性调查员位于后方、较高的中央位置，脸和上半身是三角形上方顶点；左右测量盘位于更靠近镜头的左下和右下，略向画面中心收拢，两只猫分别成为两个下方锚点。记录册打开，三层测量环完全展开并沿边缘带低亮度冰蓝冷光。左下测量盘上坐着健康、紧凑、圆润的奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、一个银蓝色空心长命锁）；它必须有一个自然猫头、两只三角耳、清楚的小型猫口鼻、厚实蓬松的躯干、两只可见前爪、自然收拢的后腿和一条位于身体后方的尾巴，不得出现多余肢体、融合的爪子、重复的脸或变形的眼睛。右下测量盘上站着修长的象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、四肢比例自然、佩戴炭灰蓝厚项圈和哑光冰石），两只猫体型差明显。两盘几乎水平，中央冰蓝几何零点位于三锚点之间并发出一次柔和、收敛的脉冲；从中心向地面扩散一圈很薄的低透明度冰蓝波纹；双盘与猫脚接触处各有一次短促、对称的冰晶闪光，少量霜粒沿盘边漂浮。特效位于人物和猫的后方或下方，不遮挡脸、猫、记录册和三角站位。脚下各有一条细巡衡线。无技能图标、无文字 HUD、地面不添加第二本记录册；不要出现巨大光柱、爆炸或满屏雪效。

**English**

Same 16:9 enclosed columned observatory hall, camera pulled to a front mid-shot. Build a clear three-body triangle rather than a flat left-to-right row: the adult female surveyor is slightly farther back and higher in the center, with her face as the top apex; the two measuring discs sit closer to camera at lower left and lower right, angled subtly inward, with the two cats as the lower anchors. The notebook is open and the three rings are fully expanded with restrained ice-blue edge light. The healthy compact round cream-gold long-haired cat has a single natural head, two triangular ears, round amber eyes, a small cat muzzle, a thick fluffy torso, two visible front paws, tucked hind legs, a tail behind the body, lighter chest and paws, and one hollow silver-blue lock charm; no extra limbs, fused paws, duplicated face, or distorted eyes. The slim ivory short-haired cat has faint warm points on its ears, nose, and tail, ice-blue eyes, naturally proportioned legs, and one charcoal-blue collar with a matte ice stone. The cats' body types must be clearly different. Discs stay almost level. Place a small geometric ice-blue center mark between the three anchors and give it one soft contained pulse, with one thin low-opacity circular ice ripple spreading across the floor beneath the triangle. Add one brief symmetrical ice-crystal contact glint at each cat's disc, plus a few tiny frost motes near the disc edges. Keep all effects behind or beneath the faces, cats, notebook, and triangle. Keep the columned interior as the main setting and do not add a second notebook on the floor. No giant ring, beam, explosion, full-screen snowstorm, UI chrome, or readable text.

---

### K06 · V04 首帧 · 轻相起势

- 文件：`tmp/video_stills/nadia_video_k06_v04_light_start_1920x1080.png`
- 状态：已视觉确认
- 参考：character_v3、pusha、h_light；`action_v2_ingame` 仅在室内背景漂移时补充
- 风格：游戏内；向上轻相
- 验收：封闭柱廊内景；圆润奶油金长毛猫仍在左盘，四爪接近盘面、只留几厘米气流间隙；修长象牙色短毛猫仍在右盘。

**中文构图**

16:9 横版游戏内中景，略偏左构图。场景是封闭冰晶观测厅，左右有高大的蓝灰色柱体，后方是深蓝拱形墙体和冰面地坪。圆润奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、佩戴银蓝色空心长命锁）仍在左侧测量盘上，耳朵刚开始动，四爪接近盘面，只留几厘米气流间隙，身体没有明显悬空。只出现稀疏的上行冰粒，不出现完整冰弧或运动模糊。成年女性调查员在中景右侧，记录册仍打开，表情平静。修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）仍在右侧盘上低头看着，尚未跳跃。前方有两三块淡冰蓝晶体剪影作为静止目标，不是怪物角色。无 UI、无文字。

**English**

16:9 landscape in-game mid-shot, weighted left. Use the enclosed blue ice observatory hall with tall blue-gray columns, a dark arched interior, and an icy floor. The round cream-gold long-haired cat with a white chest and paws, round amber eyes, and a hollow silver-blue lock charm remains on the left disc; its ears have just begun to move, all four paws stay close to the pan with only a few centimeters of air at most, and the body is not visibly airborne. Only sparse upward ice motes are present; no completed ice arc and no motion blur. The adult female surveyor is mid-right, calm, notebook open. The slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone remains on the right disc, watching without jumping. A few abstract ice-crystal silhouettes are stationary targets, not creatures. No UI, no readable text.

---

### K07 · V04 尾帧 · 轻相命中

- 文件：`tmp/video_stills/nadia_video_k07_v04_light_end_1920x1080.png`
- 状态：已视觉确认
- 参考：同 K06，同一机位
- 风格：游戏内；向上轻相
- 验收：与 K06 为同一封闭柱廊和锁定机位；圆润奶油金长毛猫在目标群上方短暂停住；目标晶体边缘有小型冰蓝闪光；上行开口弧未完全闭合；雪粒向上；不是爆炸。

**中文构图**

与提供的起始参考帧保持同一锁定机位和同一封闭冰晶观测厅。圆润奶油金长毛猫被风托在淡冰蓝晶体剪影上方，四爪微张，圆身体仍显得很重，却明显失重。一条由下向上的开口冰弧只长到一半，末端指向中心；雪粒和碎冰反常上升，目标晶体边缘出现小型冰蓝闪光但不爆炸。成年女性调查员仍在右侧中景，修长象牙色短毛猫仍在右盘。无击飞、无大冲击波、无 UI、无文字。

**English**

Use the same locked camera and the same enclosed blue ice observatory hall as the provided starting reference frame. The round cream-gold long-haired cat hovers above a few abstract ice-crystal silhouettes, its round body visibly in low gravity. A sparse upward ice arc is only half closed and points inward; snow and ice motes rise. Add a small ice-blue glint along the edges of the crystal silhouettes, without an explosion. The adult female surveyor remains mid-right, and the slim ivory short-haired cat remains on the right disc. No large shockwave, no UI, no readable text.

---

### K08 · V05 首帧 · 重相起势

- 文件：`tmp/video_stills/nadia_video_k08_v05_heavy_start_v3_1920x1080.png`
- 状态：已视觉确认
- 参考：character_v3、igla、h_heavy；`action_v2_ingame` 仅在室内背景漂移时补充
- 风格：游戏内；向下重相
- 验收：封闭柱廊内景；修长象牙色短毛猫在右盘上端正正坐，前爪自然并拢，尚未起跳；地面只有预加载细竖线；圆润奶油金长毛猫仍在左盘，保持温和、亲和、好奇的圆眼表情，不显严肃。

**中文构图**

16:9 横版游戏内中景，略偏右构图。场景是封闭冰晶观测厅，左右有高大的蓝灰色柱体，后方是深蓝拱形墙体和冰面地坪。修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）在右侧测量盘上端正正坐，后臀落在盘面，躯干直立，前爪自然并拢，尾巴在身侧自然弯曲；它处于起跳前的等待状态，不收身、不蓄力。目标脚下只有一条尚未闭合的淡冰裂竖线。成年女性调查员在中景左侧，记录册打开。圆润奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、佩戴银蓝色空心长命锁）仍在左盘；它保持温和、亲和、好奇的圆眼表情，嘴角自然放松，不是严肃守卫神态。无巨大冲击波、无爆炸、无 UI、无文字。

**English**

16:9 landscape in-game mid-shot, weighted right. Use the enclosed blue ice observatory hall with tall blue-gray columns, a dark arched interior, and an icy floor. The slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone sits upright and squarely on the right disc, hindquarters resting on the pan, torso vertical, front paws naturally together, tail curved beside the body. It is waiting before the leap, not crouching, coiling, standing, or already jumping. Beneath a few stationary abstract ice-crystal targets, show only one faint unclosed vertical ice line. The adult female surveyor is mid-left with the notebook open. The round cream-gold long-haired cat with a white chest and paws, round open amber eyes, a soft friendly curious expression, a relaxed small cat mouth, and a hollow silver-blue lock charm remains on the left disc; it is not a stern guardian. No large shockwave, no explosion, no UI, no readable text.

---

### K09 · V05 尾帧 · 重相落点

- 文件：`tmp/video_stills/nadia_video_k09_v05_heavy_end_v9_1920x1080.png`
- 状态：已视觉确认
- 参考：同 K08，同一机位，允许镜头比 K08 再下压约 8°
- 风格：游戏内；向下重相
- 验收：与 K08 为同一封闭柱廊；人物、胖猫、测量装置和整体色调以 K08 为准；修长象牙色短毛猫以前爪先落地，一只前爪触冰、另一只尚未完全落下；冰裂沿地面向外；无重复猫影或人物头发上的孤立亮点。

**本次生图提示词（唯一参考图）**

```text
以这张输入图为唯一基准，生成同一场景的连续尾帧。保持原图的整体色调、画风、构图、镜头、人物形象和所有未提及内容不变。只改变以下三项：

1. 人物动作：记录册保持打开；人物一只戴手套的食指轻轻触在书页上，像是在做记录，另一只手托住记录册。动作自然、幅度很小，人物站位和身份不变。
2. 瘦猫位置：将右侧测量盘上的修长象牙色短毛猫移动到画面右下方的前景冰面，保持同一只猫、同一张脸、同一项圈和胸前吊坠；以前爪先落地，一只前爪刚触冰，另一只前爪略微抬起，身体处于自然落地过渡。右侧测量盘不再保留这只猫。
3. 地面裂痕：在瘦猫前爪接触冰面的位置生成紧凑、自然向外扩散的冰裂，中心有一个小而收敛的金色重心点。

只输出一张 16:9 横版游戏内画面。
```

---

### K10 · V06 首帧 · 爆发起手

- 文件：`tmp/video_stills/nadia_video_k10_v06_q_start_ingame_1920x1080.png`
- 状态：已生成，初步视觉检查通过（待视频连续性验证）
- 参考：K08 v3 仅借室内蓝冰观测厅与色调；`nadia_character_v3_canonical.png` 借人物身份；`nadia_field_notebook_v1_ingame.png` 借记录册道具
- 风格：游戏内
- 验收：记录册已打开、眼镜有受控冰蓝反光；两只猫仍在地面；尚未出现完整大环或测量盘承托状态。

**中文构图**

16:9 中全景。先看见成年女性调查员的暖银圆框眼镜里的一点冰蓝反光，记录册在胸前刚打开，页面空白读数将亮。三层腰侧测量环开始自行校到同一轴线。圆润奶油金长毛猫和修长象牙色短毛猫在人物两侧地面上，还没有跳上测量盘。封闭蓝冰柱廊背景清楚、特效少。无 UI、无大法阵。

**English**

16:9 medium-wide full-body shot. Ice-blue glint in the adult female surveyor's round glasses, notebook opening, waist rings aligning to one axis. The round cream-gold long-haired cat and the slim ivory short-haired cat are still on the ground beside her, not on discs yet. Quiet enclosed blue-ice column hall. No giant ritual circle yet, no UI.

---

### K11 · V06 尾帧 · 零点测区锁定

- 文件：`tmp/video_stills/nadia_video_k11_v06_q_end_ingame_1920x1080.png`
- 状态：已生成，初步视觉检查通过（待视频连续性验证）
- 参考：K10 作为唯一场景与人物/猫连续性基准；`nadia_h_zero_v1_ingame.png` 只借测量环与锚点几何
- 验收：左右盘分别承托两只猫；巨大冰蓝环已锁定；三个锚点清楚；人物位于中央且保持冷静。盘面高低变化交给视频运动完成。

**中文构图**

16:9 略俯视的中全景，游戏内。成年女性调查员站在中央，抬眼，记录册打开。左侧测量盘承托圆润奶油金长毛猫，右侧测量盘承托修长象牙色短毛猫；两只猫都完整可见，左右盘清楚分开并有轻微高低差。巨大冰蓝测量圆环锁定战场一圈，三点锚点分别对应圆润奶油金长毛猫、人物、修长象牙色短毛猫，不要写成中文标签；可用三枚不同形状的冰蓝几何标记。人物表情绝对冷静。不要满屏雪雾，不要把猫收进书里。无 UI 血条。

**English**

16:9 slight high-angle full mid-shot. The adult female surveyor stands at center, looking up, notebook open. The left disc supports the round cream-gold long-haired cat and the right disc supports the slim ivory short-haired cat; both cats remain fully visible, the discs are clearly separated with a slight height difference. A huge ice-blue measuring ring locks a circular field. Three geometric anchor marks for the two cats and the surveyor. Calm face. No white-out blizzard, cats are not absorbed into the book.

---

### K12 · V07 首帧 · 风起之前

- 文件：`tmp/video_stills/nadia_video_k12_v07_wind_start_ingame_1920x1080.png`
- 状态：已生成，初步视觉检查通过（空心锁已做局部修正，待视频连续性验证）
- 参考：K01 仅借室外观测站、雪台、远景和光色；`nadia_character_v3_canonical.png` 借人物身份；猫使用文字外观锁，避免单猫参考引入不同饰品
- 风格：游戏内日常
- 验收：她在写；圆猫四爪着地且胸前空心锁可见；瘦猫在右后方行走；像生活，不像战斗。

**中文构图**

16:9 日常中景。寒冷北境观测站外的雪台，不是战场。成年女性调查员低头写记录册，测量环收着当腰饰。圆润奶油金长毛猫坐在她脚边的雪上，完全着地。修长象牙色短毛猫在画面右后，若无其事走来。风还很小。没有战斗特效、没有测量盘。身后门缝漏出一点室内暖光。无文字。

**English**

16:9 daily mid-shot on a snowy northern observatory terrace, not a battlefield. An adult female surveyor writes in her notebook, rings idle at her waist. The round cream-gold long-haired cat sits fully on the snow at her feet. The slim ivory short-haired cat walks in from the right rear. Light wind only. No combat VFX, no discs. Soft interior light from a doorway. No text.

---

### K13 · V07 尾帧 · 抓住普莎

- 文件：`tmp/video_stills/nadia_video_k13_v07_wind_end_ingame_v4_1920x1080.png`
- 状态：v4 已生成，初步视觉检查通过（人物停笔看普莎；记录册夹在腋下；待视频连续性验证）
- 参考：K12 作为唯一首帧基准，同一机位与光色
- 验收：普莎离地；她头不抬但眼睛看普莎；记录册被夹住、笔已收起；另一只手抓住细牵引绳；伊嘉朝她走，她还没去抱伊嘉。

**中文构图**

与提供的起始参考帧保持同一机位。一阵明显的雪风。圆润奶油金长毛猫的圆身体离开地面约一个身位，四爪微张，长命锁和一根极细安全牵引绳被扯直。成年女性调查员头部仍略低，但眼睛看向浮起的圆猫；她已经停笔，记录册合上并夹在非持绳侧的腋下与前臂、胸口之间，另一只手抓住绳子，表情平静。修长象牙色短毛猫走到她膝侧，像也想跳进怀里。无战斗特效。无文字。

**English**

Use the same camera as the provided starting reference frame. Stronger gust. The round cream-gold long-haired cat floats a body-length off the terrace, lock-charm and a thin safety leash taut. The adult female surveyor keeps her head slightly lowered but looks at the floating cat, not at her notes. She has stopped writing; the closed notebook is clamped under the upper arm on the side opposite the leash hand, pressed between arm and chest, with the pen tucked inside. Her other hand holds the leash, calm. The slim ivory short-haired cat has reached her knee, about to jump into her arms. No combat VFX.

---

### K14 · V08 首帧 · 单手去抱

- 文件：`tmp/video_stills/nadia_video_k14_v08_hug_start_ingame_1920x1080.png`
- 状态：已生成，初步视觉检查通过（待视频连续性验证）
- 参考：K12 借既定色调与猫的身份关系；`nadia_character_v3_canonical.png` 借人物身份；不再上传冲突的单猫参考图
- 风格：游戏内日常
- 验收：瘦猫在脚边；她自然弯腰、一只手伸向它；另一只手拿记录册；还没有吃力。

**中文构图**

16:9 日常中近景，观测站廊下。修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）走到成年女性调查员脚边，抬头。她正自然弯腰，准备单手抄起它，另一手还拿着记录册。表情轻松。地面木板只有极淡的下陷暗示。圆润奶油金长毛猫在背景里趴着。无特效爆炸。无文字。

**English**

16:9 daily close-mid under an observatory eaves. The slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone is at the adult female surveyor's feet, looking up. The surveyor bends, one hand reaching to scoop the cat, notebook still in the other, relaxed. Faint wood-board dip. The round cream-gold long-haired cat loafs in the background. No VFX burst.

---

### K15 · V08 尾帧 · 改成双手

- 文件：`tmp/video_stills/nadia_video_k15_v08_hug_end_ingame_1920x1080.png`
- 状态：已生成，初步视觉检查通过（待视频连续性验证）
- 参考：K14 作为唯一首帧基准，同一机位与檐下场景
- 验收：双手抱着伊嘉；她微微绷劲、眼镜可能滑一点；伊嘉若无其事；普莎仍坐在背景垫子上，不离地。

**中文构图**

与提供的起始参考帧保持同一机位。成年女性调查员已经改成双手抱起修长象牙色短毛猫，记录册夹在臂下或抵着肩。她表情微僵，肩背用力，圆框眼镜下滑一点点。修长象牙色短毛猫被抱着却很轻松，冰蓝眼睛看着镜头外。木板明显下陷一毫米级的裂缝。背景圆润奶油金长毛猫仍坐在垫子上。无字幕、无漫画汗滴。

**English**

Use the same camera as the provided starting reference frame. The adult female surveyor now holds the slim ivory short-haired cat with both hands, notebook tucked. Slight strain in her shoulders, glasses slipped a millimeter. The cat looks unbothered. The wooden board dips. The round cream-gold long-haired cat remains seated on the mat in the background. No sweat-drop cartoon marks, no text.

---

## 5. Seedance 视频规格

提交给模型的完整提示词、粘贴说明、提示词版本号、验收门和生成记录只维护在 [`docs/nadia_video_pilot.md`](nadia_video_pilot.md) §4–§7。本节只保留共用参数、对白叠轨和镜头意图，不再复制粘贴块。

### 5.1 每条共用参数

| 参数           | 试片值                                                                              |
| -------------- | ----------------------------------------------------------------------------------- |
| 模型           | Seedance 2.0；优先标准模型，实际入口名称按界面记录                                  |
| ratio          | `16:9`                                                                              |
| duration       | V01/V03/V08 各 `6s`；V07 `8s`；V04/V05 各 `5s`；V06 不生成视频                         |
| generate_audio | `true`；只允许环境音与动作音效，不允许对白                                          |
| resolution     | `720p`；试片通过后才切换 `1080p`                                                    |
| watermark      | V01、V03–V05 均实测有“AI生成”；V07/V08 保留源文件状态，仍如实记录提交页状态          |

`camera_fixed` 不是本项目已经确认的必填控制项。V01 的固定中远景、V03 的一次拉远写进提示词；实际界面若有镜头开关，必须把真实值写入生成记录。

声音提示词一律加上：

> 只有环境音和动作音效。禁止任何语言、对人说话、旁白、歌唱、字幕。

视频负面：

> 变形五官、眼镜消失、发长突变、猫耳、第三只猫、把两只猫融成一只、UI、文字、伤害数字、队友、镜头乱切、把猫吸进书里。

**模型提示词清洁规则**：执行单中可直接提交给图像/视频模型的文本，只使用可视身份、构图、镜头、动作、时序、声音和必要约束；不使用人物名、猫名、技能名、镜头编号、本地文件名、内部变量或无视觉意义的项目叙事。项目名称仅保留在人类索引、资产文件名、验收标签和角色对白中。

### 5.2 对白不要让模型说

即使开了声音，也不要在视频提示词里写台词。后期从 `output/nadia_character/assets/audio/` 叠：

| 镜头 | MP3                                                                            |
| ---- | ------------------------------------------------------------------------------ |
| V01  | `nadia_voice_01_greeting.mp3`                                                  |
| V07  | `nadia_voice_03_wind.mp3`                                                      |
| V08  | `nadia_voice_05_heavy_hug.mp3`                                                 |
| V03  | `nadia_voice_06_skill.mp3`                                                     |
| V04  | `nadia_voice_07_light_phase.mp3`                                               |
| V05  | `nadia_voice_08_heavy_phase.mp3`                                               |
| V06（已放弃） | `nadia_voice_10_burst_start.mp3`、`nadia_voice_11_burst_end.mp3`（不使用） |

对白出现时把生成轨压低 8–12 dB。

### 5.3 各镜头意图

提交时只复制执行单对应章节，不要从本表扩写。

| ID  | 参数                         | 运动意图                                                           | 提交文本                            |
| --- | ---------------------------- | ------------------------------------------------------------------ | ----------------------------------- |
| V01 | 6s，固定中远景，K01→K01E     | 圆猫下落着地，瘦猫抬爪转头；人物、双猫和双脚始终同框               | [执行单 §4.2](nadia_video_pilot.md) |
| V02 | 6s，固定机位，K02→K03        | 四段普攻，猫不入盘；本批不进 PV                                    | 本批不提交                          |
| V03 | 6s，一次拉远，K04→K05        | 扣锁近景拉到正面中景，双猫入盘，落成三体三角                       | [执行单 §4.3](nadia_video_pilot.md) |
| V04 | 5s，固定机位，K06→K07        | 圆猫被气流托起约半个身位，开口冰弧不过半                           | [执行单 §4.4](nadia_video_pilot.md) |
| V05 | 5s，起跳后下压约 8°，K08→K09 | 瘦猫从右盘跳到右下前景并落定正坐，地面开裂                         | [执行单 §4.5](nadia_video_pilot.md) |
| V06 | 已放弃视频，K10→K11          | 不再提交视频；K10/K11 仅作为 BOARD 06 静态动作板参考                | 不执行                            |
| V07 | 8s，固定机位，K12→K13        | 风力增强，人物看猫、停笔并夹住记录册，取出并扣上牵引绳后抓稳；圆猫离地；人物和两只猫自然眨眼 | [执行单 §4.7](nadia_video_pilot.md) |
| V08 | 6s，固定机位，K14→K15        | 单手改双手抱起瘦猫，哈出白雾；背景圆猫坐着只眨眼；廊下可见飘雪     | [执行单 §4.8](nadia_video_pilot.md) |

---

## 6. 叙事 PV 剪辑（当前约 42 秒；后续可扩展）

成片文件建议：`output/nadia_character/assets/video/nadia_video_pv_between_two_weights_v1.mp4`，16:9 1080p。

| 时间（约） | 画面                      | 对白入点                                                 |
| ---------- | ------------------------- | -------------------------------------------------------- |
| 0:00–0:06  | V01                       | 01「你好。娜蒂娅……」                                     |
| 0:06–0:14  | V07                       | 03「风向变了。普莎，回来。」                             |
| 0:14–0:20  | V08                       | 05「今天也是稳定状态。」                                 |
| 0:20–0:26  | V03                       | 06「普莎，伊嘉——开始记录。」                             |
| 0:26–0:31  | V04                       | 07「轻端响应。普莎，慢一点。」                           |
| 0:31–0:36  | V05                       | 08「重端响应。伊嘉，落点确认。」                         |
| 0:36–0:42  | 可回切 V01 最后一拍作静帧 | 无，或留风声；V05 余韵可延长至片尾                         |

硬切或 8–12 帧叠化。不要加标题卡字幕抢过角色。片尾若需要一行字，后期单独排：`娜蒂娅「两衡之间」`，不要让 Seedance 烧字。

V02 普攻不进 PV，只挂技能页；V06 视频已放弃，不进入 PV。

---

## 7. HTML 挂载（当前 720p 试片已落地）

| 镜头     | 建议位置                                                                            |
| -------- | ----------------------------------------------------------------------------------- |
| V01      | `index.html` hero：视频播放器，K01 首帧作 poster，原 splash 静图作浏览器回退          |
| V07、V08 | `index.html` `#companions` 下方的成对“生活片段”区                                |
| V03–V05  | `skills.html` `#boards` 的 BOARD 02–04：关键帧作 poster，原静态参考图与视频并列保留  |
| V02、V06  | 不挂视频；BOARD 01、06 保留静态动作板；BOARD 05 本批不做视频                   |
| PV       | `index.html` 导航增加「介绍影像」，或档案页底部单独一节；不要放进明信片页           |

`<video>` 使用 `controls`、`playsinline`、`preload="none"`、`poster` 指向对应关键帧；不设置 `muted`，用户点播放时默认保留视频声音。当前不自动播放、不循环，避免一进页就六条声轨；浏览器策略也可能阻止未经用户操作的有声自动播放。

公开包目录：

```text
output/nadia_character/assets/video/
  stills/
  nadia_video_v01_intro_720p_a01.mp4
  nadia_video_v03_skill_720p_a01.mp4
  nadia_video_v04_light_720p_a01.mp4
  nadia_video_v05_heavy_720p_a01.mp4
  nadia_video_v07_wind_720p_a01.mp4
  nadia_video_v08_hug_720p_a01.mp4
  nadia_video_pv_between_two_weights_v1.mp4
```

`tools/nadia_skill_simulator.html` 仍然不进分享包。

---

## 8. 验收

身份（任一条失败即重出关键帧，不要先烧 1080p 视频）：

1. 眼镜在，形状是细金属圆椭圆框。
2. 头发过肩轻波浪，不是齐腰、不是猫耳。
3. 披肩右长左短；裤子不透明；靴子平底。
4. 普莎圆、奶油金、琥珀眼；伊嘉瘦、象牙、冰蓝眼；两只同时出现时体型相反。
5. 16:9 没有裁掉边角的猫。
6. 游戏内镜头读得出轻/重/归衡方向；普攻镜头读不出 H 在动。
7. 无 UI、无字幕、无真人、无官方角色。
8. 生成音轨没有中文或英文句子。
9. 720p 试片通过后再出 1080p。

---

## 9. 第二批（明确不做）

归衡校读、待机「再次测量 / 猫毛」、传说「稳定现在」、Q 十二秒场地循环、料理、生日、竖屏、假队伍实战。

---

## 10. 本轮执行入口

本轮不再把“只落提示词”当作最终状态。已确认的执行细节、关键帧规格、视频提示词、声音边界、验收门和生成记录模板统一放在 [`docs/nadia_video_pilot.md`](nadia_video_pilot.md)。V01、V03–V05 已有试片，V07/V08 已从 Downloads 导入；V06 视频放弃，下一步完成当前六条公开预览的技术/音频验收，再决定是否制作 1080p 与混音 PV。

### 10.1 后续视频落地计划

| 顺序 | 视频       | 关键帧与时长      | 先做什么                                             | 主要验收点                                                            |
| ---- | ---------- | ----------------- | ---------------------------------------------------- | --------------------------------------------------------------------- |
| 1    | V04 轻相   | K06→K07，5s       | 核对试片的首尾连续性与环境音，并记录提交页水印状态   | 圆猫只上浮半个身位，开口冰弧不过半，不爆炸、不变猫                    |
| 2    | V05 重相   | K08 v3→K09 v9，5s | 核对试片的正坐起跳、落地和冰裂，并记录提交页水印状态 | 瘦猫从右盘落到右下前景，落定正坐；裂纹只沿地面展开，不新增冰层/重心点 |
| —    | V06 爆发   | 视频已放弃        | 不提交；K10/K11 仅保留静态动作板                         | BOARD 06 保持静态说明，不进入视频、HTML 或 PV                         |
| 3    | V07 风     | K12→K13，8s       | 核对已导入的 Downloads 视频与 K12/K13 v4 的动作对应关系 | 人物先看普莎、停笔并夹住记录册，再取出并扣上牵引绳；普莎被风托起；人物和两只猫有自然眨眼 |
| 4    | V08 抱错了 | K14→K15，6s       | 核对已导入的 Downloads 视频与廊下日常首尾帧对应关系    | 人物由单手改双手抱伊嘉，抱起时哈出白雾；背景普莎坐着不动，只眨眼      |

执行门：V04/V05/V07/V08 先完成音频、时长、画幅、编码和画面连续性复核，并记录可见水印状态；当前六条视频已经进入 HTML 预览，不因水印单独触发重跑。完成验收后，再决定是否制作 1080p 版本、叠加 MP3，并制作 PV。

执行顺序固定为：

1. 完成 V01/V03/V04/V05/V07/V08 的音频、界面参数和 720p 技术验收；不因视觉通过自动放行 1080p。
2. K06、K07、K08 v3、K09 v9 已视觉确认，不再重出关键帧。
3. 对 `output/nadia_character/assets/video/` 的六条 MP4 完成技术/音频验收；若后续重跑，保留原记录并增加新的 `a02`，不覆盖 `a01`。
4. K10/K11 不再进入视频生成；K12–K15 只作为 V07/V08 的动作与 poster 参考。
5. 仅在身份、连续性、动作落点和音轨通过后，才复制通过项生成 1080p；当前 720p 公开副本作为 HTML 预览保留，后期与 PV 另行处理。
