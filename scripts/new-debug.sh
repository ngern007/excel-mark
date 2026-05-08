#!/bin/bash
# 创建新的调试记录

DEBUG_DIR="debug-logs"
TEMPLATE="$DEBUG_DIR/TEMPLATE.md"

if [ -z "$1" ]; then
    echo "用法: ./scripts/new-debug.sh \"问题简述\""
    echo "示例: ./scripts/new-debug.sh \"登录接口返回401\""
    exit 1
fi

# 获取当前日期
DATE=$(date +%Y-%m-%d)
# 简化问题描述（替换空格为连字符）
SUMMARY=$(echo "$1" | sed 's/ /-/g')
# 生成文件名
FILENAME="$DEBUG_DIR/${DATE}-${SUMMARY}.md"

# 检查文件是否已存在
if [ -f "$FILENAME" ]; then
    echo "❌ 文件已存在: $FILENAME"
    exit 1
fi

# 复制模板
cp "$TEMPLATE" "$FILENAME"

# 在文件开头添加标题
TITLE="# $DATE - $1"
sed -i "1s|^.*|$TITLE|" "$FILENAME"

echo "✅ 创建调试记录: $FILENAME"
echo "📝 开始记录你的调试过程吧！"

# 如果有编辑器，打开文件
if command -v code &> /dev/null; then
    code "$FILENAME"
elif command -v vim &> /dev/null; then
    vim "$FILENAME"
fi
