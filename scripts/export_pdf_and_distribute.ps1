# scripts/export_pdf_and_distribute.ps1
$ErrorActionPreference = "Stop"

$rootDocx = "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx"
$rootPdf  = "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf"

Write-Host "Exporting PDF from $rootDocx..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($rootDocx)
    Write-Host "Saving PDF to $rootPdf..."
    $doc.SaveAs2($rootPdf, 17) # 17 = wdFormatPDF
    $doc.Close(0)
    Write-Host "PDF exported successfully!"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}

# Now distribute DOCX and PDF across all draft & platform folders
$draft20261109 = "E:\Papers\PFPJ\Draft_Versions\2026-11-09"
if (-not (Test-Path $draft20261109)) { New-Item -ItemType Directory -Path $draft20261109 -Force | Out-Null }

$draft20261021 = "E:\Papers\PFPJ\Draft_Versions\2026-10-21"
if (-not (Test-Path $draft20261021)) { New-Item -ItemType Directory -Path $draft20261021 -Force | Out-Null }

$platformDir = "E:\Papers\PFPJ\PFP_Platform\web\public\docs\minab-report"
if (-not (Test-Path $platformDir)) { New-Item -ItemType Directory -Path $platformDir -Force | Out-Null }

Write-Host "Distributing copies..."
Copy-Item $rootDocx -Destination "E:\Papers\PFPJ\PFPJ_Top_Ten_Most_Cited_Documents_Benchmarked_Cases.docx" -Force
Copy-Item $rootPdf  -Destination "E:\Papers\PFPJ\PFPJ_Top_Ten_Most_Cited_Documents_Benchmarked_Cases.pdf" -Force

Copy-Item $rootDocx -Destination (Join-Path $draft20261109 "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-11-09.docx") -Force
Copy-Item $rootPdf  -Destination (Join-Path $draft20261109 "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-11-09.pdf") -Force

Copy-Item $rootDocx -Destination (Join-Path $draft20261021 "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-10-21.docx") -Force
Copy-Item $rootPdf  -Destination (Join-Path $draft20261021 "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-10-21.pdf") -Force

Copy-Item $rootDocx -Destination (Join-Path $platformDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx") -Force
Copy-Item $rootPdf  -Destination (Join-Path $platformDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf") -Force

Write-Host "`nDISTRIBUTION COMPLETE! Verifying files:"
Get-Item -Path `
    "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx", `
    "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf", `
    "E:\Papers\PFPJ\PFPJ_Top_Ten_Most_Cited_Documents_Benchmarked_Cases.docx", `
    "E:\Papers\PFPJ\PFPJ_Top_Ten_Most_Cited_Documents_Benchmarked_Cases.pdf", `
    "E:\Papers\PFPJ\Draft_Versions\2026-11-09\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-11-09.docx", `
    "E:\Papers\PFPJ\Draft_Versions\2026-11-09\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-11-09.pdf", `
    "E:\Papers\PFPJ\PFP_Platform\web\public\docs\minab-report\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx", `
    "E:\Papers\PFPJ\PFP_Platform\web\public\docs\minab-report\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf" | `
    Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
