#!/usr/bin/env python3
"""
build_book.py
将 output/ 目录下所有章节 Markdown 文件按顺序拼接成一本完整的电子书。

用法：
    python build_book.py                        # 生成 大语言模型的强化学习算法.md
    python build_book.py --output my_book.md   # 自定义输出文件名
    python build_book.py --toc                 # 仅打印目录，不生成文件
"""

import os
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================
# 章节顺序配置（按需调整）
# ============================================================
CHAPTER_ORDER = [
    "chapter_1-理论基础",
    "chapter_2-强化学习具体算法",
    "chapter_3-工程实践",
]

# 每个章节内子目录的顺序
SECTION_ORDER = {
    "chapter_1-理论基础": [
        "1.1-核心数学概念解析",
        "1.2-性能差异引理PDL",
        "1.3-替代目标函数L",
    ],
    "chapter_2-强化学习具体算法": [
        "2.1-TRPO算法",
        "2.2-PPO算法",
        "2.3-DPO算法",
        "2.4-GRPO算法",
        "2.5-SAPO_GSPO",
        "2.6-学术前沿",
    ],
    "chapter_3-工程实践": [],  # 直接扫描目录下所有 md
}

# 每个子目录内文件的顺序（按文件名前缀排序，无需手动维护）
def get_md_files_sorted(directory: Path):
    """递归获取目录下所有 .md 文件，按文件名排序"""
    files = []
    for f in sorted(directory.glob("*.md")):
        files.append(f)
    return files


def build_toc(base_dir: Path) -> list[str]:
    """生成目录列表"""
    toc = ["# 目录\n"]
    for chapter in CHAPTER_ORDER:
        chapter_dir = base_dir / chapter
        if not chapter_dir.exists():
            continue
        # 章节标题
        chapter_title = chapter.split("-", 1)[1] if "-" in chapter else chapter
        toc.append(f"\n## {chapter_title}\n")

        sections = SECTION_ORDER.get(chapter, [])
        if sections:
            for section in sections:
                section_dir = chapter_dir / section
                if not section_dir.exists():
                    continue
                section_title = section.split("-", 1)[1] if "-" in section else section
                toc.append(f"\n### {section_title}\n")
                for md_file in get_md_files_sorted(section_dir):
                    toc.append(f"- {md_file.stem}\n")
        else:
            for md_file in get_md_files_sorted(chapter_dir):
                toc.append(f"- {md_file.stem}\n")
    return toc


def build_book(base_dir: Path, output_file: Path):
    """拼接所有章节为一个完整 Markdown 文件"""
    parts = []

    # 封面
    now = datetime.now()
    version = now.strftime("v%Y.%m.%d")
    build_time = now.strftime("%Y-%m-%d %H:%M")
    parts.append("# 大语言模型的强化学习算法\n\n")
    parts.append(f"**作者**：chenglitao　｜　**版本**：{version}　｜　**构建时间**：{build_time}\n\n")
    parts.append("---\n\n")

    # 目录页
    parts.extend(build_toc(base_dir))
    parts.append("\n---\n\n")

    # 正文
    for chapter in CHAPTER_ORDER:
        chapter_dir = base_dir / chapter
        if not chapter_dir.exists():
            print(f"⚠️  跳过不存在的章节目录: {chapter}")
            continue

        chapter_title = chapter.split("-", 1)[1] if "-" in chapter else chapter
        parts.append(f"\n\n---\n\n# {chapter_title}\n\n")

        sections = SECTION_ORDER.get(chapter, [])
        if sections:
            for section in sections:
                section_dir = chapter_dir / section
                if not section_dir.exists():
                    print(f"⚠️  跳过不存在的小节目录: {section}")
                    continue
                for md_file in get_md_files_sorted(section_dir):
                    print(f"  ✅ {md_file.relative_to(base_dir)}")
                    content = md_file.read_text(encoding="utf-8")
                    # 修正图片路径：相对子目录的 assets/ → 根目录的 assets/
                    content = content.replace("](assets/", "](assets/")
                    parts.append(content)
                    parts.append("\n\n")
        else:
            for md_file in get_md_files_sorted(chapter_dir):
                print(f"  ✅ {md_file.relative_to(base_dir)}")
                content = md_file.read_text(encoding="utf-8")
                content = content.replace("](assets/", "](assets/")
                parts.append(content)
                parts.append("\n\n")

    # 写入文件
    full_content = "".join(parts)
    output_file.write_text(full_content, encoding="utf-8")
    size_kb = output_file.stat().st_size / 1024
    print(f"\n✅ 图书生成完成: {output_file}  ({size_kb:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="将章节 Markdown 文件合并为完整电子书")
    parser.add_argument("--output", default="大语言模型的强化学习算法.md", help="输出文件名（默认: 大语言模型的强化学习算法.md）")
    parser.add_argument("--toc", action="store_true", help="仅打印目录")
    args = parser.parse_args()

    # 自动定位 output/ 目录（脚本放在项目根目录）
    script_dir = Path(__file__).parent
    base_dir = script_dir / "output"

    if not base_dir.exists():
        print(f"❌ 找不到 output/ 目录: {base_dir}")
        return

    if args.toc:
        print("".join(build_toc(base_dir)))
        return

    output_file = script_dir / args.output
    print(f"📚 开始合并章节...\n")
    build_book(base_dir, output_file)


if __name__ == "__main__":
    main()
