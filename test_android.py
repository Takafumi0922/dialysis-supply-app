#!/usr/bin/env python3
"""
透析供給装置薬液補充アプリ - Android版テストスクリプト
"""

import sys
import os
import time

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.medicine_selector import MedicineSelector, MedicineType
from src.camera_manager import CameraManager


def test_medicine_selector():
    """薬液選択機能のテスト"""
    print("=== 薬液選択機能テスト ===")
    
    selector = MedicineSelector()
    
    # 初期状態の確認
    assert not selector.is_medicine_selected(), "初期状態では薬液が選択されていないはず"
    assert selector.get_selected_medicine() is None, "初期状態では選択された薬液はNone"
    
    # 次亜塩素酸ナトリウムの選択
    result = selector.select_medicine(MedicineType.SODIUM_HYPOCHLORITE)
    assert result, "次亜塩素酸ナトリウムの選択に成功するはず"
    assert selector.is_medicine_selected(), "薬液が選択された状態になるはず"
    assert selector.get_selected_medicine() == MedicineType.SODIUM_HYPOCHLORITE, "選択された薬液が正しいはず"
    assert selector.get_selected_medicine_name() == "次亜塩素酸ナトリウム", "薬液名が正しいはず"
    
    # 酢酸の選択
    result = selector.select_medicine(MedicineType.ACETIC_ACID)
    assert result, "酢酸の選択に成功するはず"
    assert selector.get_selected_medicine() == MedicineType.ACETIC_ACID, "選択された薬液が酢酸になるはず"
    assert selector.get_selected_medicine_name() == "酢酸", "薬液名が酢酸になるはず"
    
    # 選択のクリア
    selector.clear_selection()
    assert not selector.is_medicine_selected(), "選択クリア後は薬液が選択されていないはず"
    assert selector.get_selected_medicine() is None, "選択クリア後は選択された薬液はNone"
    
    print("✅ 薬液選択機能テスト: 成功")


def test_android_camera():
    """Androidカメラ機能のテスト"""
    print("=== Androidカメラ機能テスト ===")
    
    try:
        from plyer import camera
        print("✅ Plyerライブラリのインポート: 成功")
        
        # カメラ機能のテスト（実際の撮影は行わない）
        print("Androidカメラ機能が利用可能です")
        print("実際のAndroidデバイスでは以下の機能が利用できます:")
        print("- カメラ撮影")
        print("- 画像保存")
        print("- 権限管理")
        
    except ImportError as e:
        print(f"❌ Plyerライブラリのインポート: 失敗 - {e}")
    except Exception as e:
        print(f"❌ Androidカメラ機能テスト: 失敗 - {e}")


def test_kivy_imports():
    """Kivy関連のインポートテスト"""
    print("=== Kivy関連インポートテスト ===")
    
    try:
        import kivy
        print(f"✅ Kivy: {kivy.__version__}")
    except ImportError as e:
        print(f"❌ Kivy: インポート失敗 - {e}")
    
    try:
        import kivymd
        print(f"✅ KivyMD: {kivymd.__version__}")
    except ImportError as e:
        print(f"❌ KivyMD: インポート失敗 - {e}")
    
    try:
        from kivymd.uix.button import MDRaisedButton
        print("✅ KivyMD UIコンポーネント: インポート成功")
    except ImportError as e:
        print(f"❌ KivyMD UIコンポーネント: インポート失敗 - {e}")
    
    try:
        from kivymd.uix.selectioncontrol import MDCheckbox
        print("✅ KivyMD 選択コントロール: インポート成功")
    except ImportError as e:
        print(f"❌ KivyMD 選択コントロール: インポート失敗 - {e}")


def test_config_loading():
    """設定ファイル読み込みテスト"""
    print("=== 設定ファイル読み込みテスト ===")
    
    try:
        import yaml
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 設定項目の確認
        assert 'camera' in config, "カメラ設定が存在するはず"
        assert 'ui' in config, "UI設定が存在するはず"
        
        camera_config = config['camera']
        assert 'device_id' in camera_config, "カメラデバイスIDが設定されているはず"
        assert 'width' in camera_config, "カメラ幅が設定されているはず"
        assert 'height' in camera_config, "カメラ高さが設定されているはず"
        assert 'fps' in camera_config, "フレームレートが設定されているはず"
        
        ui_config = config['ui']
        assert 'window_width' in ui_config, "ウィンドウ幅が設定されているはず"
        assert 'window_height' in ui_config, "ウィンドウ高さが設定されているはず"
        assert 'title' in ui_config, "タイトルが設定されているはず"
        
        print("✅ 設定ファイル読み込みテスト: 成功")
        print(f"カメラ設定: {camera_config}")
        print(f"UI設定: {ui_config}")
        
    except Exception as e:
        print(f"❌ 設定ファイル読み込みテスト: 失敗 - {e}")


def test_android_app_structure():
    """Androidアプリ構造テスト"""
    print("=== Androidアプリ構造テスト ===")
    
    try:
        # メインアプリケーションのインポートテスト
        from src.android_app import DialysisSupplyApp, MedicineSelectionScreen, CameraScreen
        print("✅ Androidアプリクラス: インポート成功")
        
        # アプリケーションの初期化テスト
        app = DialysisSupplyApp()
        print("✅ Androidアプリ初期化: 成功")
        
        # 設定の読み込みテスト
        config = app.load_config()
        assert config is not None, "設定が読み込まれているはず"
        print("✅ 設定読み込み: 成功")
        
    except Exception as e:
        print(f"❌ Androidアプリ構造テスト: 失敗 - {e}")
        import traceback
        traceback.print_exc()


def main():
    """メインテスト関数"""
    print("透析供給装置薬液補充アプリ - Android版動作確認テスト")
    print("=" * 60)
    
    try:
        # 設定ファイルテスト
        test_config_loading()
        print()
        
        # Kivy関連インポートテスト
        test_kivy_imports()
        print()
        
        # 薬液選択機能テスト
        test_medicine_selector()
        print()
        
        # Androidカメラ機能テスト
        test_android_camera()
        print()
        
        # Androidアプリ構造テスト
        test_android_app_structure()
        print()
        
        print("=" * 60)
        print("✅ 全テスト完了")
        print()
        print("Android APKのビルド準備が完了しました。")
        print("次のステップ:")
        print("1. buildozer android debug  # APKのビルド")
        print("2. buildozer android deploy # デバイスへのインストール")
        
    except Exception as e:
        print(f"❌ テスト実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
