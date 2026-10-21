# scripts/convert_charts_to_pdf.ps1
$ErrorActionPreference = "Stop"

$docxPath = "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx"
$pdfPath = "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf"

if (-not (Test-Path $docxPath)) {
    throw "DOCX not found: $docxPath"
}

Write-Host "Converting DOCX to PDF via Word COM: $docxPath"
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0

try {
    $doc = $w.Documents.Open($docxPath)
    Write-Host "Saving PDF: $pdfPath"
    $doc.SaveAs2($pdfPath, 17) # 17 = wdFormatPDF
    $doc.Close(0)
    Write-Host "PDF successfully exported!"
}
finally {
    $w.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($w) | Out-Null
}

$draftDir = "E:\Papers\PFPJ\Draft_Versions\2026-10-21"
if (-not (Test-Path $draftDir)) {
    New-Item -ItemType Directory -Path $draftDir -Force | Out-Null
}
Copy-Item $docxPath (Join-Path $draftDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-10-21.docx") -Force
Copy-Item $pdfPath (Join-Path $draftDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_2026-10-21.pdf") -Force

$platformDocsDir = "E:\Papers\PFPJ\PFP_Platform\web\public\docs\minab-report"
if (-not (Test-Path $platformDocsDir)) {
    New-Item -ItemType Directory -Path $platformDocsDir -Force | Out-Null
}
Copy-Item $docxPath (Join-Path $platformDocsDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx") -Force
Copy-Item $pdfPath (Join-Path $platformDocsDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf") -Force

Get-Item $docxPath, $pdfPath | Select-Object Name, Length, LastWriteTime
