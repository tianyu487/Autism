# =====================================================================
# 反复出图,直到每门课的每一页都拿到“真正的绘本插画”(不再有图标回退页)。
# 原理:插画成功会缓存到 output\<课>\_illus\;本脚本每轮只重试“还没有缓存”的失败页,
#       已成功的页直接复用、不重出、不联网。循环到 19/19 或达到上限为止。
# 不归档、不删除任何东西;videos\ 里的 6 个成片不受影响。
# 用法:  powershell -ExecutionPolicy Bypass -File .\gen_until_complete.ps1
# =====================================================================
$ErrorActionPreference = "Stop"
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location "D:\Claude\Autism"

$slugs     = @("naming_feelings","hello_goodbye","asking_for_help","brushing_teeth","stop_and_think")
$expected  = 19     # 每门课 = 标题+开场+4步+3练习x3+选择+2选项+收尾 = 19 页
$maxPasses = 15
$summary   = @{}

foreach ($s in $slugs) {
    Write-Host "########## $s ##########" -ForegroundColor Cyan
    $done = 0
    for ($i = 1; $i -le $maxPasses; $i++) {
        python -m autismcare train --script "scripts\$s.json" --slug $s --no-ai --scenes-only
        $illusDir = "output\$s\_illus"
        $done = 0
        if (Test-Path $illusDir) {
            $done = (Get-ChildItem "$illusDir\*.png" -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 2000 }).Count
        }
        Write-Host ("[$s] pass ${i}: $done/$expected real illustrations") -ForegroundColor Green
        if ($done -ge $expected) { Write-Host "[$s] COMPLETE" -ForegroundColor Green; break }
        Start-Sleep -Seconds 6
    }
    $summary[$s] = $done
}

Write-Host "`n================ SUMMARY ================" -ForegroundColor Cyan
foreach ($s in $slugs) {
    $c = $summary[$s]
    if ($c -ge $expected) { Write-Host ("{0,-18} {1}/{2}  OK" -f $s,$c,$expected) -ForegroundColor Green }
    else                  { Write-Host ("{0,-18} {1}/{2}  still incomplete - run again" -f $s,$c,$expected) -ForegroundColor Yellow }
}
Write-Host "`nDone. Tell me in chat when this finishes; I will review every page and only show you the passing set."
