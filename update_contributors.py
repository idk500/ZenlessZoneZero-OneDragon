#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新贡献者信息脚本
从各个来源抓取贡献者信息，并更新contributer.yaml文件
"""

import urllib.request
import re
import yaml
import os
from datetime import datetime


def fetch_github_contributors(url):
    """
    从GitHub贡献者页面抓取贡献者信息
    
    Args:
        url: GitHub贡献者页面URL
        
    Returns:
        贡献者列表，每个元素是包含name和contributions的字典
    """
    try:
        print(f"正在从 {url} 抓取贡献者信息...")
        response = urllib.request.urlopen(url, timeout=10)
        html_content = response.read().decode('utf-8')
        
        # 解析HTML获取贡献者信息
        contributors = []
        
        # 匹配贡献者名称和贡献次数的模式
        pattern = r'<a class="Link--secondary".*?>(.*?)</a>.*?<span class="text-muted text-small">([0-9,]+) contributions</span>'
        matches = re.finditer(pattern, html_content, re.DOTALL)
        
        for match in matches:
            name = match.group(1).strip()
            contributions = match.group(2).strip().replace(',', '')
            
            if name and contributions:
                contributors.append({
                    'name': name,
                    'contributions': f"{contributions} contributions"
                })
        
        print(f"成功抓取 {len(contributors)} 个贡献者信息")
        return contributors
    except Exception as e:
        print(f"从GitHub抓取贡献者信息失败: {e}")
        return []


def fetch_qq_channel_authors(url):
    """
    从QQ频道抓取作者信息
    
    Args:
        url: QQ频道URL
        
    Returns:
        作者列表，每个元素是包含name的字典
    """
    try:
        print(f"正在从 {url} 抓取作者信息...")
        response = urllib.request.urlopen(url, timeout=10)
        html_content = response.read().decode('utf-8')
        
        # 解析HTML获取作者信息
        authors = []
        
        # 匹配作者名称的模式
        pattern = r'<h3 class="nick hover-underline" data-v-c6240036="">(.*?)</h3>'
        matches = re.finditer(pattern, html_content, re.DOTALL)
        
        for match in matches:
            name = match.group(1).strip()
            if name:
                authors.append({
                    'name': name,
                    'role': '社区作者',
                    'contributions': '社区文章贡献'
                })
        
        print(f"成功抓取 {len(authors)} 个作者信息")
        return authors
    except Exception as e:
        print(f"从QQ频道抓取作者信息失败: {e}")
        return []


def fetch_recent_commits(url):
    """
    从GitHub获取最近的commit信息
    
    Args:
        url: GitHub仓库URL
        
    Returns:
        最近10个commiter列表
    """
    try:
        print(f"正在从 {url} 抓取最近commit信息...")
        # 使用GitHub API获取最近的commits
        api_url = f"{url.replace('https://github.com/', 'https://api.github.com/repos/')}/commits?per_page=10"
        response = urllib.request.urlopen(api_url, timeout=10)
        commits_data = response.read().decode('utf-8')
        
        # 解析JSON数据
        import json
        commits = json.loads(commits_data)
        
        recent_contributors = []
        seen_authors = set()
        
        for commit in commits:
            if 'commit' in commit and 'author' in commit['commit']:
                author_name = commit['commit']['author']['name']
                if author_name not in seen_authors:
                    seen_authors.add(author_name)
                    recent_contributors.append({
                        'name': author_name,
                        'role': '开发者',
                        'contributions': '近期提交'
                    })
        
        print(f"成功抓取 {len(recent_contributors)} 个近期贡献者")
        return recent_contributors
    except Exception as e:
        print(f"抓取最近commit信息失败: {e}")
        return []


def update_contributors_file():
    """
    更新contributer.yaml文件
    """
    # 定义各个来源的URL
    github_repo_url = "https://github.com/OneDragon-Anything/ZenlessZoneZero-OneDragon"
    github_docs_url = "https://github.com/OneDragon-Anything/onedragon-anything.github.io"
    qq_channel_url = "https://pd.qq.com/g/onedrag00n?subc=714508468"
    
    # 抓取各个来源的贡献者信息
    core_contributors = fetch_github_contributors(f"{github_repo_url}/graphs/contributors")
    recent_contributors = fetch_recent_commits(github_repo_url)
    docs_contributors = fetch_github_contributors(f"{github_docs_url}/graphs/contributors")
    community_maintainers = fetch_qq_channel_authors(qq_channel_url)
    
    # 读取现有文件内容
    contributors_file = "contributer.yaml"
    existing_data = {}
    
    if os.path.exists(contributors_file):
        with open(contributors_file, 'r', encoding='utf-8') as f:
            existing_data = yaml.safe_load(f)
    
    # 更新贡献者信息
    contributors_data = {
        '# 项目贡献者信息': '',
        '# 此文件包含项目的所有贡献者信息，用于滚动字幕显示': '',
        '# 更新时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        '# 项目核心贡献者（来自GitHub）': '',
        'core_contributors': core_contributors[:10],  # 只保留前10个核心贡献者
        
        '# 近期贡献者（最后10个commiter）': '',
        'recent_contributors': recent_contributors[:10],  # 只保留前10个近期贡献者
        
        '# 文档组贡献者（来自GitHub文档仓库）': '',
        'documentation_contributors': docs_contributors[:10],  # 只保留前10个文档贡献者
        
        '# 社区维护者（来自QQ频道）': '',
        'community_maintainers': community_maintainers[:10],  # 只保留前10个社区维护者
        
        '# 其他贡献者（手动添加）': '',
        'other_contributors': existing_data.get('other_contributors', [])  # 保留手动添加的贡献者
    }
    
    # 写入更新后的文件
    with open(contributors_file, 'w', encoding='utf-8') as f:
        yaml.dump(contributors_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"成功更新 {contributors_file} 文件")
    print(f"核心贡献者: {len(contributors_data['core_contributors'])}")
    print(f"近期贡献者: {len(contributors_data['recent_contributors'])}")
    print(f"文档贡献者: {len(contributors_data['documentation_contributors'])}")
    print(f"社区维护者: {len(contributors_data['community_maintainers'])}")
    print(f"其他贡献者: {len(contributors_data['other_contributors'])}")


if __name__ == "__main__":
    print("开始更新贡献者信息...")
    update_contributors_file()
    print("贡献者信息更新完成！")
