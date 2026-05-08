# -*- coding: utf-8 -*-
"""
水印生成模块
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont


# 系统字体路径（按优先级排序，支持 Windows/Linux/Mac）
SYSTEM_FONTS = [
    # Windows 字体
    "C:/Windows/Fonts/msyh.ttc",        # 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",      # 黑体
    "C:/Windows/Fonts/simsun.ttc",      # 宋体
    "C:/Windows/Fonts/STZHONGS.TTF",    # 华文中宋
    # Linux 字体
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # 文泉驿正黑
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    # Mac 字体
    "/System/Library/Fonts/PingFang.ttc",  # 苹方
    "/System/Library/Fonts/STHeiti Light.ttc",  # 黑体
    # 通用
    "arial.ttf",
]


def find_available_font():
    """查找系统可用字体"""
    for font_path in SYSTEM_FONTS:
        if os.path.exists(font_path):
            return font_path
    return None


def calculate_font_size(text, page_width, page_height, font_path=None, max_font_size=120, min_font_size=24):
    """
    根据页面大小和文字长度自动计算合适的字号
    
    Args:
        text: 水印文字
        page_width: 页面宽度（像素）
        page_height: 页面高度（像素）
        font_path: 字体路径
        max_font_size: 最大字号
        min_font_size: 最小字号
        
    Returns:
        int: 合适的字号
    """
    # 计算对角线长度作为参考
    diagonal = math.sqrt(page_width ** 2 + page_height ** 2)
    
    # 目标：文字长度约为对角线的 60%
    target_width = diagonal * 0.6
    
    # 尝试从大到小找到合适的字号
    for font_size in range(max_font_size, min_font_size - 1, -2):
        try:
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.load_default()
            
            # 获取文字实际宽度
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= target_width:
                return font_size
        except:
            continue
    
    return min_font_size


def generate_watermark_image(
    text,
    width,
    height,
    color=(128, 128, 128),
    opacity=0.3,
    angle=-45,
    font_path=None,
    font_size=None,
    output_path=None
):
    """
    生成水印图片（平铺覆盖整个页面）
    
    Args:
        text: 水印文字
        width: 图片宽度
        height: 图片高度
        color: 文字颜色 (R, G, B)
        opacity: 透明度 (0-1)
        angle: 旋转角度
        font_path: 字体路径
        font_size: 字号（None 则自动计算）
        output_path: 输出路径（None 则返回图片对象）
        
    Returns:
        PIL.Image 或 str: 图片对象或保存路径
    """
    # 查找可用字体
    if font_path is None:
        font_path = find_available_font()
    
    # 自动计算字号
    if font_size is None:
        font_size = calculate_font_size(text, width, height, font_path)
    
    # 创建透明背景图片
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 加载字体
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
    
    # 应用透明度到颜色
    r, g, b = color
    a = int(255 * opacity)
    text_color = (r, g, b, a)
    
    # 平铺水印文字
    # 计算间距（文字宽度 + 间距 = 步长）
    step_x = text_width + 100
    step_y = text_height + 80
    
    # 计算需要绘制多少行/列才能覆盖整个页面（考虑旋转）
    # 旋转后覆盖范围会扩大，所以多绘制一些
    margin = max(width, height)
    
    for y in range(-margin, height + margin, step_y):
        for x in range(-margin, width + margin, step_x):
            # 错位排列（奇数行偏移半个步长）
            offset = (step_x // 2) if ((y + margin) // step_y) % 2 == 1 else 0
            draw.text((x + offset, y), text, font=font, fill=text_color)
    
    # 旋转整个图片
    rotated = image.rotate(angle, expand=False, center=(width//2, height//2))
    
    # 保存或返回
    if output_path:
        rotated.save(output_path, 'PNG')
        return output_path
    
    return rotated


def create_watermark_for_excel(
    client_name,
    sheet_width=1200,
    sheet_height=800,
    config=None
):
    """
    为 Excel 创建水印图片
    
    Args:
        client_name: 客户名称
        sheet_width: 工作表宽度
        sheet_height: 工作表高度
        config: 水印配置
        
    Returns:
        str: 水印图片路径
    """
    if config is None:
        from config import DEFAULT_WATERMARK_CONFIG
        config = DEFAULT_WATERMARK_CONFIG
    
    # 构建水印文字
    suffix = config.get("suffix", "non-disclosure")
    text = f"{client_name} {suffix}"
    
    # 解析颜色
    from utils import validate_color
    color = validate_color(config.get("color", "#808080"))
    if color is None:
        color = (128, 128, 128)
    
    # 获取字体大小（优先使用配置，否则自动计算）
    font_size = config.get("font_size", None)
    
    # 生成水印图片
    import tempfile
    import time
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"watermark_{int(time.time() * 1000000)}.png")
    
    generate_watermark_image(
        text=text,
        width=sheet_width,
        height=sheet_height,
        color=color,
        opacity=config.get("opacity", 0.4),
        angle=config.get("angle", -45),
        font_size=font_size,
        output_path=temp_path
    )
    
    return temp_path


def add_watermark_to_sheet(worksheet, watermark_image_path):
    """
    给工作表添加水印
    
    Args:
        worksheet: openpyxl 工作表对象
        watermark_image_path: 水印图片路径
    """
    from openpyxl.drawing.image import Image as XLImage
    
    # 添加水印图片
    img = XLImage(watermark_image_path)
    
    # 设置图片位置（左上角）
    img.anchor = 'A1'
    
    # 添加到工作表
    worksheet.add_image(img)
