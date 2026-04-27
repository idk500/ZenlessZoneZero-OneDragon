# AGENTS.md

本文件为 AI 编码助手（Copilot、Claude Code、Cursor、Qwen Coder、Gemini CLI 等）提供项目上下文。
详细开发规范见 [docs/develop/spec/agent_guidelines.md](docs/develop/spec/agent_guidelines.md)。

## 项目简介

**绝区零一条龙 (ZenlessZoneZero-OneDragon)** —— 绝区零游戏自动化工具。
核心功能：自动战斗、闪避辅助（声音+图像ML识别）、日常一条龙、空洞零号（LLM识别）、定时任务、多账号管理。
运行平台：**Windows**，分辨率基准 **1080p**。

## 技术栈

- **语言**: Python 3.11（不使用 3.12+）
- **包管理**: [uv](https://github.com/astral-sh/uv)（不是 pip）
- **GUI**: PySide6 + [pyside6-fluent-widgets](https://qfluentwidgets.com/)（Fluent Design 风格）
- **ML 推理**: onnxruntime-directml（GPU）、OpenCV
- **OCR**: 自研 onnxocr（PaddleOCR 移植）
- **格式化/Lint**: Ruff（Black 兼容，行长 88）
- **测试**: pytest + pytest-asyncio（测试代码在独立仓库 [zzz-od-test](https://github.com/OneDragon-Anything/zzz-od-test)）

## 项目结构

```
src/
  one_dragon/      # 核心框架（基类、工具、YOLO、环境、启动器）
  one_dragon_qt/   # Qt GUI 框架（通用组件、视图、服务）
  onnxocr/         # ONNX OCR 引擎
  zzz_od/          # 游戏业务逻辑（自动战斗、空洞零号、控制器、截图区域等）
config/            # 运行时配置 YAML
assets/            # 游戏资源（模板图片、模型、文本）
docs/              # 开发文档（docs/develop/）
deploy/            # PyInstaller 打包配置
zzz-od-test/       # 测试仓库（需单独克隆到根目录）
```

## 常用命令

```shell
uv sync --group dev                              # 安装依赖
uv run --env-file .env src/zzz_od/gui/app.py     # 运行 GUI
uv run --env-file .env pytest zzz-od-test/        # 运行测试
uv run ruff check src/                            # Lint
uv run ruff format src/                           # 格式化
```

优先使用 Windows PowerShell 支持的指令。环境变量在 `.env` 文件中。

## 关键编码规范

- **类型提示**: 所有函数签名和类成员变量**必须**有类型注解。使用 `list[str]` 不用 `List[str]`，`X | Y` 不用 `Union`。
- **中文注释**: 注释和 docstring 使用中文（Google 风格），可以中英混用。不要建议翻译。
- **绝对导入**: 禁止相对导入。仅类型注解的导入用 `TYPE_CHECKING`。
- **构造函数**: 显式声明所有参数，避免 `**kwargs`。
- **路径**: 用 `pathlib`，不用 `os.path`。
- **字符串**: 用 f-string。
- **异常处理**: 不做无意义的 try-catch，能处理才 catch，否则让异常冒泡。
- **`__init__.py`**: 除非明确指示，不暴露模块。
- **Fluent Design**: GUI 组件优先用 pyside6-fluent-widgets 现有组件，新组件遵循 Fluent Design。
- **硬编码**: 允许硬编码 1080p 像素坐标和按键名，不要建议分辨率适配。

## 审查重点

- **只关注**: 逻辑错误、死循环、运行时崩溃、资源泄漏
- **不关注**: 代码风格（交给 Ruff）、过度工程化的最佳实践、Magic Number

## PR 流程

- Reviewer 通过 start review 提交意见，解决后由 reviewer 点 resolve
- 提交者需回复或修改所有 review comment
