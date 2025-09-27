@echo off
echo GitHub セットアップスクリプト
echo ================================
echo.

echo 1. GitHubアカウント作成
echo    https://github.com にアクセスしてアカウントを作成してください
echo.

echo 2. リポジトリ作成
echo    GitHubで新しいリポジトリを作成してください
echo    リポジトリ名: dialysis-supply-app
echo.

echo 3. Gitの初期設定（初回のみ）
set /p username="あなたの名前を入力してください: "
set /p email="あなたのメールアドレスを入力してください: "
git config --global user.name "%username%"
git config --global user.email "%email%"
echo.

echo 4. プロジェクトをGitHubにアップロード
echo    以下のコマンドを実行してください:
echo.
echo    git init
echo    git add .
echo    git commit -m "Initial commit: 透析供給装置薬液補充アプリ"
echo    git remote add origin https://github.com/あなたのユーザー名/dialysis-supply-app.git
echo    git push -u origin main
echo.

echo 5. GitHub Actionsで自動ビルド
echo    プッシュすると自動でAPKがビルドされます
echo    Actions タブでビルド状況を確認してください
echo.

echo 6. APKダウンロード
echo    ビルド完了後、Artifacts からAPKをダウンロードしてください
echo.

pause
