# Excel Watermark 项目

Excel 批量水印工具 - 为 Excel 文件添加自定义水印

## 功能特性

- 批量处理 Excel 文件
- 支持文本水印
- 支持图片水印
- 可配置水印位置、透明度等参数

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python excel_watermark.py
```

## 项目结构

```
excel-watermark/
├── excel_watermark.py    # 主程序
├── watermark.py          # 水印处理核心
├── file_handler.py       # 文件处理
├── config.py             # 配置管理
├── debug-logs/           # 调试记录目录
│   ├── TEMPLATE.md       # 调试记录模板
│   ├── README.md         # 调试记录说明
│   └── archive/          # 已解决问题归档
└── scripts/              # 自动化脚本
    ├── new-debug.sh      # 创建新调试记录
    ├── archive-debug.sh  # 归档调试记录
    └── debug-stats.sh    # 调试统计
```

## 调试记录

本项目使用 `debug-logs/` 目录管理调试过程，所有调试记录都会提交到 Git。

详见：[debug-logs/README.md](debug-logs/README.md)

### 快速创建调试记录

```bash
./scripts/new-debug.sh "问题描述"
```

## 开发日志

查看 `debug-logs/` 目录了解开发过程中的问题追踪和解决方案。
