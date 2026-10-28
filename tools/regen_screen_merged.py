# -*- coding: utf-8 -*-
"""重生成 _od_merged.yml（运行时唯一加载的画面区域合并文件）

背景：
- 框架运行时只读 assets/game_data/screen_info/_od_merged.yml，往分离文件
  （如 drive_disc_dismantle.yml）新增区域后必须重生成合并文件才会生效。
- ScreenContext 的工作目录解析固定指向 E:\\Z1D\\app，因此本脚本在 Z1D 侧
  生成后复制回 ZODE，两仓分离文件保持一致。

用法：
    /e/Z1D/.venv/Scripts/python.exe tools/regen_screen_merged.py

2026-10-27 拆解修复时手工完成过一次（提交 1012a1f1），本脚本固化该步骤。
"""
import shutil
import subprocess
import sys

ZZZ1D = r'E:\Z1D\app'
ZODE = r'E:\Z1D\zode'
MERGED_REL = r'assets\game_data\screen_info\_od_merged.yml'

REGEN_SNIPPET = '''
from one_dragon.base.screen.screen_loader import ScreenContext
sc = ScreenContext()
sc.reload(from_separated_files=True)
sc.save(reload_after_save=False)
print("merged screens:", len(sc.screen_info_list))
'''


def main() -> int:
    result = subprocess.run(
        [rf'{ZZZ1D}\.venv\Scripts\python.exe', '-c', REGEN_SNIPPET],
        cwd=ZZZ1D,
        env={**__import__('os').environ, 'PYTHONPATH': rf'{ZZZ1D}\src'},
        capture_output=True, text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr[-2000:])
        return 1

    src = rf'{ZZZ1D}\{MERGED_REL}'
    dst = rf'{ZODE}\{MERGED_REL}'
    shutil.copyfile(src, dst)
    print(f'已同步: {src} -> {dst}')

    check = subprocess.run(['git', '-C', ZODE, 'diff', '--stat', '--', MERGED_REL.replace('\\', '/')],
                           capture_output=True, text=True)
    print('git diff:', check.stdout.strip() or '(无变化)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
