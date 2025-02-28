# Deepseek-R1 模型安装器

这是一个用于简化 Deepseek-R1 大语言模型本地部署的跨平台图形化安装工具。该工具可以帮助用户根据系统配置选择合适的模型版本，并自动完成安装过程。

## 功能特点

- 支持 Windows、Linux 和 macOS 平台
- 自动检测系统配置（CPU、内存、GPU、磁盘空间等）
- 根据系统配置推荐可用的模型版本
- 自动安装必要的依赖（Docker、CUDA、Ollama等）
- 图形化界面，操作简单直观
- 实时显示安装进度
- 支持模型的安装、卸载和管理
- 详细的日志记录

## 系统要求

### Windows
- Windows 10/11 64位
- Python 3.8 或更高版本
- NVIDIA GPU（用于运行大型模型）
- Docker Desktop for Windows
- WSL2（Windows Subsystem for Linux 2）

### Linux
- Ubuntu 22.04 或更高版本
- Python 3.8 或更高版本
- NVIDIA GPU（用于运行大型模型）
- Docker
- NVIDIA Container Toolkit

### macOS
- macOS 11.0 或更高版本
- Python 3.8 或更高版本
- Docker Desktop for Mac
- 建议使用较小的模型（由于 Mac 显卡限制）

所有平台都需要：
- 足够的磁盘空间（根据选择的模型大小而定）
- 稳定的网络连接

## 安装说明

1. 克隆仓库：
```bash
git clone [repository_url]
cd deepseek_installer
```

2. 安装依赖：
```bash
# Windows
pip install -r requirements.txt

# Linux/macOS
pip3 install -r requirements.txt
```

3. 运行安装器：
```bash
# Windows
python -m src

# Linux/macOS
python3 -m src
```

## 平台特定说明

### Windows
- 请确保已安装 Docker Desktop 并启用 WSL2
- NVIDIA 驱动程序需要支持 CUDA
- 建议使用管理员权限运行安装器

### Linux
- 需要安装 NVIDIA 驱动和 CUDA
- 确保当前用户在 docker 用户组中
```bash
sudo usermod -aG docker $USER
```

### macOS
- 由于 GPU 限制，建议使用较小的模型版本
- 确保已安装 Rosetta 2（对于 M1/M2 芯片）

## 使用说明

1. 启动程序后，系统会自动检测您的硬件配置
2. 在下拉菜单中选择要安装的模型版本（仅显示系统支持的版本）
3. 选择安装路径
4. 点击"开始安装"按钮开始安装过程
5. 等待安装完成

## 支持的模型版本

- deepseek-r1:1.5b (需要 4GB 显存)
- deepseek-r1:7b (需要 8GB 显存)
- deepseek-r1:14b (需要 12GB 显存)
- deepseek-r1:32b (需要 24GB 显存)
- deepseek-r1:70b (需要 48GB 显存)
- deepseek-r1:671b (需要 400GB 显存)

## 注意事项

- 安装过程中请确保网络连接稳定
- 建议在安装大型模型前确保有足够的磁盘空间
- 如果安装过程中遇到问题，请查看日志文件了解详细信息
- 首次安装可能需要较长时间，请耐心等待
- Windows 用户可能需要关闭防火墙或添加例外
- macOS 用户首次运行需要在"系统偏好设置"中允许应用运行

## 常见问题

1. Q: 为什么某些模型版本在列表中不可选？
   A: 这是因为您的系统配置不满足该模型的最低要求。

2. Q: 安装过程中断了怎么办？
   A: 程序会自动清理未完成的安装，您可以重新启动安装过程。

3. Q: 如何卸载已安装的模型？
   A: 在主界面中选择已安装的模型，点击"卸载"按钮即可。

4. Q: Windows 下提示"找不到 NVIDIA GPU"怎么办？
   A: 请确保已安装最新的 NVIDIA 驱动，并且在 Docker Desktop 设置中启用了 GPU 支持。

5. Q: macOS 下可以运行大型模型吗？
   A: 由于 macOS 的 GPU 限制，建议使用较小的模型版本（如 1.5b 或 7b）。

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 联系方式

如有问题或建议，请通过 Issue 系统与我们联系。 