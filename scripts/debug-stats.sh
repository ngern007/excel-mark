#!/bin/bash
# 统计调试记录

DEBUG_DIR="debug-logs"
ARCHIVE_DIR="$DEBUG_DIR/archive"

echo "📊 调试记录统计"
echo "================"
echo

# 统计进行中的问题
ONGOING=$(find "$DEBUG_DIR" -maxdepth 1 -name "*.md" ! -name "TEMPLATE.md" ! -name "README.md" | wc -l)
echo "🔄 进行中: $ONGOING 个问题"

# 统计已解决的问题
if [ -d "$ARCHIVE_DIR" ]; then
    ARCHIVED=$(find "$ARCHIVE_DIR" -name "*.md" | wc -l)
    echo "✅ 已解决: $ARCHIVED 个问题"
else
    echo "✅ 已解决: 0 个问题"
fi

echo
echo "📁 最近的问题:"
echo

# 列出最近的调试记录
find "$DEBUG_DIR" -maxdepth 1 -name "*.md" ! -name "TEMPLATE.md" ! -name "README.md" -printf "%f\n" | sort -r | head -5 | while read file; do
    echo "  - $file"
done

if [ -d "$ARCHIVE_DIR" ]; then
    echo
    echo "📦 最近归档:"
    echo
    find "$ARCHIVE_DIR" -name "*.md" -printf "%f\n" | sort -r | head -5 | while read file; do
        echo "  - $file"
    done
fi
