# 项目贡献者信息更新系统

## 概述

本项目实现了一个自动化的贡献者信息更新系统，用于定期从GitHub仓库和QQ频道获取贡献者信息，并更新到`contributors.yaml`文件中。

## 功能特点

- **GitHub贡献者获取**: 自动从指定的GitHub仓库获取贡献者信息
- **QQ频道作者获取**: 支持从QQ频道获取作者信息（需要配置API令牌）
- **自动去重**: 同一贡献者在多个仓库的贡献会合并计算
- **定时更新**: 通过GitHub Action每天自动运行
- **错误处理**: 完善的错误处理和备用机制
- **网络优化**: 针对国内网络环境进行优化

## 文件结构

```
.
├── contributors.yaml                    # 贡献者信息文件
├── src/one_dragon_qt/utils/
│   └── update_contributors.py          # 主要更新脚本
├── .github/workflows/
│   └── update-contributors.yml         # GitHub Action工作流
├── config/
│   └── qq_channel_config.yaml          # QQ频道配置
└── docs/
    └── contributors-system.md          # 本文档
```

## 配置说明

### 1. GitHub配置

系统默认从以下两个GitHub仓库获取贡献者信息：
- `OneDragon-Anything/ZenlessZoneZero-OneDragon`
- `OneDragon-Anything/onedragon-anything.github.io`

如果需要修改，请编辑`src/one_dragon_qt/utils/update_contributors.py`中的`GITHUB_REPOS`列表。

### 2. QQ频道配置

QQ频道功能需要配置以下环境变量：
- `QQ_CHANNEL_TOKEN`: QQ频道API访问令牌
- `QQ_CHANNEL_API`: QQ频道API端点（可选，有默认值）

详细的API配置可以在`config/qq_channel_config.yaml`中修改。

## 使用方法

### 本地运行

1. 安装依赖：
```bash
pip install requests pyyaml
```

2. 运行更新脚本：
```bash
python src/one_dragon_qt/utils/update_contributors.py
```

3. 如果需要使用QQ频道功能，设置环境变量：
```bash
export QQ_CHANNEL_TOKEN="your_qq_channel_token"
export QQ_CHANNEL_API="https://your-qq-channel-api.com/authors"
python src/one_dragon_qt/utils/update_contributors.py
```

### GitHub Action自动运行

系统已配置GitHub Action，会在以下情况自动运行：
- 每天UTC 02:00（北京时间10:00）
- 推送到main/master分支时
- 手动触发工作流时

## 环境变量

| 变量名 | 说明 | 是否必需 | 默认值 |
|--------|------|----------|--------|
| `GITHUB_TOKEN` | GitHub访问令牌 | 否 | 自动提供 |
| `QQ_CHANNEL_TOKEN` | QQ频道API令牌 | 否 | 无 |
| `QQ_CHANNEL_API` | QQ频道API端点 | 否 | `https://api.qq-channel.com/authors` |

## 输出格式

`contributors.yaml`文件包含以下信息：

```yaml
github_contributors:
  - login: "username"
    name: "Display Name"
    avatar_url: "https://avatars.githubusercontent.com/..."
    html_url: "https://github.com/username"
    contributions: 123
    repo: "owner/repo"

qq_channel_authors:
  - id: "author_id"
    name: "Author Name"
    avatar_url: "https://example.com/avatar.png"
    channel_url: "https://qchannel.qq.com/..."
    contribution: "内容创作"

last_updated: "2025-12-14T12:00:00Z"
update_note: "此文件由GitHub Action自动更新，请勿手动修改"
```

## 故障排除

### 常见问题

1. **GitHub API限制**
   - 如果没有提供`GITHUB_TOKEN`，可能会遇到API限制
   - 解决方案：在GitHub Action中会自动提供令牌

2. **QQ频道API失败**
   - 如果没有配置`QQ_CHANNEL_TOKEN`，会使用模拟数据
   - 检查网络连接和API端点配置

3. **文件权限问题**
   - 确保脚本有权限写入`contributors.yaml`
   - 在GitHub Action中会自动处理权限

### 日志查看

脚本会输出详细的日志信息，包括：
- 获取到的贡献者数量
- API调用状态
- 错误信息
- 更新时间

## 扩展开发

### 添加新的GitHub仓库

编辑`src/one_dragon_qt/utils/update_contributors.py`，修改`GITHUB_REPOS`列表：

```python
GITHUB_REPOS = [
    "OneDragon-Anything/ZenlessZoneZero-OneDragon",
    "OneDragon-Anything/onedragon-anything.github.io",
    "your-username/your-repo"  # 添加新仓库
]
```

### 修改QQ频道API适配

如果需要适配不同的QQ频道API格式，可以修改：
1. `config/qq_channel_config.yaml`中的字段映射
2. `fetch_qq_channel_authors()`函数中的数据解析逻辑

### 添加新的贡献者来源

1. 创建新的获取函数（参考`fetch_github_contributors`）
2. 在`update_contributors_yaml()`中调用新函数
3. 更新`contributors.yaml`的结构

## 注意事项

1. **自动更新**: 此文件由GitHub Action自动更新，请勿手动修改`contributors.yaml`
2. **网络环境**: 针对国内网络环境进行了优化，但仍可能需要代理
3. **API限制**: 注意各API的调用频率限制
4. **数据隐私**: 确保遵守相关平台的数据使用政策

## 更新日志

- 2025-12-14: 初始版本，支持GitHub和QQ频道贡献者获取
- 2025-12-15: 添加错误处理和配置管理功能

## 联系方式

如有问题，请在GitHub仓库中创建Issue或提交PR。