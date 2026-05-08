#!/bin/bash
# 归档已解决的调试记录

DEBUG_DIR="debug-logs"
ARCHIVE_DIR="$DEBUG_DIR/archive"

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

if [ -z "$1" ]; then
    echo "用法: ./scripts/archive-debug.sh <调试记录文件>"
    echo "示例: ./scripts/archive-debug.sh debug-logs/2026-05-08-login-401.md"
    exit 1
fi

FILENAME="$1"

# 检查文件是否存在
if [ ! -f "$FILENAME" ]; then
    echo "❌ 文件不存在: $FILENAME"
    exit 1
fi

# 移动到归档目录
BASENAME=$(basename "$FILENAME")
mv "$FILENAME" "$ARCHIVE_DIR/$BASENAME"

echo "✅ 已归档: $ARCHIVE_DIR/$BASENAME"

# 提交到 Git
read -p "是否提交到 Git? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add "$ARCHIVE_DIR/$BASENAME"
    git commit -m "docs: archive debug record - $BASENAME"
    echo "✅ 已提交到 Git"
fi
