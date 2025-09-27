# 透析供給装置薬液補充アプリ - Android版

## 概要
透析供給装置の薬液補充作業における安全性を向上させるためのAndroidアプリケーションです。
次亜塩素酸ナトリウムと酢酸の誤操作を防ぎ、1人作業時の安全性を確保します。

## 機能
- 薬液選択（次亜塩素酸ナトリウム/酢酸）
- Androidカメラ機能
- 画像認識による薬液識別（将来実装予定）
- 安全確認機能（将来実装予定）

## 技術要件
- Python 3.10
- Kivy 2.1.0
- KivyMD 1.1.1
- OpenCV
- Plyer（Androidカメラ）

## インストール

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. Android APKのビルド
```bash
# Buildozerのインストール
pip install buildozer

# Android APKのビルド
buildozer android debug
```

### 3. デスクトップでのテスト実行
```bash
python run_android.py
```

## 使用方法

### 1. アプリケーション起動
```bash
python run_android.py
```

### 2. 薬液選択
- 次亜塩素酸ナトリウムまたは酢酸を選択
- 「補充開始」ボタンを押す

### 3. カメラ機能
- 「カメラ起動」ボタンを押してカメラを起動
- 撮影された画像が表示されます

## Android APKのビルド

### 1. Buildozerのセットアップ
```bash
# Buildozerのインストール
pip install buildozer

# 初回セットアップ
buildozer init
```

### 2. APKのビルド
```bash
# デバッグAPKのビルド
buildozer android debug

# リリースAPKのビルド
buildozer android release
```

### 3. APKのインストール
```bash
# デバイスにAPKをインストール
buildozer android deploy
```

## プロジェクト構造
```
.
├── src/
│   ├── __init__.py
│   ├── android_app.py        # Android版メインアプリケーション
│   ├── camera_manager.py     # カメラ管理
│   └── medicine_selector.py  # 薬液選択管理
├── config.yaml               # 設定ファイル
├── buildozer.spec            # Buildozer設定
├── requirements.txt          # 依存関係
├── run_android.py           # Android版実行スクリプト
└── README_Android.md        # このファイル
```

## 設定

### config.yaml
```yaml
camera:
  device_id: 0      # カメラデバイスID
  width: 640        # 映像幅
  height: 480       # 映像高さ
  fps: 30           # フレームレート

ui:
  window_width: 800   # ウィンドウ幅
  window_height: 600  # ウィンドウ高さ
  title: "透析供給装置薬液補充アプリ"
```

### buildozer.spec
- Android API 33対応
- カメラ権限設定
- ストレージ権限設定

## 開発状況
- [x] Android対応環境構築
- [x] KivyベースUI実装
- [x] 薬液選択機能実装
- [x] Androidカメラ機能実装
- [ ] 画像認識機能（YOLOモデル）
- [ ] 安全確認機能
- [ ] 音声フィードバック

## Android特有の機能

### カメラ機能
- Plyerを使用したAndroidカメラアクセス
- 撮影画像の自動表示
- カメラ権限の適切な管理

### UI/UX
- Material Design準拠
- タッチ操作最適化
- 縦画面レイアウト

### 権限管理
- CAMERA: カメラアクセス
- WRITE_EXTERNAL_STORAGE: 画像保存
- READ_EXTERNAL_STORAGE: 画像読み込み

## 注意事項
- Android 5.0 (API 21) 以上が必要
- カメラ権限の許可が必要
- 初回起動時に権限の許可を求められます
- 現在はカメラ撮影のみで、リアルタイム映像は未実装

## トラブルシューティング

### カメラが起動しない場合
1. カメラ権限が許可されているか確認
2. 他のアプリでカメラを使用していないか確認
3. デバイスの再起動を試す

### APKビルドエラーの場合
1. Android SDKが正しくインストールされているか確認
2. Java JDKがインストールされているか確認
3. 環境変数が正しく設定されているか確認

## ライセンス
このプロジェクトは医療現場での安全性向上を目的として開発されています。
