#!/usr/bin/env python3
"""
透析供給装置薬液補充アプリ - Android版（英語版）実行スクリプト
"""

import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.android_app_english import main

if __name__ == "__main__":
    main()
