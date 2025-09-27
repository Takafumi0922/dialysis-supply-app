"""
透析供給装置薬液補充アプリ メインアプリケーション
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import yaml
import os
from typing import Optional

from src.camera_manager import CameraManager
from src.medicine_selector import MedicineSelector, MedicineType


class MainApplication:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        """アプリケーションの初期化"""
        self.root = tk.Tk()
        self.camera_manager: Optional[CameraManager] = None
        self.medicine_selector = MedicineSelector()
        self.is_camera_active = False
        
        # 設定ファイルの読み込み
        self.config = self.load_config()
        
        # UIの初期化
        self.setup_ui()
        
        # カメラ管理の初期化
        self.setup_camera()
    
    def load_config(self) -> dict:
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
    
    def get_default_config(self) -> dict:
        """デフォルト設定を取得"""
        return {
            'camera': {'device_id': 0, 'width': 640, 'height': 480, 'fps': 30},
            'ui': {'window_width': 800, 'window_height': 600, 'title': '透析供給装置薬液補充アプリ'}
        }
    
    def setup_ui(self):
        """UIのセットアップ"""
        # ウィンドウ設定
        self.root.title(self.config['ui']['title'])
        self.root.geometry(f"{self.config['ui']['window_width']}x{self.config['ui']['window_height']}")
        self.root.resizable(True, True)
        
        # メインフレーム
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 薬液選択フレーム
        self.setup_medicine_selection_frame()
        
        # カメラ表示フレーム
        self.setup_camera_frame()
        
        # 制御ボタンフレーム
        self.setup_control_frame()
        
        # グリッドの重み設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
    
    def setup_medicine_selection_frame(self):
        """薬液選択フレームのセットアップ"""
        selection_frame = ttk.LabelFrame(self.main_frame, text="薬液選択", padding="10")
        selection_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 薬液選択ボタン
        self.medicine_var = tk.StringVar()
        
        sodium_btn = ttk.Radiobutton(
            selection_frame, 
            text="次亜塩素酸ナトリウム", 
            variable=self.medicine_var, 
            value="次亜塩素酸ナトリウム",
            command=self.on_medicine_selected
        )
        sodium_btn.grid(row=0, column=0, padx=(0, 20))
        
        acetic_btn = ttk.Radiobutton(
            selection_frame, 
            text="酢酸", 
            variable=self.medicine_var, 
            value="酢酸",
            command=self.on_medicine_selected
        )
        acetic_btn.grid(row=0, column=1)
        
        # 補充開始ボタン
        self.start_btn = ttk.Button(
            selection_frame, 
            text="補充開始", 
            command=self.start_supply,
            state="disabled"
        )
        self.start_btn.grid(row=0, column=2, padx=(20, 0))
    
    def setup_camera_frame(self):
        """カメラ表示フレームのセットアップ"""
        camera_frame = ttk.LabelFrame(self.main_frame, text="カメラ映像", padding="10")
        camera_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # カメラ表示ラベル
        self.camera_label = ttk.Label(camera_frame, text="カメラを起動してください", anchor="center")
        self.camera_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # グリッドの重み設定
        camera_frame.columnconfigure(0, weight=1)
        camera_frame.rowconfigure(0, weight=1)
    
    def setup_control_frame(self):
        """制御ボタンフレームのセットアップ"""
        control_frame = ttk.Frame(self.main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # カメラ起動/停止ボタン
        self.camera_btn = ttk.Button(
            control_frame, 
            text="カメラ起動", 
            command=self.toggle_camera
        )
        self.camera_btn.grid(row=0, column=0, padx=(0, 10))
        
        # 終了ボタン
        exit_btn = ttk.Button(
            control_frame, 
            text="終了", 
            command=self.on_closing
        )
        exit_btn.grid(row=0, column=1)
    
    def setup_camera(self):
        """カメラ管理のセットアップ"""
        camera_config = self.config['camera']
        self.camera_manager = CameraManager(
            device_id=camera_config['device_id'],
            width=camera_config['width'],
            height=camera_config['height'],
            fps=camera_config['fps']
        )
        
        # フレーム取得時のコールバックを設定
        self.camera_manager.set_frame_callback(self.on_frame_received)
    
    def on_medicine_selected(self):
        """薬液選択時の処理"""
        selected = self.medicine_var.get()
        if selected:
            medicine_type = MedicineType.SODIUM_HYPOCHLORITE if selected == "次亜塩素酸ナトリウム" else MedicineType.ACETIC_ACID
            self.medicine_selector.select_medicine(medicine_type)
            self.start_btn.config(state="normal")
            print(f"薬液を選択しました: {selected}")
    
    def start_supply(self):
        """補充開始処理"""
        if not self.medicine_selector.is_medicine_selected():
            messagebox.showwarning("警告", "薬液を選択してください")
            return
        
        if not self.is_camera_active:
            messagebox.showwarning("警告", "カメラを起動してください")
            return
        
        selected_medicine = self.medicine_selector.get_selected_medicine_name()
        messagebox.showinfo("補充開始", f"{selected_medicine}の補充を開始します")
        print(f"補充開始: {selected_medicine}")
    
    def toggle_camera(self):
        """カメラの起動/停止切り替え"""
        if not self.is_camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """カメラを起動"""
        if not self.camera_manager.is_camera_available():
            messagebox.showerror("エラー", "カメラが利用できません")
            return
        
        if self.camera_manager.start_camera():
            self.is_camera_active = True
            self.camera_btn.config(text="カメラ停止")
            print("カメラを起動しました")
        else:
            messagebox.showerror("エラー", "カメラの起動に失敗しました")
    
    def stop_camera(self):
        """カメラを停止"""
        self.camera_manager.stop_camera()
        self.is_camera_active = False
        self.camera_btn.config(text="カメラ起動")
        self.camera_label.config(image="", text="カメラを停止しました")
        print("カメラを停止しました")
    
    def on_frame_received(self, frame):
        """フレーム受信時の処理"""
        # BGRからRGBに変換
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # PIL Imageに変換
        image = Image.fromarray(frame_rgb)
        
        # 表示用にリサイズ
        display_width = 640
        display_height = 480
        image = image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        
        # Tkinter用の画像に変換
        photo = ImageTk.PhotoImage(image)
        
        # ラベルに画像を設定
        self.camera_label.config(image=photo, text="")
        self.camera_label.image = photo  # 参照を保持
    
    def on_closing(self):
        """アプリケーション終了時の処理"""
        if self.is_camera_active:
            self.stop_camera()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """アプリケーションを実行"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


def main():
    """メイン関数"""
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        print(f"アプリケーションエラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
