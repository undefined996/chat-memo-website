---
name: chatmemo-update
description: This skill should be used when a user wants to create Chat Memo update/release materials. Primary workflow is "单源扇出 (release fan-out)" — author one structured bilingual release entry and propagate it to ALL changelog locations (website updates-data.json, marketing poster, announcement markdown, the browser-extension CHANGELOG.md + manifest version, and GitHub/Chrome-Store release notes). Use when the user says "发布新版本", "创建更新", "生成更新海报", "发版", or provides version + feature list for a release.
---

# Chat Memo Update Generator

## Overview

This skill generates two essential marketing/documentation assets for Chat Memo version releases:

1. **HTML Poster** (`{VERSION}.html`) - A visually appealing 3:4 aspect ratio poster featuring the brand logo, version information, and a list of new features/improvements
2. **Update Description** (`{VERSION}-update.md`) - A markdown document suitable for blog posts, newsletters, or social media announcements

The generated files follow the exact format and style of existing Chat Memo release materials (e.g., 1.1.2.html and 1.1.2-update.md), ensuring brand consistency across all communications.

**Key Automation Features**:
- Automatically creates output directory at `project-root/update-item/`
- Automatically copies `logo-single.png` to ensure HTML poster displays correctly
- Defaults to creating all files in the standardized location

## 发版扇出（推荐主流程 · 单源多派生）

发版文案是**唯一事实源**，多处更新日志是**派生**。一次确认文案，扇出到所有位置，避免在 N 个地方手写同一份日志。

官网（chat-memo-website）与浏览器插件（开发/chat-memo_DEV）是**两个独立仓**；本流程用一份「发版文案 schema」作为两仓间的显式契约，由 `release_fanout.py` 跨仓桥接（一次工具动作，非结构耦合）。

### 单一事实源：结构化双语条目

schema 见 [`assets/release-entry.example.json`](./assets/release-entry.example.json)：`version`（不带 v）/ `date`/`summary`（双语）/ `poster`（海报标题+公告标题，中文营销）/ `features[]`（`type` = `new|improvement|fix`、`icon`、双语 `title`+`description`）。

发版时由插件 `CHANGELOG.md` 的 `[Unreleased]` 草稿润色 + 补 en 翻译得到这份条目——**这是唯一一次"确认文案"**。

### 扇出

```bash
# 先预览（强烈建议），确认无误再去掉 --dry-run 实际写入
python3 scripts/release_fanout.py --entry path/to/release-entry.json --dry-run
python3 scripts/release_fanout.py --entry path/to/release-entry.json
```

一次扇出到 6 处：① 官网 `updates-data.json`（prepend 双语条目）② 官网 `update-item/{ver}.html` 海报 ③ 官网 `update-item/{ver}-update.md` 公告 ④ 插件 `CHANGELOG.md`（`[Unreleased]` → `[ver]-日期`）⑤ 插件 `manifest.json` version ⑥ `update-item/{ver}-release-notes.txt`（GitHub Release / Chrome 商店"新功能"）。

路径默认按脚本位置推断两仓；可用 `--website-root` / `--changelog` / `--manifest` 覆盖。海报/公告复用下方的 `generate_files.py`（未改动）。

> 仅需海报+公告、不做全量发版时，仍可直接用下面的 `generate_files.py`（保留作为底层能力）。

## Core Capabilities

### 1. HTML Poster Generation

**Output file**: `{VERSION}.html` (e.g., 1.1.2.html)

**Template**: `assets/poster-template.html`

**Key features**:
- 600px × 800px canvas with 3:4 aspect ratio
- Blurred logo background (opacity: 0.15, blur: 48px)
- Brand color scheme (primary blue: #3B45C4, primary purple: #5A4CFF)
- Dynamic number of feature cards (highlighted first card)
- Professional typography using Noto Sans SC font

**Variable placeholders**:
- `{VERSION}` - Version number (e.g., "1.1.2")
- `{DATE}` - Release date (e.g., "2025年12月3日")
- `{MAIN_TITLE}` - Main headline with optional line breaks
- `{UPDATE_CARDS}` - Generated HTML for feature cards

**Example execution**:
```bash
python3 scripts/generate_files.py \
  --version 1.1.3 \
  --date "2025年12月10日" \
  --title "大模型支持升级\n新增 Claude 3.5 录制"
```

### 2. Markdown Update Description Generation

**Output file**: `{VERSION}-update.md` (e.g., 1.1.2-update.md)

**Template**: `assets/markdown-template.md`

**Sections**:
1. Title/Headline
2. Executive summary (2-3 sentences)
3. Feature highlights with numbered list
4. How to update (fixed template)
5. Feedback & community section (fixed template)

**Variable placeholders**:
- `{HEADLINE}` - Announcement title
- `{EXECUTIVE_SUMMARY}` - Brief introduction
- `{FEATURE_LIST}` - Formatted feature list

**Example execution**:
```bash
python3 scripts/generate_files.py \
  --headline "支持 Claude 了！Chat Memo v1.1.3 发布" \
  --summary "重磅功能来啦！" \
  --features "🚀|新增 Claude 支持|现在可以自动保存 Claude 的对话记录了"
```

## Workflow for Creating Update Materials

### Step 1: Gather Release Information

Collect the following information from the user:

- **Version number** (required): e.g., "1.1.3"
- **Release date** (required): e.g., "2025年12月10日"
- **Main headline** (required): Short title for the poster, can include `\n` for line breaks
- **Update announcement title** (required): Full title for the markdown document
- **Executive summary** (required): 2-3 sentence overview
- **Feature list** (required): One or more features in the format: `ICON|TITLE|DESCRIPTION`

**Feature format details**:
- Use `|` as delimiter (pipe character)
- ICON: Emoji representation (e.g., 🚀, ✨, 🔧)
- TITLE: Feature name (2-10 characters)
- DESCRIPTION: Feature details (1-2 sentences)
- First feature should be the most important (gets highlighted)

### Step 2: Run the Generation Script

The script automatically handles directory creation and logo copying. Execute with required parameters:

```bash
python3 scripts/generate_files.py \
  --version VERSION \
  --date "DATE" \
  --title "HEADLINE" \
  --headline "MARKDOWN_TITLE" \
  --summary "SUMMARY" \
  --features "ICON1|TITLE1|DESC1" \
             "ICON2|TITLE2|DESC2" \
             "ICON3|TITLE3|DESC3"
```

**What the script does automatically**:
- ✅ Creates the `update-item/` directory at `project-root/update-item/`
- ✅ Copies `logo-single.png` to ensure the HTML poster displays correctly
- ✅ Generates all files in the standardized location
- ✅ Reports the status of each operation

### Step 3: Review Generated Files

The script produces files in `<project-root>/update-item/`:

1. `{VERSION}.html` - Open in a browser to verify visual appearance
2. `{VERSION}-update.md` - Review content for accuracy and tone
3. `logo-single.png` - Automatically copied for the HTML poster

**Default location**: `/Users/eze/Desktop/Chat-Memo-Project/官网/chat-memo-website/updates-pic/update-item/`

**Checklist**:
- [ ] First card has `highlight` class
- [ ] Logo displays correctly (both in header and blurred background)
- [ ] Version number appears in both files
- [ ] Date format is correct
- [ ] All feature cards render properly
- [ ] Markdown has proper spacing and formatting
- [ ] `logo-single.png` is present in output directory

### Step 4: Refine if Necessary

If adjustments are needed:

- **Visual changes**: Edit the HTML file or modify `assets/poster-template.html`
- **Content changes**: Edit the Markdown file or modify `assets/markdown-template.md`
- **Style changes**: Update CSS in the HTML template or adjust the generation script

**Note**: For recurring style preferences, update the templates rather than individual generated files.

**Custom Output Location**: If you need to output to a different directory, use the `--output` flag:

```bash
# Custom output directory
python3 scripts/generate_files.py --output ./my-custom-dir ...

# Absolute path
python3 scripts/generate_files.py --output /path/to/output ...
```

When using custom output locations, the script will still automatically create the directory and copy the logo file.

## Style Guidelines

### Visual Design (HTML Poster)

- **Background**: Blurred logo with 15% opacity
- **Primary colors**: Blue (#3B45C4) and Purple (#5A4CFF)
- **Card design**: White background with backdrop blur, 20px border radius
- **Typography**: Noto Sans SC font family
- **Layout**: Left-aligned logo, right-aligned version tag

### Writing Tone (Markdown Update)

**Use a relaxed, friendly style**:

- **Include emojis**: 🚀, 🎉, ✨, 🔧, 💡, etc.
- **Use conversational language**: "重磅功能来啦！" instead of "重大功能更新"
- **Be concise but warm**: Short paragraphs, friendly tone
- **Focus on user benefits**: Explain what the feature does for the user
- **First feature gets extra attention**: Most important update listed first

**Example of effective feature description**:
```markdown
🚀 新增 Kimi 平台支持
现在 Chat Memo 也能自动保存 Kimi 的对话记录了，灵感不再丢失，每一句对话都将被妥善保管。
```

**Less effective** (too formal):
```markdown
新增对 Kimi 平台的支持
已完成 Kimi 平台的集成，支持自动保存功能。
```

## Resources

### Templates

- **Poster HTML Template**: [`assets/poster-template.html`](./assets/poster-template.html)
  - Contains placeholders: `{VERSION}`, `{DATE}`, `{MAIN_TITLE}`, `{UPDATE_CARDS}`
  - Source reference: `assets/poster-reference.html` (full 1.1.2.html example)

- **Markdown Template**: [`assets/markdown-template.md`](./assets/markdown-template.md)
  - Contains placeholders: `{HEADLINE}`, `{EXECUTIVE_SUMMARY}`, `{FEATURE_LIST}`
  - Source reference: `assets/markdown-reference.md` (full 1.1.2-update.md example)

### Brand Assets

- **Logo file**: [`assets/logo-single.png`](./assets/logo-single.png)
  - **Important**: This logo file is required for the HTML poster to display correctly
  - Used in both the header and blurred background
  - Ensure this file is present in the same directory as generated HTML files
  - If creating files in a different location, copy this logo file along with the HTML

**How to use**: When generating an HTML poster, the `logo-single.png` file must be in the same directory as the generated `{VERSION}.html` file for the logo to display properly.

### Format Guide

**Reference**: [`references/format-guide.md`](./references/format-guide.md)

Comprehensive documentation covering:
- Complete HTML structure with all CSS
- Markdown section breakdown
- Feature item format (`ICON|TITLE|DESCRIPTION`)
- Version naming conventions
- Visual design specifications
- Writing style examples

**Use this when**: You need to understand the full format specification or adjust the templates.

### Generation Script

**Script**: [`scripts/generate_files.py`](./scripts/generate_files.py)

**Capabilities**:
- Reads HTML and Markdown templates
- Replaces placeholders with user-provided data
- Generates feature cards dynamically
- Saves output files with proper encoding

**Dependencies**: Python 3.x, no external packages required

**Usage**:
```bash
python3 scripts/generate_files.py --help
```

## Example: Complete Release Workflow

**Scenario**: Creating release materials for version 1.1.3 with Claude support

### User Request

```
发布 v1.1.3，包含功能：
1. 新增 Claude 支持 🚀
2. 搜索速度提升 3 倍 ✨
3. 修复 Gemini 重复保存问题 🔧
4. UI 优化 💅
```

### Claude's Actions

1. **Request additional information**:
   - Release date
   - Main headline for poster
   - Announcement title for markdown
   - Executive summary

2. **Execute generation**:

```bash
python3 scripts/generate_files.py \
  --version 1.1.3 \
  --date "2025年12月10日" \
  --title "Claude 来啦！\n还支持 30+ 种语言" \
  --headline "重磅更新！Chat Memo v1.1.3 支持 Claude" \
  --summary "让你所有 AI 对话都能被保存和回顾，这次我们加入了大家都在催的 Claude 支持！" \
  --features "🚀|新增 Claude 3.5 支持|现在可以自动保存 Claude 的对话记录了，Anthropic 用户久等了！" \
             "✨|搜索速度提升 3 倍|底层搜索算法重构，找对话再也不用等待" \
             "🔧|修复 Gemini 重复保存|解决 Gemini 平台消息重复保存的问题，节省存储空间" \
             "💅|UI 细节优化|调整卡片间距、优化阴影效果，视觉体验更舒适"
```

3. **Verify output**:
   - Open `1.1.3.html` in browser
   - Review `1.1.3-update.md` content
   - Check that first feature has `highlight` class

4. **Provide files to user**:
   - HTML poster ready for sharing
   - Markdown document ready for blog/post

## Common Issues and Solutions

### Template files not found

**Error**: `❌ 模板文件不存在`

**Solution**: Ensure the script is run from the skill directory or that template files exist in the expected location.

**Template directory**: `/Users/eze/Desktop/Chat-Memo-Project/官网/chat-memo-website/updates-pic/.claude/skills/chatmemo-update/assets`

### Invalid feature format

**Error**: `❌ 功能格式错误`

**Solution**: Features must use format: `ICON|TITLE|DESCRIPTION`

**Example**: `🚀|新增 Kimi 支持|终于等到你！现在可以自动保存 Kimi 的对话记录了`

### File encoding issues

**Solution**: The script uses UTF-8 encoding. Ensure your terminal supports UTF-8 for proper emoji display.

## Notes

- Always use the same version number for both files
- The first feature gets `highlight` class automatically
- **Automatic logo handling**: The script automatically copies `logo-single.png` from the project root to the output directory. No manual copying is required.
- **Default output location**: Files are saved to `project-root/update-item/` by default
- Both output files are independent and can be edited separately after generation
- For recurring releases, consider creating a simple wrapper script with common parameters

### Logo File Location

The script expects `logo-single.png` to be located in the **project root directory** (the directory containing `updates-pic/`). The script will:
1. Automatically detect the project root
2. Copy the logo file to the output directory
3. Display a warning if the logo cannot be found

If you need to use a custom logo location, modify the `get_project_root()` function in `scripts/generate_files.py`.

### Output Directory Structure

After running the script, the following structure is created:

```
project-root/
├── updates-pic/
│   ├── .claude/
│   ├── logo-single.png      # Source logo file
│   ├── 1.1.2.html           # Previous releases
│   └── update-item/         # ⬅️ Generated files go here
│       ├── logo-single.png  # Copied automatically
│       ├── 1.1.3.html       # Generated poster
│       └── 1.1.3-update.md  # Generated description
```

This keeps all release files organized in a dedicated directory while maintaining access to the logo file.
