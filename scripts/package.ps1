param([string]$OutputDirectory = 'D:\迅雷下载\vibe coding')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'manifest.json') -Raw | ConvertFrom-Json
$zipPath = Join-Path $OutputDirectory "cozy-christmas-theme-$($manifest.version).zip"
if (Test-Path -LiteralPath $zipPath) { throw "Archive already exists: $zipPath" }
$items = @('manifest.json', 'logo', 'README.md', 'scripts', 'store-assets', 'PACKAGING.md', '.gitignore') | ForEach-Object { Join-Path $projectRoot $_ }
Compress-Archive -LiteralPath $items -DestinationPath $zipPath
Get-Item -LiteralPath $zipPath | Select-Object FullName,Length
