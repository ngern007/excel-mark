# -*- coding: utf-8 -*-
"""
配置模块 - 所有可配置项集中管理，便于调试和修改
"""

import os
import yaml

# ============================================================
# 核心配置项（常修改项置顶）
# ============================================================

# 默认水印配置
DEFAULT_WATERMARK_CONFIG = {
    "color": "#808080",      # 默认灰色
    "opacity": 0.4,          # 透明度 40%（更清晰）
    "angle": -45,            # 倾斜角度
    "font": "Arial",         # 字体
    "font_size": 72,         # 字体大小（增大，更清晰）
    "suffix": "non-disclosure"  # 后缀文字
}

# 默认输出配置
DEFAULT_OUTPUT_CONFIG = {
    "path": "",              # 默认源文件路径
    "suffix_format": "_for_{client_name}"  # 命名格式
}

# 默认日志配置
DEFAULT_LOG_CONFIG = {
    "enabled": True,
    "path": os.path.join(os.path.dirname(__file__), "logs"),
    "filename": "process.log"
}

# 支持的文件格式
SUPPORTED_FORMATS = {
    "excel": [".xlsx", ".xls"],
    "csv": [".csv"],
    "archive": [".zip"]
}

# 临时目录
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")

# ============================================================
# 配置加载函数
# ============================================================

def load_config(config_path=None):
    """
    从 YAML 文件加载配置
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        dict: 合并后的配置字典
    """
    config = {
        "watermark": DEFAULT_WATERMARK_CONFIG.copy(),
        "output": DEFAULT_OUTPUT_CONFIG.copy(),
        "log": DEFAULT_LOG_CONFIG.copy()
    }
    
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
            if user_config:
                # 合并配置
                if "watermark" in user_config:
                    config["watermark"].update(user_config["watermark"])
                if "output" in user_config:
                    config["output"].update(user_config["output"])
                if "log" in user_config:
                    config["log"].update(user_config["log"])
    
    return config


def get_supported_extensions():
    """获取所有支持的文件扩展名"""
    extensions = []
    for ext_list in SUPPORTED_FORMATS.values():
        extensions.extend(ext_list)
    return extensions
