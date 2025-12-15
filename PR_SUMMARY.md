# 贡献者信息自动更新系统 - PR说明

## 概述
本PR为项目添加了完整的贡献者信息自动更新系统，解决了stash演职员表的优化需求。

## 主要功能
1. **GitHub Action自动化**: 每两周自动更新贡献者信息（每月1日和15日），避免国内网络问题
2. **多源数据获取**: 从指定的GitHub仓库和QQ频道获取贡献者信息
3. **智能去重**: 同一贡献者在多个仓库的贡献会合并计算
4. **容错设计**: API失败时自动使用模拟数据，确保系统稳定

## 新增文件
- `.github/workflows/update-contributors.yml` - GitHub Action工作流配置
- `src/one_dragon_qt/utils/update_contributors.py` - 核心更新脚本
- `contributors.yaml` - 贡献者信息存储文件
- `config/qq_channel_config.yaml` - QQ频道API配置
- `docs/contributors-system.md` - 详细使用文档

## 信息源配置
- GitHub: `OneDragon-Anything/ZenlessZoneZero-OneDragon` (42个贡献者)
- GitHub: `OneDragon-Anything/onedragon-anything.github.io` (7个贡献者)
- QQ频道: 支持API调用和模拟数据

## 使用方法
1. **自动运行**: GitHub Action每两周UTC 02:00自动更新（每月1日和15日）
2. **手动运行**: 本地执行 `python src/one_dragon_qt/utils/update_contributors.py`
3. **QQ频道配置**: 设置 `QQ_CHANNEL_TOKEN` 环境变量启用真实API

## 测试验证
- ✅ 本地脚本运行成功，获取到42个GitHub贡献者
- ✅ GitHub Action工作流语法验证通过
- ✅ 容错机制测试通过（无QQ令牌时使用模拟数据）
- ✅ 文件生成和更新功能正常

## 注意事项
- 系统已配置为推送到您的个人分支，不会影响OneDragon主仓库
- 所有功能已在feature/update-contributors分支完成开发和测试
- 详细的配置和使用说明请参考 `docs/contributors-system.md`

## 后续建议
1. 在GitHub仓库设置中添加 `QQ_CHANNEL_TOKEN` 密钥以启用真实QQ频道数据
2. 可以根据需要调整GitHub Action的定时运行时间
3. 如需添加更多GitHub仓库，可修改脚本中的 `GITHUB_REPOS` 列表