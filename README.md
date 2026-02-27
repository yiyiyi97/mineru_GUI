# MinerU GUI（Windows 可下载运行）

这是一个基于 **MinerU CLI** 的可视化桌面软件，支持在 Windows 上打包为可下载的 `exe`。

## 功能

- 选择输入文档（PDF/图片）
- 选择输出目录
- 配置语言、设备（CPU/CUDA/MPS）和 OCR 开关
- 支持附加自定义参数
- 实时查看 MinerU 运行日志
- 一键停止任务

## 本地运行

1. 安装 Python 3.10+
2. 安装依赖：

```bash
python -m pip install -r requirements.txt
```

3. 启动 GUI：

```bash
python app.py
```

## 打包为 Windows 可执行文件

在 Windows 的命令行运行：

```bat
build_windows.bat
```

打包成功后可执行文件在：

```text
dist\MinerU-GUI.exe
```

## 使用说明

1. `MinerU 可执行命令`：默认是 `mineru`，如果你安装的是其他路径，可点“浏览”选择 `mineru.exe`。
2. 选择输入文件与输出目录。
3. 根据需要设置语言、设备和 OCR。
4. 点击“开始处理”，日志窗口会显示实时进度。

## 注意事项

- 本软件是 MinerU 的可视化封装，需确保 MinerU 已正确安装并可调用。
- 如果使用 GPU，请确保对应驱动与运行环境已安装。
