# 娜蒂娅介绍视频制作规格（MVP）

> 状态：已确认的分阶段执行规格。本轮先做 V01/V03 两条 720p 试片；关键帧和视频生成通过验收后，再扩展全量镜头。
> 角色：娜蒂娅「两衡之间」
> 依赖：`docs/genshin_character_full_design.md`（身份与故事）、`docs/nadia_skill_presentation.md`（技能逐镜）、`docs/nadia_voice_script.md`（对白 MP3）、现有 canonical 静帧。
> 本轮执行单：[`docs/nadia_video_pilot.md`](nadia_video_pilot.md)

---

## 0. 当前决策基线

| 项       | 选择                                                                                                     |
| -------- | -------------------------------------------------------------------------------------------------------- |
| 去处     | HTML 分享包 + 一条横屏叙事 PV，共用同一套成片                                                            |
| 模型     | Seedance 2.0；试片优先标准模型，1080p 定稿不用 Fast（若入口提供该变体）                                  |
| 画幅     | 16:9；关键帧 1920×1080；不直接把现有 3:2 / 2:3 图当首尾帧                                                |
| 批次     | MVP 仍规划 8 条；当前先执行 V01、V03 两条试片                                                            |
| 出图本轮 | 先生成 K01、K01E、K04、K05 四张 16:9 关键帧，身份通过后再跑视频                                          |
| 视频试跑 | V01/V03 各 6s、720p；试片通过后才出 1080p                                                                |
| 声音     | 开启模型环境音/动作音效；提示词禁止模型对白；后期叠现有 MP3                                              |
| 模式     | V01 用 K01→K01E 首尾帧；V03 用 K04→K05 首尾帧。canonical 图只用于关键帧/身份参考，不写死未确认的接口参数 |
| 实战边界 | 无队友、无官方 HUD、无伤害数字；目标只用抽象冰晶剪影或画外受击                                           |
| Q        | 一条 11 秒：起手到零点测区锁定；12 秒场地循环留第二批                                                    |
| 生活     | 「风」+「抱错了」                                                                                        |
| PV       | 叙事剪辑：V01 → V07 → V08 → V03 → V04 → V05 → V06；普攻 V02 只进 HTML                                    |

隐私：禁止使用 `xiting/*.jpg` 或任何真人/真猫照片。风格参考只用仓库内已生成的 canonical PNG。

---

## 1. 阶段

| 阶段 | 产物                                                                        | 本轮         |
| ---- | --------------------------------------------------------------------------- | ------------ |
| A    | 本文总规划 + [`docs/nadia_video_pilot.md`](nadia_video_pilot.md) 试片执行单 | **做**       |
| B    | 试片关键帧 K01/K04/K05 → `tmp/video_stills/`；通过后才进入视频              | **当前做**   |
| C    | V01/V03 两条 720p 试片 → `tmp/video_trials/`                                | **当前做**   |
| D    | 全量镜头 1080p 定稿 → `output/nadia_character/assets/video/`                | 试片通过后   |
| E    | 叙事 PV 混音剪辑；HTML 挂载                                                 | 成片齐后再做 |

720p 试片不要进公开分享包。Git 已精确忽略 `tmp/video_stills/` 和 `tmp/video_trials/`。

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

两只真实家猫，不是使魔、不是元素生命、不是机械体。圆润奶油金长毛猫：胸腹与爪偏白，琥珀色圆眼，神情镇定；佩戴银蓝色空心长命锁。修长象牙色短毛猫：耳鼻尾有极淡奶茶色，冰蓝色眼睛，动作轻巧；佩戴炭灰蓝厚项圈，下面一颗哑光冰石。两只猫体型必须明显不同，禁止画成一对双胞胎或一只双头猫。提交给模型的提示词只使用这些外观、饰品和位置描述，不使用项目专有名。

### 2.2 Identity lock (English, for GPT Image)

Stylized anime game adult female ice-field surveyor, mid-20s impression, 162 cm impression. Dark wavy hair just past the shoulders, tapered ends, slightly asymmetrical bangs. Thin warm-silver oval-round glasses, no glasses chain. Dual-ring hair clip: one ring with a tiny silver-white feather, one with a small dark metal weight. Asymmetric short survey cloak, longer on her right, shorter on her left, graphite-blue, thin fleece trim, not a fur collar. Cream high-collar inner layer, fitted dark gray-blue coat, no cleavage. Opaque matte slate-blue winter leggings, no stockings, no translucency. Flat practical mid-calf boots, not heels. Three-layer ice-blue measuring rings at the left-rear waist. Gentle intellectual expression, almost no teeth. Not a loli, not an icy queen, not a catgirl.

Two real house cats, not familiars. One is a round cream-gold long-haired cat with a white chest and paws, round amber eyes, and a hollow silver-blue lock charm. The other is a slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone. They must remain two distinct cats. In model prompts, use these visual, accessory, and position descriptions instead of project-specific names.

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
| V06 | 爆发起手→锁环    | 首尾帧        | 11s  | 游戏内     | K10→K11  | BOARD 06                               | 高潮     | 语音 10、11 |
| V07 | 生活「风」       | 首尾帧        | 6s   | 游戏内日常 | K12→K13  | `index.html` `#companions` 或 `#voice` | 开场后   | 语音 03     |
| V08 | 生活「抱错了」   | 首尾帧        | 6s   | 游戏内日常 | K14→K15  | 同上                                   | 紧接 V07 | 语音 05     |

BOARD 05 归衡校读本批不做视频。

建议成片文件名：

```text
output/nadia_character/assets/video/stills/nadia_video_k01_v01_intro_start_refined.png
output/nadia_character/assets/video/nadia_video_v01_intro_1080p.mp4
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

- 文件：`tmp/video_stills/nadia_video_k04_v03_skill_start_v2_1920x1080.png`
- 参考：action_v2_ingame、catalyst / field_notebook
- 风格：游戏内
- 验收：近景是书扣，读数空白；背景是与尾帧连续的柱廊内景；猫不在画内或仅在画外边缘。

**中文构图**

16:9 近景。镜头顶在记录册金属扣锁上，她的手刚要打开。书页中央冰蓝读数位置还是空白，没有 0、没有正负。背景是与尾帧连续的封闭冰晶观测厅：左右边缘可见高大的蓝灰色柱体，后方有深蓝拱形墙体、室内冰面地坪和高处冷光窗；建筑可以虚化，但必须读作室内柱廊，不能让开阔雪原、山脉或树林成为主要背景。看不到完整的两只猫。无 UI。

**English**

16:9 close-up on the metal clasp of the adult female surveyor's field notebook, her fingers about to open it. The ice-blue readout area on the page is empty, with no zero, plus sign, minus sign, or readable numbers. The background is the same enclosed icy observatory hall as the ending frame: softly blurred tall blue-gray columns at the sides, dark blue arched interior walls, an icy stone floor, and cool high windows. It must read as an indoor columned hall, not an open snowfield, mountain, or forest. Cats stay out of frame. No UI.

---

### K05 · V03 尾帧 · 巡衡建立

- 文件：`tmp/video_stills/nadia_video_k05_v03_skill_end_v2_1920x1080.png`
- 参考：action_v2_ingame、h_zero、pusha、igla
- 验收：正面中景；左盘普莎、右盘伊嘉；中央可读的归衡 0；两盘尚未明显倾斜。

**中文构图**

16:9 正面中景，游戏内。画面必须形成稳定、可一眼读出的三体三角，而不是把三者排成同一水平线：成年女性调查员位于后方、较高的中央位置，脸和上半身是三角形上方顶点；左右测量盘位于更靠近镜头的左下和右下，略向画面中心收拢，两只猫分别成为两个下方锚点。记录册打开，三层测量环展开。左下测量盘上坐着健康、紧凑、圆润的奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、一个银蓝色空心长命锁）；它必须有一个自然猫头、两只三角耳、清楚的小型猫口鼻、厚实蓬松的躯干、两只可见前爪、自然收拢的后腿和一条位于身体后方的尾巴，不得出现多余肢体、融合的爪子、重复的脸或变形的眼睛。右下测量盘上站着修长的象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、四肢比例自然、佩戴炭灰蓝厚项圈和哑光冰石），两只猫体型差明显。两盘几乎水平，中央冰蓝几何方标位于三锚点之间，不写成可读的 HUD 数字或中文；脚下各有一条细巡衡线。无技能图标、无文字 HUD、地面不添加第二本记录册。

**English**

Same 16:9 enclosed columned observatory hall, camera pulled to a front mid-shot. Build a clear three-body triangle rather than a flat left-to-right row: the adult female surveyor is slightly farther back and higher in the center, with her face as the top apex; the two measuring discs sit closer to camera at lower left and lower right, angled subtly inward, with the two cats as the lower anchors. The notebook is open and the three rings are expanded. The healthy compact round cream-gold long-haired cat has a single natural head, two triangular ears, round amber eyes, a small cat muzzle, a thick fluffy torso, two visible front paws, tucked hind legs, a tail behind the body, lighter chest and paws, and one hollow silver-blue lock charm; no extra limbs, fused paws, duplicated face, or distorted eyes. The slim ivory short-haired cat has faint warm points on its ears, nose, and tail, ice-blue eyes, naturally proportioned legs, and one charcoal-blue collar with a matte ice stone. The cats' body types must be clearly different. Discs stay almost level. Place a small geometric ice-blue center mark between the three anchors, not readable HUD text. Keep the columned interior as the main setting and do not add a second notebook on the floor. No UI chrome.

---

### K06 · V04 首帧 · 轻相起势

- 文件：`nadia_video_k06_v04_light_start_ingame.png`
- 参考：pusha、h_light、action_v2_ingame
- 风格：游戏内
- 验收：普莎仍在左盘，耳朵先动，身体刚离盘约半个身位；伊嘉仍在右盘。

**中文构图**

16:9，略偏左构图。圆润奶油金长毛猫（胸腹与爪偏白、琥珀色圆眼、佩戴银蓝色空心长命锁）在左侧测量盘上，耳朵先动，身体刚被风托起半个身位，爪子还挨着盘面。稀疏上行冰粒刚出现。成年女性调查员在中景右侧，记录册仍打开，表情平静。修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）在右侧盘上低头看着，尚未跳跃。前方有两三块淡冰蓝晶体剪影当目标，不是怪物角色。无 UI。

**English**

16:9, weighted left. The round cream-gold long-haired cat with a white chest and paws, round amber eyes, and a hollow silver-blue lock charm is on the left disc, ears moving first, body lifted half a body-length by wind, paws still near the disc. Sparse upward ice motes. The adult female surveyor is mid-right, calm, notebook open. The slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone remains on the right disc. A few abstract ice-crystal silhouettes as targets, not creatures. No UI.

---

### K07 · V04 尾帧 · 轻相命中

- 文件：`nadia_video_k07_v04_light_end_ingame.png`
- 参考：同 K06，同一机位
- 验收：普莎在目标群上方短暂停住；上行开口弧未完全闭合；雪粒向上；不是爆炸。

**中文构图**

与提供的起始参考帧保持同一机位。圆润奶油金长毛猫被风托在那些冰蓝晶体剪影上方，四爪微张，圆身体仍显得很重，却明显失重。一条由下向上的开口冰弧长到一半，末端指向中心。雪粒和碎冰反常上升。命中点明亮但不爆炸。成年女性调查员仍在右侧中景。修长象牙色短毛猫还在右盘。无击飞、无 UI。

**English**

Use the same camera as the provided starting reference frame. The round cream-gold long-haired cat hovers above the ice-crystal silhouettes, round body in low gravity. A half-closed upward ice arc points inward. Snow rising. Bright hit, no explosion. The adult female surveyor remains mid-right. The slim ivory short-haired cat remains on the right disc.

---

### K08 · V05 首帧 · 重相起势

- 文件：`nadia_video_k08_v05_heavy_start_ingame.png`
- 参考：igla、h_heavy、action_v2_ingame
- 风格：游戏内
- 验收：伊嘉在右盘收身欲跳；地面只有预加载细竖线；普莎仍在左盘。

**中文构图**

16:9，略偏右。修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）在右侧测量盘边收身，后腿蓄力，看起来轻巧。目标脚下出现尚未闭合的淡冰裂纹。成年女性调查员中景左侧，记录册打开。圆润奶油金长毛猫仍在左盘。无巨大冲击波。无 UI。

**English**

16:9, weighted right. The slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone coils on the right disc, about to leap, looking weightless. Faint unclosed ice cracks under abstract targets. The adult female surveyor is mid-left. The round cream-gold long-haired cat remains on the left disc. No shockwave. No UI.

---

### K09 · V05 尾帧 · 重相落点

- 文件：`nadia_video_k09_v05_heavy_end_ingame.png`
- 参考：同 K08，同一机位，允许镜头比 K08 再下压约 8°
- 验收：伊嘉已落地；冰裂沿地面向外；目标不飞起；无「砸地板」的漫画星芒。

**中文构图**

与提供的起始参考帧几乎同一机位，镜头略微下压。修长象牙色短毛猫轻巧落在冰面上，身体仍修长，但触地点冰裂向外走，像质量远超体型。下沉楔形收束成一个小的金色重心点。目标晶体剪影留在原地被压住，不飞到空中。成年女性调查员稳定站着。圆润奶油金长毛猫在左盘被震得微微浮起一点。无 UI。

**English**

Same setup as the provided starting reference frame, camera tilted down about 8 degrees. The slim ivory short-haired cat has landed lightly; ice fractures race outward, mass far beyond her slim body. Targets stay grounded, pressed, not launched. A small gold gravity point at the impact. The round cream-gold long-haired cat on the left disc lifts a centimeter. No comic impact stars, no UI.

---

### K10 · V06 首帧 · 爆发起手

- 文件：`nadia_video_k10_v06_q_start_ingame.png`
- 参考：action_v3_ingame、portrait_study_01、field_notebook
- 风格：游戏内
- 验收：以眼镜反光和记录册为主；尚未出现完整大环；猫未站上左右盘。

**中文构图**

16:9 近中景。先看见成年女性调查员的暖银圆框眼镜里的一点冰蓝反光，记录册在胸前刚打开，页面空白读数将亮。三层腰侧测量环开始自行校到同一轴线。圆润奶油金长毛猫和修长象牙色短毛猫在人物两侧地面上，还没有跳上测量盘。雪原背景实、特效少。无 UI、无大法阵。

**English**

16:9 close-mid. Ice-blue glint in the adult female surveyor's round glasses, notebook opening, waist rings aligning to one axis. The round cream-gold long-haired cat and the slim ivory short-haired cat are still on the ground beside her, not on discs yet. Quiet snowfield. No giant ritual circle yet, no UI.

---

### K11 · V06 尾帧 · 零点测区锁定

- 文件：`nadia_video_k11_v06_q_end_ingame.png`
- 参考：action_v3_ingame、h_zero、splash 只借环的几何，不借宣传风密度
- 验收：左盘明显上升且坐着普莎；右盘明显下沉且站着伊嘉；巨大冰蓝环锁定；能读到三个锚点；她在中央冷静。

**中文构图**

16:9 略俯视的中全景，游戏内。成年女性调查员站在中央，抬眼，记录册打开。左侧测量盘猛然上倾，圆润奶油金长毛猫坐在盘上却几乎没有把盘压下去。右侧测量盘明显下沉，修长象牙色短毛猫站在盘上，冰面裂开。巨大冰蓝测量圆环锁定战场一圈，三点锚点分别对应圆润奶油金长毛猫、人物、修长象牙色短毛猫，不要写成中文标签；可用三枚不同形状的冰蓝几何标记。人物表情绝对冷静。不要满屏雪雾，不要把猫收进书里。无 UI 血条。

**English**

16:9 slight high-angle full mid-shot. The adult female surveyor stands at center, looking up, notebook open. Left disc tilted upward with the round cream-gold long-haired cat sitting on it, disc barely depressed. Right disc sunk under the slim ivory short-haired cat, ice cracked. A huge ice-blue measuring ring locks a circular field. Three geometric anchor marks for the two cats and the surveyor. Calm face. No white-out blizzard, cats are not absorbed into the book.

---

### K12 · V07 首帧 · 风起之前

- 文件：`nadia_video_k12_v07_wind_start_ingame.png`
- 参考：companions_v3、character_v3、pusha、igla
- 风格：游戏内日常
- 验收：她在写；普莎四爪着地；伊嘉在附近；像生活，不像战斗。

**中文构图**

16:9 日常中景。寒冷北境观测站外的雪台，不是战场。成年女性调查员低头写记录册，测量环收着当腰饰。圆润奶油金长毛猫坐在她脚边的雪上，完全着地。修长象牙色短毛猫在画面右后，若无其事走来。风还很小。没有战斗特效、没有测量盘。身后门缝漏出一点室内暖光。无文字。

**English**

16:9 daily mid-shot on a snowy northern observatory terrace, not a battlefield. An adult female surveyor writes in her notebook, rings idle at her waist. The round cream-gold long-haired cat sits fully on the snow at her feet. The slim ivory short-haired cat walks in from the right rear. Light wind only. No combat VFX, no discs. Soft interior light from a doorway. No text.

---

### K13 · V07 尾帧 · 抓住普莎

- 文件：`nadia_video_k13_v07_wind_end_ingame.png`
- 参考：同 K12，同一机位
- 验收：普莎离地；她不抬头、另一只手抓住锁或细牵引绳；伊嘉朝她走，她还没去抱伊嘉。

**中文构图**

与提供的起始参考帧保持同一机位。一阵明显的雪风。圆润奶油金长毛猫的圆身体离开地面约一个身位，四爪微张，长命锁和一根极细安全牵引绳被扯直。成年女性调查员眼睛仍看着笔记，另一只手已经抓住绳子，表情平静。修长象牙色短毛猫走到她膝侧，像也想跳进怀里。无战斗特效。无文字。

**English**

Use the same camera as the provided starting reference frame. Stronger gust. The round cream-gold long-haired cat floats a body-length off the terrace, lock-charm and a thin safety leash taut. The adult female surveyor keeps looking at her notes, other hand already holding the leash, calm. The slim ivory short-haired cat has reached her knee, about to jump into her arms. No combat VFX.

---

### K14 · V08 首帧 · 单手去抱

- 文件：`nadia_video_k14_v08_hug_start_ingame.png`
- 参考：companions_v3、igla、character_v3
- 风格：游戏内日常
- 验收：伊嘉在脚边；她自然弯腰、一只手伸向它；还没有吃力。

**中文构图**

16:9 日常中近景，观测站廊下。修长象牙色短毛猫（耳鼻尾有极淡奶茶色、冰蓝色眼睛、佩戴炭灰蓝厚项圈和哑光冰石）走到成年女性调查员脚边，抬头。她正自然弯腰，准备单手抄起它，另一手还拿着记录册。表情轻松。地面木板只有极淡的下陷暗示。圆润奶油金长毛猫在背景里趴着。无特效爆炸。无文字。

**English**

16:9 daily close-mid under an observatory eaves. The slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone is at the adult female surveyor's feet, looking up. The surveyor bends, one hand reaching to scoop the cat, notebook still in the other, relaxed. Faint wood-board dip. The round cream-gold long-haired cat loafs in the background. No VFX burst.

---

### K15 · V08 尾帧 · 改成双手

- 文件：`nadia_video_k15_v08_hug_end_ingame.png`
- 参考：同 K14，同一机位
- 验收：双手抱着伊嘉；她微微绷劲、眼镜可能滑一点；伊嘉若无其事；普莎仍很轻地待在背景。

**中文构图**

与提供的起始参考帧保持同一机位。成年女性调查员已经改成双手抱起修长象牙色短毛猫，记录册夹在臂下或抵着肩。她表情微僵，肩背用力，圆框眼镜下滑一点点。修长象牙色短毛猫被抱着却很轻松，冰蓝眼睛看着镜头外。木板明显下陷一毫米级的裂缝。背景圆润奶油金长毛猫被风吹得几乎离地，对比用。无字幕、无漫画汗滴。

**English**

Use the same camera as the provided starting reference frame. The adult female surveyor now holds the slim ivory short-haired cat with both hands, notebook tucked. Slight strain in her shoulders, glasses slipped a millimeter. The cat looks unbothered. The wooden board dips. The round cream-gold long-haired cat in the background almost lifts in the breeze, for contrast. No sweat-drop cartoon marks, no text.

---

## 5. Seedance 视频提示词

### 5.1 每条共用参数

| 参数           | 试片值                                                 |
| -------------- | ------------------------------------------------------ |
| 模型           | Seedance 2.0；优先标准模型，实际入口名称按界面记录     |
| ratio          | `16:9`                                                 |
| duration       | V01/V03 各 `6s`                                        |
| generate_audio | `true`；只允许环境音与动作音效，不允许对白             |
| resolution     | `720p`；试片通过后才切换 `1080p`                       |
| watermark      | 若界面提供开关则关闭；未提供时记录实际状态，不虚构关闭 |

`camera_fixed` 不是本项目已经确认的必填控制项。V01 的固定中远景、V03 的一次拉远写进提示词；实际界面若有镜头开关，必须把真实值写入生成记录。

声音提示词一律加上：

> 只有环境音和动作音效。禁止任何语言、对人说话、旁白、歌唱、字幕。

视频负面：

> 变形五官、眼镜消失、发长突变、猫耳、第三只猫、把两只猫融成一只、UI、文字、伤害数字、队友、镜头乱切、把猫吸进书里。

**模型提示词清洁规则**：本节以及 [`docs/nadia_video_pilot.md`](nadia_video_pilot.md) 中可直接提交给图像/视频模型的文本，只使用可视身份、构图、镜头、动作、时序、声音和负面约束；不使用人物名、猫名、技能名、镜头编号、本地文件名、内部变量或无视觉意义的项目叙事。项目名称仅保留在人类索引、资产文件名、验收标签和角色对白中。

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
| V06  | `nadia_voice_10_burst_start.mp3` 起手，`nadia_voice_11_burst_end.mp3` 锁环之后 |

对白出现时把生成轨压低 8–12 dB。

---

### V01 · 登场 · 6s · 首尾帧 K01→K01E

> 本段英文仅作镜头摘要，不是提交时的完整文本。实际提交请复制 [`docs/nadia_video_pilot.md`](nadia_video_pilot.md) 的 V01 提示词；首尾帧由页面输入区处理，提交文本不写本地文件名、内部帧编号或 `@图片` 标记。

**运动**

Use the uploaded first and last frames as the start and end anchors. Hold the same locked medium-wide/full-body 16:9 composition for the entire 6 seconds. The adult female surveyor’s face, glasses, torso, hands, both cats, and both boots remain visible throughout. No push-in, zoom, pan, tilt, crop, waist close-up, or reframing. The three measuring rings stay a small, dim secondary accessory at her waist and do not become the visual subject. The round cream-gold long-haired cat with a white chest and paws, round amber eyes, and a hollow silver-blue lock charm descends gently from the upper-left start pose and reaches the snow with her front paws; the slim ivory short-haired cat with faint warm points on the ears, nose, and tail, ice-blue eyes, and a charcoal-blue collar with a matte ice stone shifts one small step, lifts one front paw, and turns her head toward the surveyor. Snow drifts across the frame; the surveyor’s cloak and dark hair move in a gentle wind. Land smoothly on the uploaded last frame and hold the same wide composition. The surveyor does not speak. No cut, no new characters.

**声音**

Cold wind, distant snow, faint metallic tick of measuring rings, one very soft cat bell. No voice.

---

### V02 · 普攻 · 6s · K02→K03（机位保持）

**运动**

Hold the same camera. In 6 seconds the adult female surveyor performs a four-beat catalog attack, slower than game timing so each beat is readable. Beat 1: thumb on the spine, one ring flicks forward, a short ice page slices across. Beat 2: notebook turns vertical, a ring drops from her shoulder, a thin upright ice tick flashes; the round cream-gold long-haired cat’s tail in the background traces a tiny upward glint only. Beat 3: two rings cross, a four-point ice spark at the crossing; the slim ivory short-haired cat in the distance lifts her head, does not jump. Beat 4: she closes then opens the notebook, rings close at her chest, a larger ice refraction — land on the last frame. Cats never mount discs. No balance meter or readable UI. No speech.

**声音**

Paper, short ice scrape, light chime, ice crack, book clasp. No voice.

---

### V03 · 战技 · 6s · K04→K05（一次拉远）

**运动**

Start on the notebook clasp inside the same enclosed columned observatory hall. Ice-blue readout wakes from blank to a centered abstract zero mark, not + or −. Camera pulls to a front mid-shot without a cut. Three rings open. The round cream-gold long-haired cat with a white chest and paws and a hollow silver-blue lock charm steps onto the left disc; the slim ivory short-haired cat with faint warm points on the ears, nose, and tail and a charcoal-blue collar with a matte ice stone steps onto the right. The human remains the higher rear apex while the cats settle into the lower left and lower right anchors; do not finish as a flat row. Discs stay almost level. Thin orbit lines appear under them. Hold on the balanced three-body setup to match the revised ending frame. No teleport. No HUD. No speech.

**声音**

Book clasp, page, two discs seating, a low sustained measuring hum. No voice.

---

### V04 · 轻相 · 5s · K06→K07（机位保持）

**运动**

Same camera. The round cream-gold long-haired cat’s ears move first. Wind lifts her round body half a length off the left disc — she does not teleport. Sparse particles rise. An open ice arc grows upward and only half-closes, pointing inward. She pauses above the abstract ice-crystal targets. Hits glow, do not explode. Snow rises. The slim ivory short-haired cat stays on the right disc. End exactly on the hovering pose. No speech.

**声音**

Soft wind, rising ice grains, a gentle traction tighten. No voice.

---

### V05 · 重相 · 5s · K08→K09（机位下压约 8°）

**运动**

The slim ivory short-haired cat coils and leaps from the right disc like a normal light cat, then lands. Camera tilts down about 8 degrees. Ice cracks run outward along the ground. Targets stay put, pressed, not launched. A sinking wedge collapses into a small gold gravity point. The round cream-gold long-haired cat on the left disc bobbles upward one centimeter. End on the landed pose. No shockwave dome, no speech.

**声音**

Low landing thud, ice fracture, short heavy impact. No voice.

---

### V06 · 爆发 · 11s · K10→K11（机位逐步升高）

**运动**

0–2s: glasses glint, notebook opens, waist rings align. 2–5s: the round cream-gold long-haired cat hops onto the left disc and the disc rises; the slim ivory short-haired cat hops onto the right disc and the disc sinks; pointer swings then recenters. 5–8s: three rings push out of the page, slightly off-center, then snap to center; camera lifts to a gentle high angle. 8–11s: a huge ice-blue ring locks the field; three geometric anchors appear; hold the last frame. She stays calm. Cats are never sucked into the book. No 12-second combat loop, no HUD, no speech.

**声音**

Page, discs seating with opposite pitch (left high, right low), rings unfolding, a deep lock-in chime at the end. No voice.

---

### V07 · 风 · 6s · K12→K13（机位保持）

**运动**

Same daily camera. The adult female surveyor keeps writing. Wind builds. The round cream-gold long-haired cat’s body leaves the terrace slowly, leash and lock pulling taut. The surveyor’s other hand catches the leash without looking up. The slim ivory short-haired cat walks to her knee. Continuous shot, no combat rings. End on the caught-leash pose. No speech.

**声音**

Wind rising, snow, paper, a tiny lock-charm tick, one distant cat sound that is not a human word.

---

### V08 · 抱错了 · 6s · K14→K15（机位保持）

**运动**

Same daily camera. She bends and reaches with one hand. A pause. Her face stiffens. She switches to two hands and lifts the slim ivory short-haired cat; the board dips; glasses slip a millimeter. The slim ivory short-haired cat looks unbothered. The round cream-gold long-haired cat in the background almost floats. Hold the two-handed lift. No cartoon effects, no speech.

**声音**

Wood creak, fabric, a too-heavy lift effort, faint ice tick in the collar stone. No voice.

---

## 6. 叙事 PV 剪辑（约 60–80 秒）

成片文件建议：`output/nadia_character/assets/video/nadia_video_pv_between_two_weights_v1.mp4`，16:9 1080p。

| 时间（约） | 画面                      | 对白入点                                                 |
| ---------- | ------------------------- | -------------------------------------------------------- |
| 0:00–0:06  | V01                       | 01「你好。娜蒂娅……」                                     |
| 0:06–0:13  | V07                       | 03「风向变了。普莎，回来。」                             |
| 0:13–0:20  | V08                       | 05「今天也是稳定状态。」                                 |
| 0:20–0:27  | V03                       | 06「普莎，伊嘉——开始记录。」                             |
| 0:27–0:33  | V04                       | 07「轻端响应。普莎，慢一点。」                           |
| 0:33–0:39  | V05                       | 08「重端响应。伊嘉，落点确认。」                         |
| 0:39–0:50  | V06                       | 10 起手「重新归零。」；锁环后 11「轻与重，都记录好了。」 |
| 0:50–0:56  | 可回切 V01 最后一拍作静帧 | 无，或留风声                                             |

硬切或 8–12 帧叠化。不要加标题卡字幕抢过角色。片尾若需要一行字，后期单独排：`娜蒂娅「两衡之间」`，不要让 Seedance 烧字。

V02 普攻不进 PV，只挂技能页。

---

## 7. HTML 挂载（成片后再改，本轮不动代码）

| 镜头     | 建议位置                                                                            |
| -------- | ----------------------------------------------------------------------------------- |
| V01      | `index.html` hero，静图旁或可替换为循环视频+静图回退                                |
| V07、V08 | `index.html` `#companions` 或 `#voice` 待机条目附近                                 |
| V02–V06  | `skills.html` `#boards` 各 BOARD 的 `shot-media`：静图保留为 poster，视频作可播放层 |
| PV       | `index.html` 导航增加「介绍影像」，或档案页底部单独一节；不要放进明信片页           |

`<video>` 使用 `muted` 默认、`playsinline`、`preload="none"`、`poster` 指向对应关键帧。音量交给用户点播放，避免一进页就八条声轨。

公开包目录：

```text
output/nadia_character/assets/video/
  stills/
  nadia_video_v01_intro_1080p.mp4
  ...
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

本轮不再把“只落提示词”当作最终状态。已确认的执行细节、三张关键帧规格、两条视频提示词、声音边界、验收门和生成记录模板统一放在 [`docs/nadia_video_pilot.md`](nadia_video_pilot.md)。

执行顺序固定为：

1. 按参考图优先级生成 K01、K01E、K04、K05 四张 1920×1080 关键帧，并先做身份检查。
2. K01/K01E 作为 V01 首尾帧；K04/K05 作为 V03 首尾帧；两条都以 16:9、6s、720p 试跑。
3. 仅在身份、连续性、动作落点和音轨通过后，才复制参数生成 1080p；试片文件留在 `tmp/video_trials/`，不进入公开包。
4. 两条试片通过后，再回到本文件第 3 节的全量镜头表，决定是否制作 BOARD 05、Q 场地循环、生活片段扩展、PV 和 HTML 挂载。
