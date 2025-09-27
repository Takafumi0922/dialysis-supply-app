"""
カメラ管理クラス
リアルタイムカメラ映像の取得と表示を管理
"""

import cv2
import numpy as np
from typing import Optional, Callable
import threading
import time


class CameraManager:
    """カメラ管理クラス"""
    
    def __init__(self, device_id: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        """
        カメラ管理クラスの初期化
        
        Args:
            device_id: カメラデバイスID
            width: 映像幅
            height: 映像高さ
            fps: フレームレート
        """
        self.device_id = device_id
        self.width = width
        self.height = height
        self.fps = fps
        
        self.camera: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.capture_thread: Optional[threading.Thread] = None
        self.frame_callback: Optional[Callable[[np.ndarray], None]] = None
        self.current_frame: Optional[np.ndarray] = None
        self.lock = threading.Lock()
    
    def start_camera(self) -> bool:
        """
        カメラを起動
        
        Returns:
            bool: 起動成功の場合True
        """
        try:
            self.camera = cv2.VideoCapture(self.device_id)
            if not self.camera.isOpened():
                print(f"カメラデバイス {self.device_id} を開けませんでした")
                return False
            
            # カメラ設定
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            
            self.is_running = True
            
            # キャプチャスレッドを開始
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            print(f"カメラを起動しました (デバイスID: {self.device_id})")
            return True
            
        except Exception as e:
            print(f"カメラ起動エラー: {e}")
            return False
    
    def stop_camera(self):
        """カメラを停止"""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        print("カメラを停止しました")
    
    def set_frame_callback(self, callback: Callable[[np.ndarray], None]):
        """
        フレーム取得時のコールバック関数を設定
        
        Args:
            callback: フレーム取得時に呼ばれる関数
        """
        self.frame_callback = callback
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """
        現在のフレームを取得
        
        Returns:
            np.ndarray: 現在のフレーム（BGR形式）
        """
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def _capture_loop(self):
        """カメラキャプチャのメインループ"""
        frame_interval = 1.0 / self.fps
        
        while self.is_running and self.camera:
            start_time = time.time()
            
            ret, frame = self.camera.read()
            if not ret:
                print("フレームの取得に失敗しました")
                break
            
            # フレームをリサイズ
            frame = cv2.resize(frame, (self.width, self.height))
            
            # フレームを保存
            with self.lock:
                self.current_frame = frame.copy()
            
            # コールバック関数を呼び出し
            if self.frame_callback:
                try:
                    self.frame_callback(frame)
                except Exception as e:
                    print(f"フレームコールバックエラー: {e}")
            
            # フレームレート制御
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_interval - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def is_camera_available(self) -> bool:
        """
        カメラが利用可能かチェック
        
        Returns:
            bool: カメラが利用可能な場合True
        """
        try:
            test_camera = cv2.VideoCapture(self.device_id)
            if test_camera.isOpened():
                test_camera.release()
                return True
            return False
        except:
            return False
    
    def get_camera_info(self) -> dict:
        """
        カメラ情報を取得
        
        Returns:
            dict: カメラ情報
        """
        if not self.camera or not self.camera.isOpened():
            return {}
        
        return {
            "device_id": self.device_id,
            "width": int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": self.camera.get(cv2.CAP_PROP_FPS),
            "is_opened": self.camera.isOpened()
        }
