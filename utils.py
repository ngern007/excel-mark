# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import os
import shutil
import logging
from datetime import datetime


def setup_logger(log_config):
    """
    设置日志记录器
    
    Args:
        log_config: 日志配置字典
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger("excel_watermark")
    logger.setLevel(logging.INFO)
    
    # 清除已有的处理器
    logger.handlers = []
    
    if log_config.get("enabled", True):
        log_path = log_config.get("path", "./logs")
        os.makedirs(log_path, exist_ok=True)
        
        log_file = os.path.join(
            log_path, 
            log_config.get("filename", "process.log")
        )
        
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def generate_output_filename(original_path, client_name, output_dir=None):
    """
    生成输出文件名
    
    Args:
        original_path: 原文件路径
        client_name: 客户名称
        output_dir: 输出目录（None 或空字符串则使用原文件目录）
        
    Returns:
        str: 输出文件完整路径
    """
    # 安全检查
    if not original_path:
        raise ValueError("原文件路径不能为空")
    if not client_name:
        raise ValueError("客户名称不能为空")
    
    # 获取原文件名和扩展名
    dir_name = os.path.dirname(original_path)
    file_name = os.path.basename(original_path)
    name, ext = os.path.splitext(file_name)
    
    # 生成新文件名
    new_name = f"{name}_for_{client_name}{ext}"
    
    # 确定输出目录（处理 None 和空字符串）
    target_dir = output_dir if output_dir else dir_name
    
    # 再次确保 target_dir 不为空
    if not target_dir:
        target_dir = "."
    
    return os.path.join(target_dir, new_name)


def ensure_temp_dir(temp_dir):
    """确保临时目录存在"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def clean_temp_dir(temp_dir):
    """清理临时目录"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def get_file_type(file_path):
    """
    判断文件类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 'excel', 'csv', 'archive' 或 None
    """
    from config import SUPPORTED_FORMATS
    
    ext = os.path.splitext(file_path)[1].lower()
    
    for file_type, extensions in SUPPORTED_FORMATS.items():
        if ext in extensions:
            return file_type
    
    return None


def print_progress(status, current=None, total=None, filename=None):
    """
    打印处理进度
    
    Args:
        status: 状态 ('processing', 'done', 'error')
        current: 当前文件序号
        total: 总文件数
        filename: 当前文件名
    """
    if status == 'processing':
        if current and total and filename:
            print(f"[处理中] ({current}/{total}) {filename}")
        elif filename:
            print(f"[处理中] {filename}")
        else:
            print("[处理中]...")
            
    elif status == 'done':
        if filename:
            print(f"[完成] {filename}")
        else:
            print("[完成]")
            
    elif status == 'error':
        if filename:
            print(f"[错误] {filename}")
        else:
            print("[错误]")


def validate_color(color_str):
    """
    验证颜色格式
    
    Args:
        color_str: 颜色字符串，如 "#808080"
        
    Returns:
        tuple: (R, G, B) 或 None
    """
    if not color_str:
        return None
        
    color_str = color_str.strip()
    
    if color_str.startswith('#') and len(color_str) == 7:
        try:
            r = int(color_str[1:3], 16)
            g = int(color_str[3:5], 16)
            b = int(color_str[5:7], 16)
            return (r, g, b)
        except ValueError:
            return None
    
    return None
