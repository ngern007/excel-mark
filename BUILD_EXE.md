# Excel 水印工具 - 打包说明

## 方案一：便携版（推荐，无需打包）

直接下载 `excel-watermark-portable.zip`，解压即用。

**优点：**
- 无需打包，下载即用
- 包含 GUI 界面
- 自动安装依赖

**使用：**
1. 安装 Python 3.8+
2. 解压 zip 文件
3. 双击 `run_gui.bat` 启动图形界面
4. 或双击 `excel_watermark.bat` 使用命令行

---

## 方案二：打包成 .exe（需要 Windows）

如果你想要真正的单文件 .exe，需要在 Windows 上操作：

### 步骤 1：安装打包工具

```bash
pip install pyinstaller
```

### 步骤 2：创建打包配置

创建 `excel_watermark.spec` 文件：

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['excel_watermark.py'],
    pathex=[],
    binaries=[],
    datas=[('config.yaml', '.')],
    hiddenimports=['openpyxl', 'PIL', 'yaml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='excel_watermark',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### 步骤 3：打包

```bash
pyinstaller excel_watermark.spec
```

打包完成后，在 `dist/` 目录下会生成 `excel_watermark.exe`

---

## 方案三：使用 GitHub Actions 自动打包

创建 `.github/workflows/build.yml`：

```yaml
name: Build EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      
      - name: Build EXE
        run: pyinstaller -F excel_watermark.py --add-data "config.yaml;."
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: excel-watermark-exe
          path: dist/excel_watermark.exe
```

推送 tag 后，GitHub Actions 会自动打包并上传。

---

## 推荐方案

| 场景 | 推荐方案 |
|------|----------|
| 临时使用，不想折腾 | 方案一：便携版 |
| 长期使用，想要 .exe | 方案二：Windows 打包 |
| 团队使用，需要分发 | 方案三：GitHub Actions |

---

## 常见问题

### Q: 为什么不能在 Linux 上打包 Windows .exe？
A: PyInstaller 是平台相关的。在 Linux 上只能打包 Linux 可执行文件。

### Q: 便携版需要安装 Python 吗？
A: 是的，但只需要安装一次，后续无需重复安装。

### Q: 能否做成完全无需 Python 的版本？
A: 可以，但需要在 Windows 上打包成 .exe，或使用其他工具如 Nuitka。
