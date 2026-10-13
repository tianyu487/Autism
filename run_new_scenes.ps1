# =====================================================================
# 批量为 5 门新课程重新生成场景插画(仅出图 --scenes-only),供审查。
# 用的是 train 子命令(训练模块 module.json),不是 generate(那是社交故事)。
# 旧草稿若还在 output\ 里,会先【移动】备份到 output\_prior\<时间戳>\(只移动、不删除)。
# videos\ 里已生成的 6 个成片不受影响。
# 用法:  powershell -ExecutionPolicy Bypass -File .\run_new_scenes.ps1
# =====================================================================
$ErrorActionPreference = "Stop"
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location "D:\Claude\Autism"

$slugs = @("naming_feelings","hello_goodbye","asking_for_help","brushing_teeth","stop_and_think")
$stamp   = Get-Date -Format "yyyyMMdd_HHmmss"
$archive = "output\_prior\$stamp"

foreach ($s in $slugs) {
    $script = "scripts\$s.json"
    if (-not (Test-Path $script)) { Write-Host "SKIP $s : missing $script" -ForegroundColor Yellow; continue }

    $src = "output\$s"
    if (Test-Path $src) {
        New-Item -ItemType Directory -Force -Path $archive | Out-Null
        Write-Host "Archiving old folder: $src -> $archive\$s"
        Move-Item -Path $src -Destination "$archive\$s"
    }

    Write-Host "=== Generating scenes: $s ===" -ForegroundColor Green
    python -m autismcare train --script $script --slug $s --no-ai --scenes-only
    if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $s (exit $LASTEXITCODE)" -ForegroundColor Red }
    else { Write-Host "OK: $s scenes done`n" -ForegroundColor Green }
}

Write-Host "`nAll done. Scenes are in output\<slug>\scenes\" -ForegroundColor Cyan
Write-Host "Tell me in chat that generation is done; I will review every page and only show you the passing set."
