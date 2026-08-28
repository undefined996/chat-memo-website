#!/usr/bin/env python3
"""
Chat Memo 发版文案「一次确认，扇出多处」工具。

读一份结构化双语发版条目（唯一事实源），派生到所有更新日志位置：
  1. 官网 updates-data.json        —— prepend 新条目（双语，驱动 chatmemo.ai/updates）
  2. 官网 update-item/{ver}.html    —— 营销海报（复用 generate_files）
  3. 官网 update-item/{ver}-update.md —— 公告长文（复用 generate_files）
  4. 插件 CHANGELOG.md              —— [Unreleased] 切成 [ver]-日期
  5. 插件 manifest.json             —— version 同步（版本号唯一事实源）
  6. 插件 package.json / lockfile   —— 开发期 npm 元数据，随 manifest 同步
  7. release-notes.txt              —— GitHub Release / Chrome 商店「新功能」文本

设计：官网与插件是两个独立仓（两个黑盒），本工具是它们之间「发版文案 schema」
这条显式契约的桥接器——一次工具动作跨仓写，不是结构耦合。

用法：
  python3 release_fanout.py --entry release-entry.json [--dry-run]
  路径默认按脚本位置推断，可用 --website-root / --changelog / --manifest 覆盖。

条目 schema 见 assets/release-entry.example.json。
"""

import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import generate_files  # 复用海报/公告生成（不修改它）

# CHANGELOG / updates-data.json 的 type → 中文小节
TYPE_ZH = {"new": "新增", "improvement": "改进", "fix": "修复"}
TYPE_ORDER = ["new", "improvement", "fix"]


def default_paths():
    """按脚本位置推断默认路径（skill 在 <web>/.agent/skills/chatmemo-update/scripts/）。"""
    website_root = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
    ext_root = os.path.abspath(os.path.join(website_root, "..", "browser-extension"))
    return {
        "website_root": website_root,
        "updates_data": os.path.join(website_root, "updates-data.json"),
        "update_item": os.path.join(website_root, "update-item"),
        "changelog": os.path.join(ext_root, "CHANGELOG.md"),
        "manifest": os.path.join(ext_root, "manifest.json"),
        "package": os.path.join(ext_root, "package.json"),
        "package_lock": os.path.join(ext_root, "package-lock.json"),
    }


def load_entry(path):
    with open(path, "r", encoding="utf-8") as f:
        entry = json.load(f)
    # 最小校验
    for k in ("version", "date", "summary", "features"):
        if k not in entry:
            sys.exit(f"❌ 条目缺少必填字段: {k}")
    for f in entry["features"]:
        if f.get("type") not in TYPE_ZH:
            sys.exit(f"❌ feature.type 非法: {f.get('type')}（应为 {list(TYPE_ZH)}）")
        for k in ("title", "description"):
            if "zh-CN" not in f.get(k, {}) or "en" not in f.get(k, {}):
                sys.exit(f"❌ feature.{k} 需同时含 zh-CN 与 en")
    if not re.fullmatch(r"(?:0|[1-9]\d*)(?:\.(?:0|[1-9]\d*)){1,3}", entry["version"]):
        sys.exit("❌ version 必须是 2–4 段非负整数，且不带 v 前缀")
    return entry


def version_tuple(version):
    """Chrome manifest 版本比较；缺失段按 0 补齐。"""
    parts = tuple(int(part) for part in version.split("."))
    return parts + (0,) * (4 - len(parts))


def assert_manifest_version_not_downgraded(path, target_version):
    """发版扇出必须 fail closed，禁止示例或旧条目把生产版本倒退。"""
    text = open(path, encoding="utf-8").read()
    match = re.search(r'"version"\s*:\s*"([^"]+)"', text)
    if not match:
        sys.exit("❌ manifest.json 未找到 version 字段")
    current_version = match.group(1)
    if version_tuple(target_version) < version_tuple(current_version):
        sys.exit(
            f"❌ 拒绝版本倒退：manifest.json 当前为 {current_version}，"
            f"条目目标为 {target_version}"
        )


def preflight_targets(updates_path, changelog_path, manifest_path, package_path, package_lock_path, target_version):
    """写入前一次性校验全部事实源，避免可预见错误造成跨仓半写入。"""
    updates = json.load(open(updates_path, encoding="utf-8"))
    if not isinstance(updates.get("updates"), list):
        sys.exit("❌ updates-data.json 缺少 updates 数组")

    changelog = open(changelog_path, encoding="utf-8").read()
    version_heading = re.compile(rf"^## \[{re.escape(target_version)}\](?:\s|$)", re.MULTILINE)
    if not version_heading.search(changelog) and "## [Unreleased]\n" not in changelog:
        sys.exit("❌ CHANGELOG.md 未找到 [Unreleased] 段")

    assert_manifest_version_not_downgraded(manifest_path, target_version)
    package = json.load(open(package_path, encoding="utf-8"))
    if not isinstance(package.get("version"), str):
        sys.exit("❌ package.json 未找到字符串 version 字段")
    package_lock = json.load(open(package_lock_path, encoding="utf-8"))
    if not isinstance(package_lock.get("version"), str):
        sys.exit("❌ package-lock.json 未找到字符串 version 字段")
    if not isinstance(package_lock.get("packages", {}).get("", {}).get("version"), str):
        sys.exit("❌ package-lock.json 未找到 packages[''].version 字段")


def feature_pipe_strings(entry):
    """转成 generate_files 期望的 'ICON|TITLE|DESC'（中文，营销侧）。"""
    out = []
    for f in entry["features"]:
        icon = f.get("icon", "✨")
        out.append(f"{icon}|{f['title']['zh-CN']}|{f['description']['zh-CN']}")
    return out


# ---------- 各派生目标 ----------

def build_updates_entry(entry):
    """官网 updates-data.json 的条目（双语，去掉 icon/poster）。"""
    return {
        "version": f"v{entry['version']}",
        "date": entry["date"],
        "summary": entry["summary"],
        "features": [
            {"type": f["type"], "title": f["title"], "description": f["description"]}
            for f in entry["features"]
        ],
    }


def update_updates_data(path, entry, dry):
    data = json.load(open(path, encoding="utf-8"))
    new = build_updates_entry(entry)
    existing = [u["version"] for u in data["updates"]]
    if new["version"] in existing:
        print(f"⚠️  updates-data.json 已存在 {new['version']}，跳过 prepend")
        return
    data["updates"].insert(0, new)
    if dry:
        print(f"  [dry] 将 prepend {new['version']} 到 updates-data.json（共 {len(data['updates'])} 条）")
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✅ updates-data.json 已 prepend {new['version']}")


def build_changelog_section(entry):
    """生成 CHANGELOG 版本小节（中文，按 type 分组）。"""
    by_type = {}
    for f in entry["features"]:
        by_type.setdefault(f["type"], []).append(f)
    lines = [f"## [{entry['version']}] - {entry['date']['zh-CN']}", ""]
    for t in TYPE_ORDER:
        if t not in by_type:
            continue
        lines.append(f"### {TYPE_ZH[t]}")
        lines.append("")
        for f in by_type[t]:
            lines.append(f"- **{f['title']['zh-CN']}**：{f['description']['zh-CN']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def update_changelog(path, entry, dry):
    text = open(path, encoding="utf-8").read()
    section = build_changelog_section(entry)
    version_heading = re.compile(rf"^## \[{re.escape(entry['version'])}\](?:\s|$)", re.MULTILINE)
    if version_heading.search(text):
        print(f"  CHANGELOG.md 已存在 [{entry['version']}]，跳过切分")
        return
    # 把 [Unreleased] 段（到下一个 ## [ 之前）替换为：空的 [Unreleased] + 新版本段
    pattern = re.compile(r"(## \[Unreleased\]\n)(.*?)(?=\n## \[)", re.DOTALL)
    if not pattern.search(text):
        sys.exit("❌ CHANGELOG.md 未找到 [Unreleased] 段")
    replacement = "## [Unreleased]\n\n" + section + "\n"
    new_text = pattern.sub(lambda m: replacement, text, count=1)
    if dry:
        print(f"  [dry] CHANGELOG.md 将切出 [{entry['version']}] - {entry['date']['zh-CN']}，并清空 [Unreleased]")
        print("  ---- 新版本段预览 ----")
        for ln in section.splitlines():
            print("  | " + ln)
        return
    open(path, "w", encoding="utf-8").write(new_text)
    print(f"✅ CHANGELOG.md 已切出 [{entry['version']}]，[Unreleased] 已清空")


def update_manifest(path, entry, dry):
    text = open(path, encoding="utf-8").read()
    m = re.search(r'"version"\s*:\s*"([^"]+)"', text)
    if not m:
        sys.exit("❌ manifest.json 未找到 version 字段")
    old = m.group(1)
    if old == entry["version"]:
        print(f"  manifest.json version 已是 {old}，无需改")
        return
    if dry:
        print(f"  [dry] manifest.json version: {old} → {entry['version']}")
        return
    new_text = text[: m.start(1)] + entry["version"] + text[m.end(1):]
    open(path, "w", encoding="utf-8").write(new_text)
    print(f"✅ manifest.json version: {old} → {entry['version']}")


def update_package_version(path, entry, dry):
    data = json.load(open(path, encoding="utf-8"))
    old = data.get("version")
    if old == entry["version"]:
        print(f"  package.json version 已是 {old}，无需改")
        return
    if dry:
        print(f"  [dry] package.json version: {old} → {entry['version']}")
        return
    data["version"] = entry["version"]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"✅ package.json version: {old} → {entry['version']}")


def update_package_lock_version(path, entry, dry):
    data = json.load(open(path, encoding="utf-8"))
    old = data["version"]
    old_root = data["packages"][""]["version"]
    if old == entry["version"] and old_root == entry["version"]:
        print(f"  package-lock.json version 已是 {old}，无需改")
        return
    if dry:
        print(f"  [dry] package-lock.json version: {old} / {old_root} → {entry['version']}")
        return
    data["version"] = entry["version"]
    data["packages"][""]["version"] = entry["version"]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"✅ package-lock.json version: {old} / {old_root} → {entry['version']}")


def build_release_notes(entry):
    """GitHub Release / Chrome 商店「新功能」纯文本（中文）。"""
    lines = [f"Chat Memo v{entry['version']}", "", entry["summary"]["zh-CN"], ""]
    for f in entry["features"]:
        lines.append(f"- {f['title']['zh-CN']}：{f['description']['zh-CN']}")
    return "\n".join(lines) + "\n"


def write_poster_and_md(entry, update_item_dir, dry):
    feats = feature_pipe_strings(entry)
    ver = entry["version"]
    html = generate_files.generate_html_poster(ver, entry["date"]["zh-CN"], entry.get("poster", {}).get("title", entry["summary"]["zh-CN"]), feats)
    md = generate_files.generate_markdown_update(ver, entry.get("poster", {}).get("headline", f"Chat Memo v{ver} 发布"), entry["summary"]["zh-CN"], feats)
    html_path = os.path.join(update_item_dir, f"{ver}.html")
    md_path = os.path.join(update_item_dir, f"{ver}-update.md")
    if dry:
        print(f"  [dry] 将生成海报 {html_path}（{len(html)} 字符）")
        print(f"  [dry] 将生成公告 {md_path}（{len(md)} 字符）")
        return
    os.makedirs(update_item_dir, exist_ok=True)
    generate_files.setup_output_directory(update_item_dir)
    open(html_path, "w", encoding="utf-8").write(html)
    open(md_path, "w", encoding="utf-8").write(md)
    print(f"✅ 海报: {html_path}")
    print(f"✅ 公告: {md_path}")


def main():
    p = argparse.ArgumentParser(description="发版文案一次确认、扇出多处")
    p.add_argument("--entry", required=True, help="结构化双语发版条目 JSON 路径")
    p.add_argument("--dry-run", action="store_true", help="只预览不写入")
    dp = default_paths()
    p.add_argument("--website-root", default=dp["website_root"])
    p.add_argument("--updates-data", default=dp["updates_data"])
    p.add_argument("--update-item", default=dp["update_item"])
    p.add_argument("--changelog", default=dp["changelog"])
    p.add_argument("--manifest", default=dp["manifest"])
    p.add_argument("--package", default=dp["package"])
    p.add_argument("--package-lock", default=dp["package_lock"])
    p.add_argument("--notes-out", default=None, help="release-notes 文本输出路径（默认 update-item/{ver}-release-notes.txt）")
    args = p.parse_args()

    entry = load_entry(args.entry)
    ver = entry["version"]
    preflight_targets(
        args.updates_data,
        args.changelog,
        args.manifest,
        args.package,
        args.package_lock,
        ver,
    )
    notes_out = args.notes_out or os.path.join(args.update_item, f"{ver}-release-notes.txt")

    print(f"📦 发版扇出 v{ver}（{'DRY-RUN 预览' if args.dry_run else '写入'}）")
    print(f"   官网仓: {args.website_root}")
    print(f"   插件 CHANGELOG: {args.changelog}")
    print()

    print("① 官网 updates-data.json")
    update_updates_data(args.updates_data, entry, args.dry_run)
    print("② / ③ 官网海报 + 公告")
    write_poster_and_md(entry, args.update_item, args.dry_run)
    print("④ 插件 CHANGELOG.md")
    update_changelog(args.changelog, entry, args.dry_run)
    print("⑤ 插件 manifest.json version")
    update_manifest(args.manifest, entry, args.dry_run)
    print("⑥ 插件 package.json version")
    update_package_version(args.package, entry, args.dry_run)
    update_package_lock_version(args.package_lock, entry, args.dry_run)
    print("⑦ release-notes 文本（GitHub/Chrome 商店）")
    notes = build_release_notes(entry)
    if args.dry_run:
        print(f"  [dry] 将写 {notes_out}")
        for ln in notes.splitlines():
            print("  | " + ln)
    else:
        notes_dir = os.path.dirname(notes_out)
        if notes_dir:
            os.makedirs(notes_dir, exist_ok=True)
        open(notes_out, "w", encoding="utf-8").write(notes)
        print(f"✅ {notes_out}")

    print()
    print("✨ 扇出完成。" + ("（预览，未写入任何文件）" if args.dry_run else "请检查各处文案后再提交/发版。"))


if __name__ == "__main__":
    main()
