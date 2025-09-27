@echo off
echo Android APK ビルドスクリプト
echo.

echo 方法1: WSLを使用してビルド
echo wsl -e bash -c "cd /mnt/c/Users/gotos/Desktop/ykuekiAI\ project && buildozer android debug"
echo.

echo 方法2: Dockerを使用してビルド
echo docker build -t dialysis-app .
echo docker run -v %cd%\bin:/app/bin dialysis-app
echo.

echo 方法3: 手動でWSLに移動してビルド
echo wsl
echo cd /mnt/c/Users/gotos/Desktop/ykuekiAI\ project
echo buildozer android debug
echo.

echo ビルドが完了したら、bin/ ディレクトリにAPKファイルが生成されます。
echo.

pause
