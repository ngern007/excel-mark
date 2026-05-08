# -*- coding: utf-8 -*-
"""
Excel 水印工具 - 主程序入口

使用方法:
    python excel_watermark.py -n "客户名称" -f 文件路径
    python excel_watermark.py -n "客户名称" -d 目录路径
    python excel_watermark.py -n "客户名称" -f 文件路径 -o 输出目录
    python excel_watermark.py -n "客户名称" -f 文件路径 -c "#FF0000"
"""

import argparse
import os
import sys

from config import load_config, get_supported_extensions, TEMP_DIR
from utils import setup_logger, get_file_type, validate_color
from file_handler import process_single_file, process_batch


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='Excel 水印工具 - 为 Excel/CSV 文件添加水印',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s -n "张三" -f report.xlsx
  %(prog)s -n "张三" -f data.zip
  %(prog)s -n "张三" -d ./files/
  %(prog)s -n "张三" -f report.xlsx -o ./output/
  %(prog)s -n "张三" -f report.xlsx -c "#808080"
  %(prog)s -n "张三" -f report.xlsx --font-size 100
  %(prog)s -n "张三" -f report.xlsx --opacity 0.5
  %(prog)s -n "张三" -f report.xlsx --config config.yaml
        '''
    )
    
    parser.add_argument(
        '-n', '--name',
        required=True,
        help='客户名称（必填）'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='要处理的文件路径'
    )
    
    parser.add_argument(
        '-d', '--dir',
        help='要处理的目录路径（批量处理）'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出目录（默认为源文件目录）'
    )
    
    parser.add_argument(
        '-c', '--color',
        help='水印颜色（如 #808080）'
    )
    
    parser.add_argument(
        '--font-size',
        type=int,
        help='字体大小（如 72, 100, 150）'
    )
    
    parser.add_argument(
        '--opacity',
        type=float,
        help='透明度（0.1-1.0，如 0.4）'
    )
    
    parser.add_argument(
        '--config',
        help='配置文件路径'
    )
    
    return parser.parse_args()


def collect_files(directory):
    """
    收集目录下所有支持的文件
    
    Args:
        directory: 目录路径
        
    Returns:
        list: 文件路径列表
    """
    supported_extensions = get_supported_extensions()
    files = []
    
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            ext = os.path.splitext(file_path)[1].lower()
            if ext in supported_extensions:
                files.append(file_path)
    
    return files


def main():
    """主函数"""
    args = parse_arguments()
    
    # 加载配置
    config = load_config(args.config)
    
    # 覆盖命令行指定的颜色
    if args.color:
        color = validate_color(args.color)
        if color:
            config['watermark']['color'] = args.color
        else:
            print(f"警告: 无效的颜色格式 '{args.color}'，使用默认颜色")
    
    # 覆盖命令行指定的字体大小
    if args.font_size:
        config['watermark']['font_size'] = args.font_size
    
    # 覆盖命令行指定的透明度
    if args.opacity:
        config['watermark']['opacity'] = args.opacity
    
    # 设置日志
    logger = setup_logger(config['log'])
    
    # 验证输入
    if not args.file and not args.dir:
        logger.error("请指定要处理的文件 (-f) 或目录 (-d)")
        sys.exit(1)
    
    if args.file and args.dir:
        logger.error("不能同时指定文件和目录，请使用其中一个")
        sys.exit(1)
    
    # 收集要处理的文件
    files = []
    if args.file:
        if not os.path.exists(args.file):
            logger.error(f"文件不存在: {args.file}")
            sys.exit(1)
        files = [args.file]
    else:
        if not os.path.exists(args.dir):
            logger.error(f"目录不存在: {args.dir}")
            sys.exit(1)
        files = collect_files(args.dir)
        if not files:
            logger.error(f"目录中没有找到支持的文件: {args.dir}")
            sys.exit(1)
    
    # 输出信息
    logger.info("=" * 50)
    logger.info("Excel 水印工具")
    logger.info("=" * 50)
    logger.info(f"客户名称: {args.name}")
    logger.info(f"文件数量: {len(files)}")
    logger.info(f"输出目录: {args.output or '源文件目录'}")
    logger.info(f"水印颜色: {config['watermark']['color']}")
    logger.info(f"字体大小: {config['watermark'].get('font_size', '自动')}")
    logger.info(f"透明度: {config['watermark'].get('opacity', 0.4)}")
    logger.info("=" * 50)
    
    # 处理文件
    if len(files) == 1:
        print(f"\n[处理中] {os.path.basename(files[0])}")
        result = process_single_file(
            files[0],
            args.name,
            args.output,
            config['watermark'],
            logger
        )
        if result:
            print(f"[完成] 输出文件: {result}")
        else:
            print("[错误] 处理失败")
            sys.exit(1)
    else:
        results = process_batch(
            files,
            args.name,
            args.output,
            config['watermark'],
            logger
        )
        
        print("\n" + "=" * 50)
        print(f"处理完成: 成功 {len(results)}/{len(files)} 个文件")
        print("=" * 50)
        
        if results:
            print("\n输出文件:")
            for r in results:
                print(f"  - {r}")
    
    logger.info("处理完成")


if __name__ == '__main__':
    main()
