# 娜蒂娅「两衡之间」

这是一个围绕娜蒂娅、普莎、伊嘉与“衡标”展开的原创同人角色设计与展示仓库。项目包含角色设定、玩法规格、技能表现、语音文案、交互式网页和可印刷 PDF。内容借用《原神》的世界观语汇，但不是官方资料，也不代表真实游戏数据或服务器逻辑已经验证。

## 快速查看

网页使用本地资源，不需要前端构建工具或联网。启动仓库根目录的静态服务器：

```sh
python3 -m http.server 8000
```

然后打开 <http://localhost:8000/output/nadia_character/index.html>。公共展示页包括角色档案、玩法规格、技能表现和 24 张可翻面的明信片；页面中的图片与 20 条中文语音均来自本地 `output/nadia_character/assets/`。

## 目录说明

- `docs/`：角色设定、剧情、玩法、语音与实体制作的设计基线。
- `output/nadia_character/`：对外 HTML 展示包及其资源；其中 `print/` 保存 PDF 生成脚本。
- `output/pdf/`：20 页 A5 角色档案和 48 页明信片套组。
- `tools/nadia_skill_simulator.html`：开发调参用模拟器，不属于公开分享包。

## 生成印刷文件

在 Python 3.10+ 虚拟环境中安装 `reportlab`、`Pillow` 和 `pypdf`，并使用 macOS CJK 字体，然后运行：

```sh
python3 output/nadia_character/print/build_dossier.py
python3 output/nadia_character/print/build_postcards.py
```

生成结果写入 `output/pdf/`。修改 HTML、图片或文案时，应同步更新相关文档、路径和受影响的 PDF/分享包。大型 ZIP 交付物由 Git LFS 管理；需要时先执行 `git lfs pull`。

## 隐私与贡献边界

`xiting/*.jpg` 是仅供本地创作参考的私人照片，已被忽略，禁止加入公开 HTML、PDF、ZIP 或 Git 提交。新增素材应使用生成后的角色资产，并保持现有的小写命名和版本后缀。提交前运行 `git diff --check`，并参阅 [`AGENTS.md`](AGENTS.md) 了解完整的贡献和审阅要求。
