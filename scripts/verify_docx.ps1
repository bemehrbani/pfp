# scripts/verify_docx.ps1
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx")
    Write-Host "DOCX Verification:"
    Write-Host "Paragraphs: $($doc.Paragraphs.Count)"
    Write-Host "Tables:     $($doc.Tables.Count)"
    Write-Host "Hyperlinks: $($doc.Hyperlinks.Count)"
    
    $headings = @()
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^CASE \d+:") {
            $headings += $txt
        }
    }
    Write-Host "`nCase Headings Found ($($headings.Count)):"
    foreach ($h in $headings) {
        Write-Host "  - $h"
    }

    Write-Host "`nHyperlink Sample (first 10):"
    for ($i = 1; $i -le [Math]::Min(10, $doc.Hyperlinks.Count); $i++) {
        $hl = $doc.Hyperlinks.Item($i)
        Write-Host "  [$i] $($hl.TextToDisplay) -> $($hl.Address)"
    }

    $doc.Close(0)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
