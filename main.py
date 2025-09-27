#!/usr/bin/env python3
"""
透析供給装置薬液補充アプリ - メインエントリーポイント
"""

import sys
import os

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Androidアプリを起動
if __name__ == "__main__":
    try:
        from src.android_app_english import main
        main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Falling back to desktop version...")
        try:
            from src.main_app import main
            main()
        except ImportError as e2:
            print(f"Desktop version also failed: {e2}")
            sys.exit(1)
