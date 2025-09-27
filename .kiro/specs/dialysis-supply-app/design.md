# 透析供給装置薬液補充アプリ 設計書

## 1. システムアーキテクチャ

### 1.1 全体構成

```
┌─────────────────────────────────────────────────────────────┐
│                    透析供給装置薬液補充アプリ                    │
├─────────────────────────────────────────────────────────────┤
│  UI Layer (Tkinter/PyQt)                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │薬液選択画面  │ │カメラ表示画面 │ │結果表示画面  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │薬液選択管理  │ │画像認識管理  │ │安全確認管理  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  AI/ML Layer                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │YOLO推論     │ │画像前処理   │ │結果後処理   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Hardware Layer                                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │カメラ制御   │ │音声出力    │ │ファイルI/O  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 主要コンポーネント

#### 1.2.1 UI Layer
- **薬液選択画面**: 次亜塩素酸ナトリウム/酢酸の選択
- **カメラ表示画面**: リアルタイム映像表示
- **結果表示画面**: 正解/誤答の表示

#### 1.2.2 Business Logic Layer
- **薬液選択管理**: 選択状態の管理と検証
- **画像認識管理**: YOLO推論の制御
- **安全確認管理**: 結果の判定とフィードバック

#### 1.2.3 AI/ML Layer
- **YOLO推論**: リアルタイム物体検出
- **画像前処理**: フレームの前処理
- **結果後処理**: 検出結果の解釈

## 2. データフロー設計

### 2.1 メインフロー

```
1. アプリ起動
   ↓
2. 薬液選択画面表示
   ↓
3. ユーザーが薬液を選択
   ↓
4. 補充開始ボタン押下
   ↓
5. カメラ起動・映像表示開始
   ↓
6. リアルタイム画像認識開始
   ↓
7. YOLO推論実行
   ↓
8. 検出結果の解釈
   ↓
9. 選択薬液と検出結果の照合
   ↓
10. 結果表示・音声フィードバック
```

### 2.2 画像認識フロー

```
カメラフレーム取得
   ↓
画像前処理（リサイズ、正規化）
   ↓
YOLO推論実行
   ↓
検出結果の解析
   ↓
信頼度フィルタリング
   ↓
薬液種類の判定
   ↓
蓋開閉状態の判定
   ↓
結果の統合・出力
```

## 3. クラス設計

### 3.1 主要クラス

#### 3.1.1 MainApplication
```python
class MainApplication:
    """メインアプリケーションクラス"""
    def __init__(self):
        self.medicine_selector = MedicineSelector()
        self.camera_manager = CameraManager()
        self.ai_recognizer = AIRecognizer()
        self.safety_checker = SafetyChecker()
    
    def run(self):
        """アプリケーション実行"""
        pass
```

#### 3.1.2 MedicineSelector
```python
class MedicineSelector:
    """薬液選択管理クラス"""
    def __init__(self):
        self.selected_medicine = None
        self.medicine_types = ["次亜塩素酸ナトリウム", "酢酸"]
    
    def select_medicine(self, medicine_type: str):
        """薬液選択"""
        pass
    
    def get_selected_medicine(self) -> str:
        """選択された薬液を取得"""
        pass
```

#### 3.1.3 CameraManager
```python
class CameraManager:
    """カメラ管理クラス"""
    def __init__(self):
        self.camera = None
        self.is_running = False
    
    def start_camera(self):
        """カメラ起動"""
        pass
    
    def stop_camera(self):
        """カメラ停止"""
        pass
    
    def get_frame(self) -> np.ndarray:
        """フレーム取得"""
        pass
```

#### 3.1.4 AIRecognizer
```python
class AIRecognizer:
    """AI画像認識クラス"""
    def __init__(self, model_path: str):
        self.model = self.load_yolo_model(model_path)
        self.confidence_threshold = 0.5
    
    def load_yolo_model(self, model_path: str):
        """YOLOモデル読み込み"""
        pass
    
    def detect_objects(self, frame: np.ndarray) -> List[Detection]:
        """物体検出実行"""
        pass
    
    def classify_medicine(self, detections: List[Detection]) -> str:
        """薬液種類の分類"""
        pass
```

#### 3.1.5 SafetyChecker
```python
class SafetyChecker:
    """安全確認クラス"""
    def __init__(self):
        self.audio_player = AudioPlayer()
        self.visual_feedback = VisualFeedback()
    
    def check_safety(self, selected_medicine: str, detected_medicine: str) -> bool:
        """安全性チェック"""
        pass
    
    def show_result(self, is_safe: bool):
        """結果表示"""
        pass
    
    def play_audio(self, is_safe: bool):
        """音声再生"""
        pass
```

### 3.2 データクラス

#### 3.2.1 Detection
```python
@dataclass
class Detection:
    """検出結果データクラス"""
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    medicine_type: str
    cap_status: str  # "open" or "closed"
```

## 4. データベース設計

### 4.1 学習データ構造

```
data/
├── images/
│   ├── sodium_hypochlorite/
│   │   ├── cap_closed/
│   │   └── cap_open/
│   └── acetic_acid/
│       ├── cap_closed/
│       └── cap_open/
├── labels/
│   ├── sodium_hypochlorite/
│   │   ├── cap_closed/
│   │   └── cap_open/
│   └── acetic_acid/
│       ├── cap_closed/
│       └── cap_open/
└── models/
    └── best.pt
```

### 4.2 設定ファイル

```yaml
# config.yaml
model:
  path: "models/best.pt"
  confidence_threshold: 0.5
  nms_threshold: 0.4

camera:
  device_id: 0
  width: 640
  height: 480
  fps: 30

audio:
  success_sound: "sounds/success.wav"
  error_sound: "sounds/error.wav"
  volume: 0.8

ui:
  window_width: 800
  window_height: 600
  theme: "dark"
```

## 5. アルゴリズム設計

### 5.1 YOLO推論アルゴリズム

```python
def yolo_inference(frame: np.ndarray) -> List[Detection]:
    """YOLO推論アルゴリズム"""
    # 1. 画像前処理
    processed_frame = preprocess_image(frame)
    
    # 2. YOLO推論実行
    predictions = model(processed_frame)
    
    # 3. 信頼度フィルタリング
    filtered_predictions = filter_by_confidence(predictions)
    
    # 4. NMS適用
    final_predictions = apply_nms(filtered_predictions)
    
    # 5. 結果の変換
    detections = convert_to_detections(final_predictions)
    
    return detections
```

### 5.2 安全性チェックアルゴリズム

```python
def safety_check(selected: str, detected: str) -> bool:
    """安全性チェックアルゴリズム"""
    # 1. 選択された薬液と検出された薬液の一致確認
    if selected == detected:
        return True
    
    # 2. 不一致の場合は危険
    return False
```

## 6. エラーハンドリング設計

### 6.1 例外クラス

```python
class CameraError(Exception):
    """カメラ関連エラー"""
    pass

class ModelLoadError(Exception):
    """モデル読み込みエラー"""
    pass

class RecognitionError(Exception):
    """認識エラー"""
    pass
```

### 6.2 エラー処理フロー

```
エラー発生
   ↓
エラータイプの判定
   ↓
適切な例外クラスの選択
   ↓
エラーメッセージの生成
   ↓
ユーザーへの通知
   ↓
復旧処理の実行
```

## 7. パフォーマンス設計

### 7.1 最適化戦略

- **マルチスレッド処理**: カメラ取得とAI推論の並列実行
- **フレームスキップ**: 処理負荷軽減のためのフレーム間引き
- **モデル最適化**: 量子化による推論速度向上
- **メモリ管理**: 効率的なメモリ使用

### 7.2 パフォーマンス指標

- **フレームレート**: 30fps以上
- **認識遅延**: 100ms以下
- **CPU使用率**: 80%以下
- **メモリ使用量**: 2GB以下

## 8. セキュリティ設計

### 8.1 データ保護

- **ローカル処理**: 外部通信なし
- **データ暗号化**: 機密データの暗号化
- **アクセス制御**: ファイルアクセス権限の管理

### 8.2 安全性確保

- **入力検証**: ユーザー入力の検証
- **例外処理**: 適切なエラーハンドリング
- **ログ記録**: 操作履歴の記録
