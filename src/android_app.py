"""
透析供給装置薬液補充アプリ - Android版
KivyベースのAndroid対応アプリケーション
"""

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.theming import ThemeManager
import cv2
import numpy as np
import yaml
from plyer import camera
import threading
import time

from src.medicine_selector import MedicineSelector, MedicineType
from src.camera_manager import CameraManager


class MedicineSelectionScreen(MDScreen):
    """薬液選択画面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.medicine_selector = MedicineSelector()
        self.selected_medicine = None
        self.setup_ui()
    
    def setup_ui(self):
        """UIのセットアップ"""
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=20,
            adaptive_height=True
        )
        
        # タイトル
        title = MDLabel(
            text="薬液選択",
            theme_text_color="Primary",
            size_hint_y=None,
            height=50,
            halign="center",
            font_name="Japanese"
        )
        layout.add_widget(title)
        
        # 薬液選択カード
        card = MDCard(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint_y=None,
            height=200
        )
        
        # 次亜塩素酸ナトリウム選択
        sodium_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )
        
        self.sodium_radio = MDCheckbox(
            group='medicine',
            on_release=self.on_medicine_selected
        )
        sodium_label = MDLabel(
            text="次亜塩素酸ナトリウム",
            theme_text_color="Primary",
            font_name="Japanese"
        )
        
        sodium_layout.add_widget(self.sodium_radio)
        sodium_layout.add_widget(sodium_label)
        
        # 酢酸選択
        acetic_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )
        
        self.acetic_radio = MDCheckbox(
            group='medicine',
            on_release=self.on_medicine_selected
        )
        acetic_label = MDLabel(
            text="酢酸",
            theme_text_color="Primary",
            font_name="Japanese"
        )
        
        acetic_layout.add_widget(self.acetic_radio)
        acetic_layout.add_widget(acetic_label)
        
        card.add_widget(sodium_layout)
        card.add_widget(acetic_layout)
        layout.add_widget(card)
        
        # 補充開始ボタン
        self.start_button = MDRaisedButton(
            text="補充開始",
            size_hint_y=None,
            height=50,
            disabled=True,
            on_release=self.start_supply,
            font_name="Japanese"
        )
        layout.add_widget(self.start_button)
        
        self.add_widget(layout)
    
    def on_medicine_selected(self, instance):
        """薬液選択時の処理"""
        if instance == self.sodium_radio and instance.active:
            # 他の選択をクリア
            self.acetic_radio.active = False
            self.medicine_selector.select_medicine(MedicineType.SODIUM_HYPOCHLORITE)
            self.selected_medicine = "次亜塩素酸ナトリウム"
        elif instance == self.acetic_radio and instance.active:
            # 他の選択をクリア
            self.sodium_radio.active = False
            self.medicine_selector.select_medicine(MedicineType.ACETIC_ACID)
            self.selected_medicine = "酢酸"
        
        if self.selected_medicine:
            self.start_button.disabled = False
            print(f"薬液を選択しました: {self.selected_medicine}")
    
    def start_supply(self, instance):
        """補充開始処理"""
        if not self.medicine_selector.is_medicine_selected():
            self.show_dialog("警告", "薬液を選択してください")
            return
        
        # カメラ画面に遷移
        app = App.get_running_app()
        app.screen_manager.current = 'camera'
        app.camera_screen.start_camera()


class CameraScreen(MDScreen):
    """カメラ画面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_manager = None
        self.is_camera_active = False
        self.setup_ui()
    
    def setup_ui(self):
        """UIのセットアップ"""
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10
        )
        
        # カメラ映像表示
        self.camera_image = Image(
            size_hint=(1, 0.8),
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.camera_image)
        
        # 制御ボタン
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )
        
        self.camera_button = MDRaisedButton(
            text="カメラ起動",
            on_release=self.toggle_camera,
            font_name="Japanese"
        )
        
        self.back_button = MDFlatButton(
            text="戻る",
            on_release=self.go_back,
            font_name="Japanese"
        )
        
        button_layout.add_widget(self.camera_button)
        button_layout.add_widget(self.back_button)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def start_camera(self):
        """カメラを起動"""
        if not self.is_camera_active:
            self.toggle_camera()
    
    def toggle_camera(self, instance=None):
        """カメラの起動/停止切り替え"""
        if not self.is_camera_active:
            self.activate_camera()
        else:
            self.deactivate_camera()
    
    def activate_camera(self):
        """カメラを有効化"""
        try:
            # Androidカメラの起動
            camera.take_picture(
                filename='temp_camera.jpg',
                on_complete=self.on_camera_result
            )
            self.is_camera_active = True
            self.camera_button.text = "カメラ停止"
            print("カメラを起動しました")
        except Exception as e:
            print(f"カメラ起動エラー: {e}")
            self.show_dialog("エラー", "カメラの起動に失敗しました")
    
    def deactivate_camera(self):
        """カメラを無効化"""
        self.is_camera_active = False
        self.camera_button.text = "カメラ起動"
        self.camera_image.texture = None
        print("カメラを停止しました")
    
    def on_camera_result(self, filename):
        """カメラ撮影結果の処理"""
        if os.path.exists(filename):
            # 画像を読み込んで表示
            self.camera_image.source = filename
            print(f"カメラ画像を取得しました: {filename}")
        else:
            print("カメラ画像の取得に失敗しました")
    
    def go_back(self, instance):
        """前の画面に戻る"""
        if self.is_camera_active:
            self.deactivate_camera()
        
        app = App.get_running_app()
        app.screen_manager.current = 'medicine_selection'
    
    def show_dialog(self, title, text):
        """ダイアログを表示"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


class DialysisSupplyApp(MDApp):
    """メインアプリケーションクラス"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.camera_screen = None
        self.medicine_screen = None
        self.config_data = self.load_config()
    
    def load_config(self):
        """設定ファイルを読み込み"""
        try:
            with open('config.yaml', 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("設定ファイルが見つかりません。デフォルト設定を使用します。")
            return self.get_default_config()
        except Exception as e:
            print(f"設定ファイルの読み込みエラー: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """デフォルト設定を取得"""
        return {
            'camera': {'device_id': 0, 'width': 640, 'height': 480, 'fps': 30},
            'ui': {'window_width': 800, 'window_height': 600, 'title': '透析供給装置薬液補充アプリ'}
        }
    
    def build(self):
        """アプリケーションの構築"""
        # テーマ設定
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        # 日本語フォントの設定
        from kivy.core.text import LabelBase
        import os
        
        # 複数の日本語フォントを試行
        japanese_fonts = [
            'C:/Windows/Fonts/msgothic.ttc',
            'C:/Windows/Fonts/meiryo.ttc',
            'C:/Windows/Fonts/yuanti.ttc',
            'C:/Windows/Fonts/meiryob.ttc'
        ]
        
        for font_path in japanese_fonts:
            if os.path.exists(font_path):
                try:
                    LabelBase.register(name='Japanese', fn_regular=font_path)
                    print(f"日本語フォントを登録しました: {font_path}")
                    break
                except Exception as e:
                    print(f"フォント登録エラー: {e}")
                    continue
        
        # 画面管理の設定
        self.screen_manager = ScreenManager()
        
        # 薬液選択画面
        self.medicine_screen = MedicineSelectionScreen(name='medicine_selection')
        self.screen_manager.add_widget(self.medicine_screen)
        
        # カメラ画面
        self.camera_screen = CameraScreen(name='camera')
        self.screen_manager.add_widget(self.camera_screen)
        
        return self.screen_manager
    
    def on_start(self):
        """アプリケーション開始時の処理"""
        print("透析供給装置薬液補充アプリを開始しました")
    
    def on_stop(self):
        """アプリケーション終了時の処理"""
        if self.camera_screen and self.camera_screen.is_camera_active:
            self.camera_screen.deactivate_camera()
        print("アプリケーションを終了しました")


def main():
    """メイン関数"""
    try:
        app = DialysisSupplyApp()
        app.run()
    except Exception as e:
        print(f"アプリケーションエラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
