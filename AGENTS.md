# Chat Memo Website

Chat Memo 产品家族的公开官网，生产地址 `https://chatmemo.ai`。

## 生产事实

- Git 仓库：`eze-is/chat-memo-website`
- 部署：GitHub Pages，从 `main` 分支根目录发布
- `CNAME`、页面 HTML、`updates-data.json` 与 `resource/` 是线上部署资产
- Cloudflare 只代理域名与 CDN，不拥有本仓的构建或发布事实

## 入口

| 任务 | 入口 |
|---|---|
| 首页与页面 | `index.html`、`welcome.html`、`updates.html` |
| 线上资源 | `resource/` |
| 更新数据 | `updates-data.json` |
| 发版文案单源扇出 | `.agent/skills/chatmemo-update/SKILL.md` |
| 产品家族结构与宣传资产 | `../INDEX.md`、`../assets/brand-and-marketing/INDEX.md` |

## 开发资产

- `.agent/skills/` 是 Skill 唯一真实目录。
- `.claude/skills`、`.agents/skills`、`.Codex/skills` 是兼容软链接，不维护副本。
- `CLAUDE.md` 指向本文件。

官网与浏览器插件是独立 Git 仓；跨仓发版只通过 `chatmemo-update` 的结构化条目和 `release_fanout.py` 协作。不要把插件源码、商店包或产品家族宣传源文件复制进官网仓；页面直接引用的部署资源必须继续留在本仓。
