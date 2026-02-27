# MinerU GUI（Windows 可下载运行）

这是一个基于 **MinerU CLI** 的可视化桌面软件，支持在 Windows 上打包为可下载的 `exe`，并提供**应用内一键安装/升级 MinerU**，用户无需手动安装命令行。

## 功能

- 一键安装/升级 MinerU（内置 `python -m pip install -U mineru`）
- 检测 MinerU 是否可用（`mineru --help`）
- 选择输入文档（PDF/图片）
- 选择输出目录
- 配置语言、设备（CPU/CUDA/MPS）和 OCR 开关
- 支持附加自定义参数
- 实时查看运行日志
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

## 给最终用户的使用流程（无需手工装 MinerU）

1. 打开 `MinerU-GUI.exe`。
2. 点击 **“一键安装/升级 MinerU”**，等待日志显示安装完成。
3. 点击 **“检测安装”**，确认 `mineru --help` 可运行。
4. 选择输入文件、输出目录，按需配置参数后点击 **“开始处理”**。

## 注意事项

- 一键安装依赖网络和 pip 源可用性。
- 若企业环境限制网络，可在“MinerU 安装命令”中替换为内部源命令。
- 若 `mineru` 命令不在 PATH，可在“MinerU 可执行命令”填写完整路径（例如 `C:\\path\\to\\mineru.exe`）。
