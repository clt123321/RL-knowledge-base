#!/usr/bin/env python3
"""
fix_gfm_latex.py
修复 GitHub Flavored Markdown 对 LaTeX 公式的渲染问题。

规则：
1. 强制空行隔离：每个独立的 $$ 上下各有一个空行
2. 列表缩进保护：列表项后跟 $$ 时，保证 $$ 缩进对齐
3. 清理非法转义符：$...$ 内部的 \_ 替换为 _
4. 修复目录锚点：生成正确的 GitHub anchor 跳转链接
"""

import re
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# 规则 3: 清理 LaTeX 内部的非法转义符 \_  →  _
# ──────────────────────────────────────────────────────────────
def fix_escaped_underscores(text: str) -> str:
    result = []
    i = 0
    length = len(text)

    while i < length:
        # 匹配块级公式 $$...$$
        if text[i:i+2] == '$$':
            end = text.find('$$', i + 2)
            if end != -1:
                inner = text[i+2:end]
                inner = inner.replace('\\_', '_')
                result.append('$$' + inner + '$$')
                i = end + 2
                continue
        # 匹配行内公式 $...$（避免 $$ 被误匹配）
        elif text[i] == '$' and (i == 0 or text[i-1] != '$') and text[i+1:i+2] != '$':
            end = text.find('$', i + 1)
            while end != -1 and text[end-1] == '\\':
                end = text.find('$', end + 1)
            if end != -1 and text[end+1:end+2] != '$':
                inner = text[i+1:end]
                inner = inner.replace('\\_', '_')
                result.append('$' + inner + '$')
                i = end + 1
                continue
        result.append(text[i])
        i += 1

    return ''.join(result)


# ──────────────────────────────────────────────────────────────
# 规则 1 & 2: 强制空行隔离 + 列表缩进保护
# ──────────────────────────────────────────────────────────────
LIST_ITEM_RE = re.compile(r'^(\s*(?:[-*+]|\d+\.)\s+)')

def fix_block_formula_spacing(text: str) -> str:
    lines = text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 检测到 $$ 开始行
        if stripped == '$$' or stripped.startswith('$$') and not stripped.endswith('$$'):
            # 规则1：上方空行
            if result and result[-1].strip() != '':
                result.append('')

            # 规则2：检查前文是否是列表项，需要缩进
            indent = ''
            for prev in reversed(result):
                if prev.strip() == '':
                    continue
                m = LIST_ITEM_RE.match(prev)
                if m:
                    indent = '   '  # 列表下 3 空格缩进
                break

            result.append(indent + line.lstrip())
            i += 1

            # 收集公式体直到结束 $$
            while i < len(lines):
                body_line = lines[i]
                body_stripped = body_line.strip()
                result.append(indent + body_line.lstrip() if indent else body_line)
                i += 1
                if body_stripped == '$$' or body_stripped.endswith('$$'):
                    break

            # 规则1：下方空行
            if i < len(lines) and lines[i].strip() != '':
                result.append('')
        else:
            result.append(line)
            i += 1

    return '\n'.join(result)


# ──────────────────────────────────────────────────────────────
# 规则 4: 修复目录锚点链接（GitHub anchor 生成规则）
# ──────────────────────────────────────────────────────────────
def to_github_anchor(heading_text: str) -> str:
    """将标题文本转换为 GitHub 风格的 anchor"""
    # 去掉标题中的 markdown 格式符和 LaTeX
    text = re.sub(r'\$[^$]+\$', '', heading_text)  # 去掉行内公式
    text = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', text)  # 只保留字母/中文/空格/连字符
    text = text.strip().lower()
    text = re.sub(r'\s+', '-', text)  # 空格替换为 -
    return '#' + text


def fix_toc_anchors(text: str) -> str:
    """重建文中的目录跳转链接"""
    lines = text.split('\n')
    # 收集所有标题
    headings = {}
    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            anchor = to_github_anchor(title)
            headings[title] = anchor

    # 修复目录区域中形如 [标题文字](#xxx) 的链接
    def replace_anchor(m):
        label = m.group(1)
        # 在已收集的标题中查找匹配
        for title, anchor in headings.items():
            if label in title or title in label:
                return f'[{label}]({anchor})'
        return m.group(0)

    result = re.sub(r'\[([^\]]+)\]\(#[^)]*\)', replace_anchor, text)
    return result


# ──────────────────────────────────────────────────────────────
# 主处理流程
# ──────────────────────────────────────────────────────────────
def process_file(path: Path) -> dict:
    original = path.read_text(encoding='utf-8')
    text = original

    text = fix_escaped_underscores(text)
    text = fix_block_formula_spacing(text)

    changed = text != original
    if changed:
        path.write_text(text, encoding='utf-8')
    return {'changed': changed, 'path': path}


def main():
    root = Path(__file__).parent

    # 要处理的 md 文件（排除 debug 目录）
    md_files = [
        p for p in root.rglob('*.md')
        if 'debug' not in str(p) and '.git' not in str(p)
    ]

    total = len(md_files)
    changed_count = 0
    changed_files = []

    print(f'🔍 扫描到 {total} 个 Markdown 文件...\n')

    for md_path in sorted(md_files):
        result = process_file(md_path)
        if result['changed']:
            changed_count += 1
            changed_files.append(md_path.relative_to(root))
            print(f'  ✏️  {md_path.relative_to(root)}')

    print(f'\n✅ 处理完成！共修改 {changed_count}/{total} 个文件：')
    for f in changed_files:
        print(f'   - {f}')

    if changed_count == 0:
        print('   （所有文件已符合规范，无需修改）')


if __name__ == '__main__':
    main()
