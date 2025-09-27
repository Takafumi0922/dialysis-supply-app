# Android APK ビルド - 代替方法

## 現在の状況
- Windows環境でBuildozerが直接動作しない
- WSLのインストールが進行中
- 代替手段が必要

## 推奨方法

### 1. オンラインサービスを使用

#### GitHub Actions を使用
```yaml
# .github/workflows/android.yml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    
    - name: Install buildozer
      run: pip install buildozer
    
    - name: Build APK
      run: buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-debug
        path: bin/*.apk
```

### 2. クラウドビルドサービス

#### Bitrise
1. https://bitrise.io にアカウント作成
2. GitHubリポジトリを接続
3. Androidビルド設定
4. 自動ビルド実行

#### Codemagic
1. https://codemagic.io にアカウント作成
2. GitHubリポジトリを接続
3. Androidビルド設定
4. 自動ビルド実行

### 3. ローカルDocker環境

#### Docker Desktop を使用
```bash
# Dockerfile を作成
# 既に作成済み

# Dockerイメージをビルド
docker build -t dialysis-app .

# コンテナを実行してAPKをビルド
docker run -v ${PWD}/bin:/app/bin dialysis-app
```

### 4. 仮想マシンを使用

#### VirtualBox + Ubuntu
1. VirtualBoxをインストール
2. Ubuntu 20.04 LTSをインストール
3. プロジェクトをコピー
4. Buildozerでビルド

## 即座に試せる方法

### 1. GitHub Actions セットアップ
```bash
# GitHubリポジトリを作成
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/dialysis-app.git
git push -u origin main
```

### 2. 手動でAPKを作成
```bash
# 既存のKivyアプリをAPKに変換
# オンラインツールを使用
```

## 推奨手順

1. **GitHub Actions** を使用（最も簡単）
2. **Docker** を使用（ローカル環境）
3. **WSL完了後** にBuildozerを使用

## 次のステップ

1. GitHubリポジトリを作成
2. コードをプッシュ
3. GitHub Actionsで自動ビルド
4. APKをダウンロード
5. Android端末にインストール
