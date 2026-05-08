#!/usr/bin/env python3
"""
创建便携版 Excel 水印工具 - v1.3
修复：Windows 编码问题
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def build_portable():
    """创建便携版"""
    
    # 当前目录
    src_dir = Path(__file__).parent
    dist_dir = src_dir / "dist" / "excel-watermark-portable"
    
    # 清理旧文件
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    print("📦 创建便携版 Excel 水印工具 v1.3...")
    
    # 1. 复制 Python 脚本
    scripts = ["excel_watermark.py", "config.py", "watermark.py", 
               "file_handler.py", "utils.py", "config.yaml"]
    for script in scripts:
        src = src_dir / script
        if src.exists():
            shutil.copy2(src, dist_dir / script)
            print(f"  ✓ 复制 {script}")
    
    # 2. 创建启动脚本 (Windows)
    bat_content = '''@echo off
chcp 65001 >nul
title Excel 水印工具
echo ========================================
echo    Excel 水印工具 - 便携版 v1.3
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
pip show openpyxl >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装依赖...
    pip install openpyxl Pillow PyYAML
)

REM 显示帮助
echo 使用方法:
echo   excel_watermark.exe -n "客户名称" -f 文件路径
echo   excel_watermark.exe -n "客户名称" -d 目录路径
echo.
echo 可选参数:
echo   --font-size 100    字体大小
echo   --opacity 0.5      透明度
echo   -c "#FF0000"       水印颜色
echo.
echo 示例:
echo   excel_watermark.exe -n "张三" -f report.xlsx --font-size 100 --opacity 0.5
echo.

REM 运行程序
python excel_watermark.py %*
'''
    
    with open(dist_dir / "excel_watermark.bat", "w", encoding="utf-8") as f:
        f.write(bat_content)
    print("  ✓ 创建启动脚本 excel_watermark.bat")
    
    # 3. 创建 GUI 启动脚本
    gui_content = '''@echo off
chcp 65001 >nul
title Excel 水印工具 - GUI

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python
    pause
    exit /b 1
)

REM 检查依赖
pip show openpyxl >nul 2>&1
if errorlevel 1 (
    pip install openpyxl Pillow PyYAML
)

REM 启动 GUI
python excel_watermark_gui.py
'''
    
    with open(dist_dir / "run_gui.bat", "w", encoding="utf-8") as f:
        f.write(gui_content)
    print("  ✓ 创建 GUI 启动脚本 run_gui.bat")
    
    # 4. 创建修复版 GUI（修复 Windows 编码问题）
    gui_script = r'''#!/usr/bin/env python3
"""
Excel 水印工具 - GUI v1.3
修复：Windows 编码问题
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys
import yaml
import platform

class ExcelWatermarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel 水印工具 v1.3")
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        
        # 检测系统编码
        self.system_encoding = 'gbk' if platform.system() == 'Windows' else 'utf-8'
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建界面
        self.create_widgets()
    
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except:
            return {"watermark": {}}
    
    def save_config(self):
        """保存配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def create_widgets(self):
        """创建界面组件"""
        root = self.root
        row = 0
        
        # ===== 基本信息 =====
        tk.Label(root, text="【基本信息】", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=3, padx=10, pady=(15, 5), sticky="w")
        row += 1
        
        # 客户名称
        tk.Label(root, text="客户名称:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.client_entry = tk.Entry(root, width=35)
        self.client_entry.grid(row=row, column=1, columnspan=2, padx=10, pady=8, sticky="w")
        row += 1
        
        # ===== 文件选择 =====
        tk.Label(root, text="【文件选择】", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")
        row += 1
        
        # 选择文件
        tk.Label(root, text="选择文件:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.file_entry = tk.Entry(root, width=35)
        self.file_entry.grid(row=row, column=1, padx=10, pady=8, sticky="w")
        tk.Button(root, text="浏览", command=self.browse_file, width=8).grid(row=row, column=2, padx=5)
        row += 1
        
        # 选择目录
        tk.Label(root, text="选择目录:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.dir_entry = tk.Entry(root, width=35)
        self.dir_entry.grid(row=row, column=1, padx=10, pady=8, sticky="w")
        tk.Button(root, text="浏览", command=self.browse_dir, width=8).grid(row=row, column=2, padx=5)
        row += 1
        
        # 输出目录
        tk.Label(root, text="输出目录:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.output_entry = tk.Entry(root, width=35)
        self.output_entry.grid(row=row, column=1, padx=10, pady=8, sticky="w")
        tk.Button(root, text="浏览", command=self.browse_output, width=8).grid(row=row, column=2, padx=5)
        row += 1
        
        # ===== 水印设置 =====
        tk.Label(root, text="【水印设置】", font=("Arial", 10, "bold")).grid(
            row=row, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")
        row += 1
        
        # 水印颜色
        tk.Label(root, text="水印颜色:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.color_entry = tk.Entry(root, width=15)
        default_color = self.config.get("watermark", {}).get("color", "#808080")
        self.color_entry.insert(0, default_color)
        self.color_entry.grid(row=row, column=1, padx=10, pady=8, sticky="w")
        
        # 颜色预览
        self.color_preview = tk.Label(root, text="  ", bg=default_color, width=3)
        self.color_preview.grid(row=row, column=1, padx=(120, 0), pady=8, sticky="w")
        tk.Button(root, text="选色", command=self.choose_color, width=8).grid(row=row, column=2, padx=5)
        row += 1
        
        # 字体大小
        tk.Label(root, text="字体大小:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.font_size_var = tk.IntVar(value=self.config.get("watermark", {}).get("font_size", 72))
        font_frame = tk.Frame(root)
        font_frame.grid(row=row, column=1, columnspan=2, padx=10, pady=8, sticky="w")
        
        tk.Scale(font_frame, from_=24, to=150, orient="horizontal", 
                 variable=self.font_size_var, length=200,
                 command=self.update_font_label).pack(side="left")
        self.font_label = tk.Label(font_frame, text=f"{self.font_size_var.get()}pt", width=6)
        self.font_label.pack(side="left", padx=10)
        row += 1
        
        # 透明度
        tk.Label(root, text="透明度:").grid(row=row, column=0, padx=10, pady=8, sticky="w")
        self.opacity_var = tk.IntVar(value=int(self.config.get("watermark", {}).get("opacity", 0.4) * 100))
        opacity_frame = tk.Frame(root)
        opacity_frame.grid(row=row, column=1, columnspan=2, padx=10, pady=8, sticky="w")
        
        tk.Scale(opacity_frame, from_=10, to=80, orient="horizontal", 
                 variable=self.opacity_var, length=200,
                 command=self.update_opacity_label).pack(side="left")
        self.opacity_label = tk.Label(opacity_frame, text=f"{self.opacity_var.get()}%", width=6)
        self.opacity_label.pack(side="left", padx=10)
        row += 1
        
        # ===== 操作按钮 =====
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=row, column=0, columnspan=3, pady=15)
        tk.Button(btn_frame, text="开始处理", command=self.process, 
                  width=15, bg="#4CAF50", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="保存设置", command=self.save_settings, 
                  width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="退出", command=root.quit, 
                  width=15).pack(side="left", padx=10)
        row += 1
        
        # ===== 日志 =====
        self.log_text = tk.Text(root, height=6, width=65)
        self.log_text.grid(row=row, column=0, columnspan=3, padx=10, pady=10)
    
    def update_font_label(self, val):
        self.font_label.config(text=f"{int(float(val))}pt")
    
    def update_opacity_label(self, val):
        self.opacity_label.config(text=f"{int(float(val))}%")
    
    def choose_color(self):
        """选择颜色"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(color=self.color_entry.get())
        if color[1]:
            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(0, color[1])
            self.color_preview.config(bg=color[1])
    
    def browse_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls *.csv"), ("All files", "*.*")])
        if file:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file)
    
    def browse_dir(self):
        dir = filedialog.askdirectory()
        if dir:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir)
    
    def browse_output(self):
        dir = filedialog.askdirectory()
        if dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir)
    
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
    
    def save_settings(self):
        """保存设置到配置文件"""
        self.config["watermark"]["color"] = self.color_entry.get().strip()
        self.config["watermark"]["font_size"] = self.font_size_var.get()
        self.config["watermark"]["opacity"] = self.opacity_var.get() / 100.0
        self.save_config()
        self.log("✓ 设置已保存到 config.yaml")
        messagebox.showinfo("成功", "设置已保存！")
    
    def process(self):
        client = self.client_entry.get().strip()
        if not client:
            messagebox.showerror("错误", "请输入客户名称")
            return
        
        file = self.file_entry.get().strip()
        dir = self.dir_entry.get().strip()
        output = self.output_entry.get().strip()
        color = self.color_entry.get().strip()
        font_size = self.font_size_var.get()
        opacity = self.opacity_var.get() / 100.0
        
        if not file and not dir:
            messagebox.showerror("错误", "请选择文件或目录")
            return
        
        # 构建命令
        cmd = [
            sys.executable, 
            "excel_watermark.py", 
            "-n", client,
            "--font-size", str(font_size),
            "--opacity", str(opacity),
        ]
        
        if file:
            cmd.extend(["-f", file])
        if dir:
            cmd.extend(["-d", dir])
        if output:
            cmd.extend(["-o", output])
        if color:
            cmd.extend(["-c", color])
        
        self.log(f"开始处理...")
        self.log(f"  客户: {client}")
        self.log(f"  字体: {font_size}pt, 透明度: {int(opacity*100)}%")
        
        try:
            # 关键修复：使用系统编码，忽略解码错误
            result = subprocess.run(
                cmd, 
                capture_output=True,
                encoding=self.system_encoding,
                errors='replace'  # 忽略解码错误，替换为 ?
            )
            
            if result.returncode == 0:
                self.log("✓ 处理完成！")
                if result.stdout:
                    self.log(result.stdout)
                messagebox.showinfo("成功", "处理完成！")
            else:
                error_msg = result.stderr if result.stderr else "未知错误"
                self.log(f"✗ 错误: {error_msg}")
                messagebox.showerror("错误", error_msg)
        except Exception as e:
            self.log(f"✗ 异常: {str(e)}")
            messagebox.showerror("异常", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelWatermarkGUI(root)
    root.mainloop()
'''
    
    with open(dist_dir / "excel_watermark_gui.py", "w", encoding="utf-8") as f:
        f.write(gui_script)
    print("  ✓ 创建修复版 GUI v1.3")
    
    # 5. 创建说明文件
    readme = '''# Excel 水印工具 - 便携版 v1.3

## v1.3 更新
- ✅ 修复：Windows 编码问题（UnicodeDecodeError）
- ✅ 自动检测系统编码（Windows 用 GBK，Linux/Mac 用 UTF-8）
- ✅ 忽略解码错误，避免崩溃

## 使用方法

### 方式一：GUI 界面（推荐）
双击 `run_gui.bat` 启动图形界面

### 方式二：命令行
双击 `excel_watermark.bat` 启动，然后输入命令：
```
excel_watermark.exe -n "张三" -f report.xlsx --font-size 100 --opacity 0.5
```

## 参数说明
- `-n` 客户名称（必需）
- `-f` 文件路径
- `-d` 目录路径
- `-o` 输出目录
- `-c` 水印颜色
- `--font-size` 字体大小（24-150）
- `--opacity` 透明度（0.1-1.0）

## 系统要求
- Windows 7/10/11
- Python 3.8+（首次运行会自动安装依赖）

## 首次使用
1. 安装 Python: https://www.python.org/downloads/
2. 双击启动脚本，会自动安装依赖
'''
    
    with open(dist_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("  ✓ 创建说明文件 README.md")
    
    # 6. 打包
    print("\n📦 打包中...")
    import zipfile
    zip_path = src_dir / "dist" / "excel-watermark-portable.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in dist_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(dist_dir))
    
    print(f"\n✅ 完成！")
    print(f"   便携版目录: {dist_dir}")
    print(f"   压缩包: {zip_path}")
    print(f"   大小: {zip_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    build_portable()
