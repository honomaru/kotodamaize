# frontendディレクトリに移動
Set-Location ./frontend

# Reactアプリのビルド
npm run build

$outDir = "../builded_kotodamize"

# 出力フォルダが存在しない場合、作成
if (-Not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir
}

# buildディレクトリを丸ごとコピー（強制的に上書き）
Copy-Item -Recurse -Force ./build -Destination (Join-Path $outDir "build")

# バックエンドファイルを出力フォルダにコピー
$backendFiles = "../api.py", "../audio_utils.py", "../text_utils.py", "../requirements.txt"
Copy-Item $backendFiles -Force -Destination $outDir

Set-Location ../

Write-Output "Created $outDir"