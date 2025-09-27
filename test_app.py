#!/usr/bin/env python3
"""
透析供給装置薬液補充アプリ テストスクリプト
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


def test_camera_manager():
    """カメラ管理機能のテスト"""
    print("=== カメラ管理機能テスト ===")
    
    camera_manager = CameraManager(device_id=0, width=640, height=480, fps=30)
    
    # カメラの利用可能性チェック
    is_available = camera_manager.is_camera_available()
    print(f"カメラ利用可能性: {is_available}")
    
    if is_available:
        # カメラ起動テスト
        print("カメラ起動テストを実行中...")
        start_result = camera_manager.start_camera()
        
        if start_result:
            print("✅ カメラ起動: 成功")
            
            # カメラ情報の取得
            info = camera_manager.get_camera_info()
            print(f"カメラ情報: {info}")
            
            # フレーム取得テスト
            print("フレーム取得テストを実行中...")
            for i in range(5):  # 5フレーム取得テスト
                frame = camera_manager.get_current_frame()
                if frame is not None:
                    print(f"フレーム {i+1}: 取得成功 (形状: {frame.shape})")
                else:
                    print(f"フレーム {i+1}: 取得失敗")
                time.sleep(0.1)
            
            # カメラ停止
            camera_manager.stop_camera()
            print("✅ カメラ停止: 成功")
        else:
            print("❌ カメラ起動: 失敗")
    else:
        print("⚠️ カメラが利用できません。テストをスキップします。")
    
    print("✅ カメラ管理機能テスト: 完了")


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


def main():
    """メインテスト関数"""
    print("透析供給装置薬液補充アプリ - 動作確認テスト")
    print("=" * 50)
    
    try:
        # 設定ファイルテスト
        test_config_loading()
        print()
        
        # 薬液選択機能テスト
        test_medicine_selector()
        print()
        
        # カメラ管理機能テスト
        test_camera_manager()
        print()
        
        print("=" * 50)
        print("✅ 全テスト完了")
        
    except Exception as e:
        print(f"❌ テスト実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
