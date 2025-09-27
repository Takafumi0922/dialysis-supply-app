# Android APK ビルド手順

## 方法1: WSL (Windows Subsystem for Linux) を使用

### 1. WSLのインストール
```bash
# PowerShell (管理者として実行)
wsl --install
```

### 2. Ubuntu環境でのセットアップ
```bash
# WSLでUbuntuを起動
wsl

# 必要なパッケージをインストール
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Buildozerをインストール
pip3 install buildozer

# Android SDKをインストール
mkdir -p ~/.buildozer/android/platform/android-ndk-r25b
```

### 3. プロジェクトのコピー
```bash
# WindowsのプロジェクトをWSLにコピー
cp -r /mnt/c/Users/gotos/Desktop/ykuekiAI\ project ~/dialysis_app
cd ~/dialysis_app
```

### 4. APKビルド
```bash
# 初回ビルド（時間がかかります）
buildozer android debug

# ビルドされたAPKは bin/ ディレクトリにあります
```

## 方法2: Dockerを使用

### 1. Docker Desktopのインストール
- Docker Desktop for Windowsをインストール

### 2. Dockerfileの作成
```dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3 \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install buildozer

WORKDIR /app
COPY . .

CMD ["buildozer", "android", "debug"]
```

### 3. Dockerでビルド
```bash
# Dockerイメージをビルド
docker build -t dialysis-app .

# コンテナを実行してAPKをビルド
docker run -v ${PWD}/bin:/app/bin dialysis-app
```

## 方法3: オンラインサービスを使用

### 1. GitHub Actions
- GitHubリポジトリにプッシュ
- GitHub Actionsで自動ビルド

### 2. クラウドビルドサービス
- Bitrise
- Codemagic
- AppCenter

## トラブルシューティング

### よくある問題
1. **Java環境**: OpenJDK 8が必要
2. **Android SDK**: 適切なバージョンのSDKが必要
3. **メモリ不足**: ビルドには十分なメモリが必要

### 推奨環境
- RAM: 8GB以上
- ストレージ: 10GB以上の空き容量
- インターネット接続: 初回ビルド時に大量のダウンロード

## ビルド後の確認

### APKの確認
```bash
# APKファイルの場所
ls -la bin/*.apk

# APKの情報を確認
aapt dump badging bin/dialysis_supply_app-1.0-debug.apk
```

### インストール方法
1. Android端末で「開発者オプション」を有効化
2. 「不明なソースからのアプリ」を許可
3. APKファイルを端末に転送してインストール
