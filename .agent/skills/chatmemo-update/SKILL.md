---
name: chatmemo-update
description: Chat Memo 浏览器插件与官网的发版文案单源扇出。Use when 用户说“发布插件新版本”“生成更新海报”“创建更新公告”“同步官网与商店更新日志”或提供版本号与功能列表。区分全量发版和仅生成宣传材料；全量发版必须先用结构化双语条目 dry-run，确认后才写入官网与插件两个独立仓。
---

# Chat Memo Release Fan-out

## 核心哲学

- 一份结构化双语发版条目是唯一事实源；官网数据、海报、公告、插件 CHANGELOG、manifest、开发期 package 与 lockfile 元数据和商店说明都是派生物。
- `website/` 与 `browser-extension/` 是两个独立 Git 仓。脚本只跨仓扇出明确契约，不把仓库生命周期耦合在一起。
- 本 Skill 只生成或更新文件，不替用户 tag、push、上传商店或部署官网。

## 前置检查

1. 确认官网与插件位于同一产品家族目录：`website/`、`browser-extension/`。
2. 插件版本必须以 Chrome 商店实际生产版本或其已核验 tag 为基线，不得默认把远端 `main` 当生产。
3. 官网生产源以 GitHub Pages 的 `main` 根目录为准；Cloudflare 只承担 DNS/代理/CDN 时，不得写成 Cloudflare Pages 部署。
4. 全量发版前，插件变更已经写入 `CHANGELOG.md` 的 `[Unreleased]`，最终用户文案已经确认。
5. 如果文案尚未确认，只创建 entry 或执行 `--dry-run`，不得实际写入。
6. 遇到不明 dirty worktree，先盘点并保留，不覆盖、不顺手清理。

## 选择正确路径

| 目标 | 使用方式 |
|---|---|
| 完整插件发版扇出 | `release_fanout.py`，先 dry-run，确认后再写入 |
| 只预览完整扇出 | `release_fanout.py --dry-run` |
| 只生成海报和公告 | `generate_files.py` |
| 调整今后所有海报/公告风格 | 修改 `assets/` 中的模板 |
| 修改当前线上官网页面 | 直接修改官网生产文件，不通过宣传素材目录绕行 |

## 全量发版工作流

### ① 建立唯一条目

参照 [`assets/release-entry.example.json`](./assets/release-entry.example.json) 创建 JSON：

- `version`：不带 `v` 的版本号
- `date`：发版日期
- `summary`：中英双语摘要
- `poster`：中文海报标题与公告标题
- `features[]`：`type`、`icon`、中英双语标题与说明

条目通常从插件 `CHANGELOG.md` 的 `[Unreleased]` 提炼，但最终条目才是本次扇出的唯一输入。

### ② 先 dry-run

在官网仓根目录运行：

```bash
python3 .agent/skills/chatmemo-update/scripts/release_fanout.py \
  --entry path/to/release-entry.json \
  --dry-run
```

默认路径应解析为：

- 官网：`../website`
- 插件：`../browser-extension`

若目录不同，显式传入 `--website-root`、`--changelog`、`--manifest`、`--package`、`--package-lock`，不得依赖猜测。

### ③ 获得确认后再写入

```bash
python3 .agent/skills/chatmemo-update/scripts/release_fanout.py \
  --entry path/to/release-entry.json
```

脚本派生七类结果：

1. 官网 `updates-data.json`
2. 官网 `update-item/{version}.html`
3. 官网 `update-item/{version}-update.md`
4. 插件 `CHANGELOG.md`
5. 插件 `manifest.json`
6. 插件 `package.json` 与 `package-lock.json` 的开发期版本元数据
7. 官网 `update-item/{version}-release-notes.txt`

### ④ 分仓验收

分别检查官网和插件的 `git diff`、测试与构建。两个仓分别 commit；未经明确授权，不 tag、push、上传商店或部署。

## 仅生成海报与公告

```bash
python3 .agent/skills/chatmemo-update/scripts/generate_files.py \
  --version 1.3.4 \
  --date "2026年8月28日" \
  --title "更新标题" \
  --headline "Chat Memo v1.3.4 发布" \
  --summary "本次更新摘要" \
  --features "✨|功能标题|面向用户的功能说明"
```

默认输出到官网仓 `update-item/`；可用 `--output` 指定其他目录。生成脚本会同时复制海报所需的 `logo-single.png`。

## 成功标准

- 只有一份结构化发版输入，所有派生文案版本一致。
- dry-run 不产生文件改动。
- 写入前一次性预检两个仓的目标文件；重复运行不会重复插入同一 CHANGELOG 版本。
- 实际扇出只触及约定的七类目标。
- 官网与插件仍可独立测试、提交、回滚和发布。
- 不把“生成材料”扩大成未经授权的发版动作。

## 技术事实与陷阱

- Chrome 商店生产版本与远端默认分支可能不同；必须先核验生产包/tag。
- 官网由 GitHub Pages 从 `main` 根目录发布时，Cloudflare 代理状态不等于 Cloudflare Pages。
- 产品家族的历史宣传源文件归 `../assets/brand-and-marketing/`；官网实际引用的部署资源继续留在官网仓。
- 当前模板自带 `logo-single.png` 作为生成依赖；这不自动把它升级为品牌唯一权威源。
- 一次性改生成物只影响当次；可复用的视觉或文案偏好应修改模板。

## References 索引

| 文件 | 何时读取 |
|---|---|
| [`assets/release-entry.example.json`](./assets/release-entry.example.json) | 创建结构化发版条目时 |
| [`references/format-guide.md`](./references/format-guide.md) | 调整海报结构、字段或写作格式时 |
| [`assets/poster-template.html`](./assets/poster-template.html) | 修改长期海报视觉时 |
| [`assets/markdown-template.md`](./assets/markdown-template.md) | 修改长期公告文案结构时 |
