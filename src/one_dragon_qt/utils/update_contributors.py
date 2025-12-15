#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新项目贡献者信息的脚本
用于GitHub Action自动更新contributors.yaml文件
"""

import json
import os
import requests
import yaml
from datetime import datetime
from typing import Dict, List, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# GitHub API配置
GITHUB_API_BASE = "https://api.github.com"
GITHUB_REPOS = [
    "OneDragon-Anything/ZenlessZoneZero-OneDragon",
    "OneDragon-Anything/onedragon-anything.github.io"
]

# QQ频道作者API（模拟实现，实际需要根据具体API调整）
QQ_CHANNEL_API = "https://api.qq-channel.com/authors"  # 示例URL

def fetch_github_contributors(repo: str, token: str = None) -> List[Dict[str, Any]]:
    """
    从GitHub仓库获取贡献者信息
    
    Args:
        repo: 仓库名称 (格式: owner/repo)
        token: GitHub访问令牌（可选，用于提高API限制）
    
    Returns:
        贡献者信息列表
    """
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    contributors = []
    page = 1
    
    try:
        while True:
            url = f"{GITHUB_API_BASE}/repos/{repo}/contributors"
            params = {
                "page": page,
                "per_page": 100
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            page_contributors = response.json()
            if not page_contributors:
                break
            
            for contributor in page_contributors:
                contributors.append({
                    "login": contributor["login"],
                    "name": contributor.get("name", contributor["login"]),
                    "avatar_url": contributor["avatar_url"],
                    "html_url": contributor["html_url"],
                    "contributions": contributor["contributions"],
                    "repo": repo
                })
            
            page += 1
            
            # 检查是否有下一页
            if 'next' not in response.links:
                break
                
    except requests.exceptions.RequestException as e:
        logger.error(f"获取GitHub贡献者信息失败: {e}")
        return []
    
    logger.info(f"从 {repo} 获取到 {len(contributors)} 个贡献者")
    return contributors

def fetch_qq_channel_authors() -> List[Dict[str, Any]]:
    """
    获取QQ频道作者信息
    
    Returns:
        QQ频道作者信息列表
    """
    logger.info("获取QQ频道作者信息...")
    
    # 从环境变量获取配置
    qq_channel_token = os.environ.get('QQ_CHANNEL_TOKEN')
    qq_channel_api = os.environ.get('QQ_CHANNEL_API', 'https://api.qq-channel.com/authors')
    
    # 如果没有配置令牌，使用模拟数据
    if not qq_channel_token:
        logger.warning("未找到QQ_CHANNEL_TOKEN环境变量，使用模拟数据")
        mock_authors = [
            {
                "id": "qq_author_1",
                "name": "QQ频道作者1",
                "avatar_url": "https://example.com/avatar1.png",
                "channel_url": "https://qchannel.qq.com/test1",
                "contribution": "内容创作"
            },
            {
                "id": "qq_author_2",
                "name": "QQ频道作者2",
                "avatar_url": "https://example.com/avatar2.png",
                "channel_url": "https://qchannel.qq.com/test2",
                "contribution": "技术支持"
            }
        ]
        logger.info(f"获取到 {len(mock_authors)} 个QQ频道作者")
        return mock_authors
    
    # 实际API调用
    try:
        headers = {
            "Authorization": f"Bearer {qq_channel_token}",
            "Content-Type": "application/json",
            "User-Agent": "OneDragon-Contributors-Bot/1.0"
        }
        
        # 添加重试机制
        session = requests.Session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
        
        response = session.get(qq_channel_api, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # 解析QQ频道API返回的数据格式
        authors = []
        if isinstance(data, list):
            for item in data:
                author = {
                    "id": str(item.get("id", "")),
                    "name": item.get("name", ""),
                    "avatar_url": item.get("avatar", ""),
                    "channel_url": item.get("channel_url", ""),
                    "contribution": item.get("role", "内容创作"),
                    "join_date": item.get("join_date", ""),
                    "description": item.get("description", "")
                }
                authors.append(author)
        elif isinstance(data, dict) and "authors" in data:
            # 如果返回的是包含authors字段的对象
            for item in data["authors"]:
                author = {
                    "id": str(item.get("id", "")),
                    "name": item.get("name", ""),
                    "avatar_url": item.get("avatar", ""),
                    "channel_url": item.get("channel_url", ""),
                    "contribution": item.get("role", "内容创作"),
                    "join_date": item.get("join_date", ""),
                    "description": item.get("description", "")
                }
                authors.append(author)
        
        logger.info(f"成功获取到 {len(authors)} 个QQ频道作者")
        return authors
        
    except requests.exceptions.RequestException as e:
        logger.error(f"获取QQ频道作者信息失败: {e}")
        logger.info("使用备用模拟数据")
        # 如果API调用失败，返回模拟数据
        return [
            {
                "id": "qq_author_backup",
                "name": "QQ频道备用作者",
                "avatar_url": "https://example.com/avatar_backup.png",
                "channel_url": "https://qchannel.qq.com/backup",
                "contribution": "API访问失败时使用"
            }
        ]
    except Exception as e:
        logger.error(f"解析QQ频道作者数据失败: {e}")
        return []

def update_contributors_yaml(github_token: str = None) -> bool:
    """
    更新contributors.yaml文件
    
    Args:
        github_token: GitHub访问令牌（可选）
    
    Returns:
        是否成功更新
    """
    try:
        # 获取GitHub贡献者
        all_github_contributors = []
        for repo in GITHUB_REPOS:
            repo_contributors = fetch_github_contributors(repo, github_token)
            all_github_contributors.extend(repo_contributors)
        
        # 去重（同一个人可能在多个仓库贡献）
        unique_contributors = {}
        for contributor in all_github_contributors:
            login = contributor["login"]
            if login not in unique_contributors:
                unique_contributors[login] = contributor
            else:
                # 合并贡献数
                unique_contributors[login]["contributions"] += contributor["contributions"]
        
        github_contributors = list(unique_contributors.values())
        
        # 获取QQ频道作者
        qq_channel_authors = fetch_qq_channel_authors()
        
        # 构建更新数据
        contributors_data = {
            "github_contributors": github_contributors,
            "qq_channel_authors": qq_channel_authors,
            "last_updated": datetime.now().isoformat(),
            "update_note": "此文件由GitHub Action自动更新，请勿手动修改"
        }
        
        # 写入YAML文件
        yaml_path = "contributors.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(contributors_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
        logger.info(f"成功更新 {yaml_path}")
        logger.info(f"GitHub贡献者: {len(github_contributors)} 人")
        logger.info(f"QQ频道作者: {len(qq_channel_authors)} 人")
        
        return True
        
    except Exception as e:
        logger.error(f"更新contributors.yaml失败: {e}")
        return False

def main():
    """主函数"""
    # 从环境变量获取GitHub令牌
    github_token = os.environ.get('GITHUB_TOKEN')
    
    # 更新contributors.yaml
    success = update_contributors_yaml(github_token)
    
    if success:
        logger.info("贡献者信息更新完成")
        exit(0)
    else:
        logger.error("贡献者信息更新失败")
        exit(1)

if __name__ == "__main__":
    main()