#!/usr/bin/env python3
"""
测试水印生成 - 对比不同字体大小
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# 系统字体路径
SYSTEM_FONTS = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # 文泉驿正黑
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]

def find_font():
    for path in SYSTEM_FONTS:
        if os.path.exists(path):
            return path
    return None

def create_watermark_test(text, font_size, opacity, output_path):
    """创建测试水印"""
    width, height = 1200, 800
    
    # 创建透明背景
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    font_path = find_font()
    print(f"字体路径: {font_path}")
    
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"字体加载失败: {e}")
        font = ImageFont.load_default()
    
    # 获取文字尺寸
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    print(f"文字尺寸: {text_width}x{text_height}")
    
    # 计算颜色（带透明度）
    a = int(255 * opacity)
    color = (128, 128, 128, a)
    
    # 平铺水印
    step_x = text_width + 100
    step_y = text_height + 80
    margin = max(width, height)
    
    for y in range(-margin, height + margin, step_y):
        for x in range(-margin, width + margin, step_x):
            offset = (step_x // 2) if ((y + margin) // step_y) % 2 == 1 else 0
            draw.text((x + offset, y), text, font=font, fill=color)
    
    # 旋转
    rotated = image.rotate(-45, expand=False, center=(width//2, height//2))
    
    # 保存
    rotated.save(output_path, 'PNG')
    print(f"保存到: {output_path}")
    print(f"文件大小: {os.path.getsize(output_path)} bytes")

# 测试不同配置
text = "测试对比 non-disclosure"
configs = [
    (72, 0.4, "watermark_72pt_40p.png"),
    (100, 0.5, "watermark_100pt_50p.png"),
    (150, 0.6, "watermark_150pt_60p.png"),
]

print("=" * 50)
for font_size, opacity, filename in configs:
    print(f"\n测试: {font_size}pt, {int(opacity*100)}%")
    output = f"/home/node/.openclaw/workspace/excel-watermark/output/{filename}"
    create_watermark_test(text, font_size, opacity, output)
    print("-" * 50)
