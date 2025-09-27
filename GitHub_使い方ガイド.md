# GitHub 使い方ガイド - Android APK ビルド

## 📚 GitHubとは？
GitHubは、コードを保存・共有・管理するためのプラットフォームです。今回の目的は、GitHub Actionsという機能を使って、自動でAndroid APKをビルドすることです。

## 🚀 ステップ1: GitHubアカウント作成

### 1.1 GitHubにアクセス
- ブラウザで https://github.com にアクセス
- 「Sign up」をクリック

### 1.2 アカウント情報を入力
- **Username**: 好きなユーザー名（例：gotos-dialysis）
- **Email**: メールアドレス
- **Password**: パスワード
- 「Create account」をクリック

### 1.3 メール認証
- 登録したメールアドレスに認証メールが届く
- メール内のリンクをクリックして認証完了

## 📁 ステップ2: リポジトリ作成

### 2.1 新しいリポジトリを作成
1. GitHubにログイン後、右上の「+」→「New repository」をクリック
2. 以下の情報を入力：
   - **Repository name**: `dialysis-supply-app`
   - **Description**: `透析供給装置薬液補充アプリ`
   - **Public** を選択（無料で使用可能）
   - **Add a README file** にチェック
3. 「Create repository」をクリック

## 💻 ステップ3: ローカルからGitHubにアップロード

### 3.1 Gitの初期設定（初回のみ）
```bash
# PowerShellまたはコマンドプロンプトで実行
git config --global user.name "あなたの名前"
git config --global user.email "あなたのメールアドレス"
```

### 3.2 プロジェクトをGitHubにアップロード
```bash
# プロジェクトディレクトリに移動
cd "C:\Users\gotos\Desktop\ykuekiAI project"

# Gitリポジトリを初期化
git init

# すべてのファイルを追加
git add .

# 初回コミット
git commit -m "Initial commit: 透析供給装置薬液補充アプリ"

# GitHubリポジトリと接続（作成したリポジトリのURLを使用）
git remote add origin https://github.com/あなたのユーザー名/dialysis-supply-app.git

# GitHubにアップロード
git push -u origin main
```

## 🔧 ステップ4: GitHub Actions設定

### 4.1 ワークフローファイルの作成
プロジェクトに以下のファイルを作成：

**`.github/workflows/android.yml`**
```yaml
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
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    
    - name: Install Python dependencies
      run: |
        pip install buildozer
    
    - name: Build APK
      run: |
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-debug
        path: bin/*.apk
```

### 4.2 ファイルをGitHubにアップロード
```bash
# 新しいファイルを追加
git add .github/workflows/android.yml

# 変更をコミット
git commit -m "Add GitHub Actions workflow for Android build"

# GitHubにプッシュ
git push
```

## 📱 ステップ5: APKビルドの実行

### 5.1 自動ビルドの確認
1. GitHubのリポジトリページにアクセス
2. 「Actions」タブをクリック
3. ビルドが自動で開始される
4. ビルド状況を確認（約10-15分かかります）

### 5.2 ビルド完了後の確認
1. ビルドが完了すると緑色のチェックマークが表示
2. ビルド名をクリック
3. 「Artifacts」セクションでAPKファイルをダウンロード

## 📲 ステップ6: Android端末にインストール

### 6.1 Android端末の設定
1. **設定** → **端末情報** → **ビルド番号**を7回タップ
2. **設定** → **開発者向けオプション** → **USBデバッグ**を有効化
3. **設定** → **セキュリティ** → **不明なソースからのアプリ**を許可

### 6.2 APKのインストール
1. ダウンロードしたAPKファイルをAndroid端末に転送
2. ファイルマネージャーでAPKファイルをタップ
3. インストールを実行

## 🔄 ステップ7: コード更新時の手順

### 7.1 コードを変更した場合
```bash
# 変更をステージング
git add .

# 変更をコミット
git commit -m "Update: 変更内容の説明"

# GitHubにプッシュ
git push
```

### 7.2 自動ビルド
- プッシュすると自動で新しいAPKがビルドされる
- Actionsタブでビルド状況を確認

## 🆘 トラブルシューティング

### よくある問題と解決方法

#### 1. Git認証エラー
```bash
# 個人アクセストークンを使用
git remote set-url origin https://ユーザー名:トークン@github.com/ユーザー名/リポジトリ名.git
```

#### 2. ビルドエラー
- GitHub Actionsのログを確認
- エラーメッセージを読んで問題を特定
- 必要に応じてコードを修正

#### 3. APKが生成されない
- buildozer.specファイルの設定を確認
- 依存関係が正しく指定されているか確認

## 📋 チェックリスト

- [ ] GitHubアカウント作成
- [ ] リポジトリ作成
- [ ] ローカルプロジェクトをGitHubにアップロード
- [ ] GitHub Actionsワークフロー作成
- [ ] 自動ビルド実行
- [ ] APKダウンロード
- [ ] Android端末にインストール

## 🎉 完了！

これで、GitHubを使用してAndroid APKを自動ビルドできるようになりました！

### メリット
- ✅ 自動ビルド：コードをプッシュするだけでAPKが作成される
- ✅ バージョン管理：コードの変更履歴を管理
- ✅ 共有：他の人とコードを共有可能
- ✅ バックアップ：コードがクラウドに保存される
