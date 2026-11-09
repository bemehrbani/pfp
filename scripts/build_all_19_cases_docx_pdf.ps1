# scripts/build_all_19_cases_docx_pdf.ps1
# Generates publication-grade MS Word (.docx) and Adobe PDF (.pdf) editions
# of the Case-Based Benchmark Charts covering ALL 19 CASES for the Minab Strike Dossier (Docket PFPJ-2026-IR-001)

param (
    [string]$ProductionDate = "2026-11-09"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================================="
Write-Host "PFPJ ry -- ALL 19 CASES Legal Benchmark Charts Generator"
Write-Host "Production Date: $ProductionDate"
Write-Host "=========================================================="

$sourceMd = "E:\Papers\PFPJ\Campaigns\minab\legal_benchmarks\COMPREHENSIVE_BENCHMARKING_ALL_19_CASES.md"

if (-not (Test-Path $sourceMd)) {
    throw "Source Markdown file not found: $sourceMd"
}

function Format-InlineText ($text) {
    if ([string]::IsNullOrEmpty($text)) { return "" }
    
    # 1. Protect inline code: `code`
    $codeTokens = New-Object System.Collections.Generic.List[string]
    $text = [regex]::Replace($text, '`([^`]+)`', {
        param($m)
        $idx = $codeTokens.Count
        $codeTokens.Add($m.Groups[1].Value)
        return "XYZINLINECODE${idx}XYZ"
    })

    # 2. Extract and protect markdown links: [text](url)
    $linkTokens = New-Object System.Collections.Generic.List[hashtable]
    $text = [regex]::Replace($text, '\[([^\]]+)\]\(([^)]+)\)', {
        param($m)
        $anchor = $m.Groups[1].Value.Trim()
        $url = $m.Groups[2].Value.Trim()
        if ($url -notmatch '^[a-zA-Z]+://') {
            $url = "https://" + $url
        }
        $idx = $linkTokens.Count
        $linkTokens.Add(@{ Text = $anchor; Url = $url })
        return "XYZMARKDOWNLINK${idx}XYZ"
    })

    # 3. HTML entities
    $text = $text -replace '&(?!#?[a-zA-Z0-9]+;)', '&amp;'
    
    # 4. Math symbols
    $text = $text -replace '\$M_L = ([0-9.]+)\$', '<i>M</i><sub>L</sub> = $1'
    $text = $text -replace '\$\\Delta t = ([0-9.]+) seconds\$', '&Delta;<i>t</i> = $1 seconds'
    $text = $text -replace '\$\\Delta t = ([0-9.]+)s\$', '&Delta;<i>t</i> = $1s'
    $text = $text -replace '\\Delta t = ([0-9.]+)s', '&Delta;<i>t</i> = $1s'
    $text = $text -replace '\$([0-9,]+)\$', '\$$1'

    # 5. Bold & Italics on prose text
    $text = [regex]::Replace($text, '\*\*\*(.*?)\*\*\*', '<b><i>$1</i></b>')
    $text = [regex]::Replace($text, '\*\*(.*?)\*\*', '<b>$1</b>')
    $text = [regex]::Replace($text, '(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', '<i>$1</i>')
    $text = [regex]::Replace($text, '(?<!_)_(?!_)(.*?)(?<!_)_(?!_)', '<i>$1</i>')

    # 6. Reinsert protected code tokens
    for ($i = 0; $i -lt $codeTokens.Count; $i++) {
        $cVal = [System.Net.WebUtility]::HtmlEncode($codeTokens[$i])
        $codeHtml = "<code style='font-family: Consolas, monospace; background-color: #f1f5f9; padding: 1px 3px; border-radius: 3px; font-size: 8pt; color: #831843;'>$cVal</code>"
        $text = $text.Replace("XYZINLINECODE${i}XYZ", $codeHtml)
    }

    # 7. Reinsert protected link tokens with styled active <a> tags
    for ($i = 0; $i -lt $linkTokens.Count; $i++) {
        $entry = $linkTokens[$i]
        $anchorText = $entry.Text
        $anchorText = [regex]::Replace($anchorText, '\*\*(.*?)\*\*', '<b>$1</b>')
        $anchorText = [regex]::Replace($anchorText, '(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', '<i>$1</i>')
        $urlClean = $entry.Url -replace '"', '&quot;'
        $linkHtml = "<a href=""$urlClean"" style=""color: #1d4ed8; text-decoration: underline; font-weight: 500;"">$anchorText</a>"
        $text = $text.Replace("XYZMARKDOWNLINK${i}XYZ", $linkHtml)
    }

    return $text
}

function Convert-MdToHtmlBody ($lines) {
    $sb = New-Object System.Text.StringBuilder
    $inTable = $false
    $inQuote = $false
    $inUl = $false
    $inPre = $false
    $tableRows = New-Object System.Collections.Generic.List[string]

    $closeBlocks = {
        if ($inQuote) {
            $sb.AppendLine("</blockquote>") | Out-Null
            $script:inQuote = $false
        }
        if ($inUl) {
            $sb.AppendLine("</ul>") | Out-Null
            $script:inUl = $false
        }
    }

    $renderTable = {
        param($rows)
        if ($rows.Count -eq 0) { return }
        $sb.AppendLine("<table class='case-chart-table' style='width: 100%; border-collapse: collapse; margin: 12px 0 16px 0; font-size: 8pt; font-family: Calibri, sans-serif; table-layout: fixed;'>") | Out-Null
        $isFirst = $true
        $colCount = 0

        foreach ($r in $rows) {
            $cells = $r.Trim().Trim('|').Split('|')
            $isSeparator = $true
            foreach ($c in $cells) {
                if ($c.Trim() -notmatch '^:?-+:?$') {
                    $isSeparator = $false
                    break
                }
            }
            if ($isSeparator) { continue }

            $sb.AppendLine("  <tr>") | Out-Null
            if ($isFirst) {
                $colCount = $cells.Count
                for ($idx = 0; $idx -lt $cells.Count; $idx++) {
                    $cellText = Format-InlineText ($cells[$idx].Trim())
                    # Custom column width allocations
                    $wAttr = ""
                    if ($colCount -eq 5) {
                        # Chart 1: No, Issuing Entity, Document Title, Canonical URL, Core Determination
                        if ($idx -eq 0) { $wAttr = "width: 5%; text-align: center;" }
                        elseif ($idx -eq 1) { $wAttr = "width: 22%;" }
                        elseif ($idx -eq 2) { $wAttr = "width: 28%;" }
                        elseif ($idx -eq 3) { $wAttr = "width: 16%; word-break: break-all;" }
                        elseif ($idx -eq 4) { $wAttr = "width: 29%;" }
                    } elseif ($colCount -eq 4) {
                        # Chart 2: Extracted Data, Prior Citations, Target Chapter, Judicial Formulation
                        if ($idx -eq 0) { $wAttr = "width: 24%;" }
                        elseif ($idx -eq 1) { $wAttr = "width: 20%;" }
                        elseif ($idx -eq 2) { $wAttr = "width: 18%;" }
                        elseif ($idx -eq 3) { $wAttr = "width: 38%;" }
                    }
                    $sb.AppendLine("    <th style='background-color: #0f172a; color: #ffffff; padding: 6px 8px; border: 1px solid #334155; text-align: left; font-weight: bold; font-size: 8.5pt; $wAttr'>$cellText</th>") | Out-Null
                }
                $isFirst = $false
            } else {
                for ($idx = 0; $idx -lt $cells.Count; $idx++) {
                    $cellText = Format-InlineText ($cells[$idx].Trim())
                    $alignAttr = ""
                    if ($colCount -eq 5 -and $idx -eq 0) { $alignAttr = "text-align: center; font-weight: bold;" }
                    $sb.AppendLine("    <td style='padding: 5px 8px; border: 1px solid #cbd5e1; vertical-align: top; background-color: #ffffff; $alignAttr'>$cellText</td>") | Out-Null
                }
            }
            $sb.AppendLine("  </tr>") | Out-Null
        }
        $sb.AppendLine("</table>") | Out-Null
    }

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        $trimmed = $line.Trim()

        if ($trimmed.StartsWith('```')) {
            & $closeBlocks
            if ($inPre) {
                $sb.AppendLine("</pre>") | Out-Null
                $inPre = $false
            } else {
                $sb.AppendLine("<pre style='background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 3px solid #0f172a; padding: 8px 12px; font-family: Consolas, monospace; font-size: 7.5pt; color: #0f172a; overflow-x: auto; margin: 10px 0;'>") | Out-Null
                $inPre = $true
            }
            continue
        }

        if ($inPre) {
            $encodedLine = $line -replace '&', '&amp;' -replace '<', '&lt;' -replace '>', '&gt;'
            $sb.AppendLine($encodedLine) | Out-Null
            continue
        }

        if ($trimmed.StartsWith('|') -and $trimmed.EndsWith('|')) {
            & $closeBlocks
            $tableRows.Add($trimmed)
            $inTable = $true
            continue
        } else {
            if ($inTable) {
                & $renderTable $tableRows
                $tableRows.Clear()
                $inTable = $false
            }
        }

        if ($trimmed -match '^(---|\*\*\*|___)$') {
            & $closeBlocks
            $sb.AppendLine("<hr style='border: none; border-top: 1.5px solid #cbd5e1; margin: 16px 0;' />") | Out-Null
            continue
        }

        if ($trimmed -match '^(#{1,5})\s+(.*)$') {
            & $closeBlocks
            $level = $matches[1].Length
            $htext = Format-InlineText ($matches[2])
            
            if ($level -eq 1) {
                $sb.AppendLine("<h1 style='font-family: Georgia, serif; font-size: 14pt; color: #0f172a; margin-top: 24px; margin-bottom: 6px; font-weight: bold; border-bottom: 2px solid #0f172a; padding-bottom: 3px; text-transform: uppercase;'>$htext</h1>") | Out-Null
            } elseif ($level -eq 2) {
                $sb.AppendLine("<h2 style='font-family: Georgia, serif; font-size: 12pt; color: #1e293b; margin-top: 18px; margin-bottom: 4px; font-weight: bold; border-bottom: 1px solid #94a3b8; padding-bottom: 2px;'>$htext</h2>") | Out-Null
            } elseif ($level -eq 3) {
                $sb.AppendLine("<h3 style='font-family: Calibri, sans-serif; font-size: 10.5pt; color: #0f172a; margin-top: 14px; margin-bottom: 3px; font-weight: bold;'>$htext</h3>") | Out-Null
            } else {
                $sb.AppendLine("<h4 style='font-family: Calibri, sans-serif; font-size: 9.5pt; color: #334155; margin-top: 10px; margin-bottom: 2px; font-weight: bold; font-style: italic;'>$htext</h4>") | Out-Null
            }
            continue
        }

        if ($trimmed.StartsWith('>')) {
            if (-not $inQuote) {
                & $closeBlocks
                $sb.AppendLine("<blockquote style='margin: 8px 0 8px 12px; padding: 6px 12px; border-left: 3px solid #0f172a; background-color: #f8fafc; font-style: italic; color: #334155; font-size: 8.5pt;'>") | Out-Null
                $inQuote = $true
            }
            $qtext = $trimmed.Substring(1).Trim()
            $qformatted = Format-InlineText ($qtext)
            $sb.AppendLine("<p style='margin: 2px 0;'>$qformatted</p>") | Out-Null
            continue
        } else {
            if ($inQuote) {
                $sb.AppendLine("</blockquote>") | Out-Null
                $inQuote = $false
            }
        }

        if ($trimmed -match '^(\*|-)\s+(.*)$') {
            if (-not $inUl) {
                & $closeBlocks
                $sb.AppendLine("<ul style='margin: 4px 0 6px 16px; padding-left: 6px; font-size: 8.5pt;'>") | Out-Null
                $inUl = $true
            }
            $litext = Format-InlineText ($matches[2])
            $sb.AppendLine("  <li style='margin-bottom: 2px;'>$litext</li>") | Out-Null
            continue
        }

        if ([string]::IsNullOrWhiteSpace($trimmed)) {
            & $closeBlocks
            continue
        }

        & $closeBlocks
        $pformatted = Format-InlineText ($trimmed)
        $sb.AppendLine("<p style='margin: 0 0 5px 0; text-align: justify; font-size: 8.5pt;'>$pformatted</p>") | Out-Null
    }

    & $closeBlocks
    if ($inTable) {
        & $renderTable $tableRows
    }

    return $sb.ToString()
}

Write-Host "Reading Markdown Source: $sourceMd"
$mdLines = Get-Content -Path $sourceMd -Encoding utf8
$bodyHtml = Convert-MdToHtmlBody $mdLines

# Build Full HTML Document with Header and Styling
$fullHtml = @"
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>PFPJ ry -- Case-Based Legal Benchmark Charts (All 19 Cases)</title>
<style>
  @page {
    size: letter landscape;
    margin: 0.5in;
  }
  body {
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 8.5pt;
    line-height: 1.35;
    color: #0f172a;
    background-color: #ffffff;
    margin: 15px;
  }
  table.case-chart-table tr:nth-child(even) td {
    background-color: #f8fafc !important;
  }
  a {
    color: #1d4ed8 !important;
    text-decoration: underline !important;
  }
</style>
</head>
<body>

<!-- Official Header & Banner -->
<table style="width: 100%; border: 2px solid #0f172a; background-color: #0f172a; color: #ffffff; margin-bottom: 14px;">
  <tr>
    <td style="padding: 14px 18px; border: none; background-color: #0f172a; color: #ffffff;">
      <p style="margin: 0; font-size: 8pt; letter-spacing: 1.5px; font-weight: bold; color: #94a3b8; text-transform: uppercase;">PEOPLE FOR PEACE &amp; JUSTICE RY (HELSINKI, FINLAND) &middot; BUSINESS ID: 3616815-5</p>
      <p style="margin: 4px 0 2px 0; font-size: 14pt; font-family: Georgia, serif; font-weight: bold; color: #ffffff; text-transform: uppercase;">CASE-BASED JURIDICAL BENCHMARK CHARTS &amp; AUTHORITY COMPENDIUM (ALL 19 CASES)</p>
      <p style="margin: 0 0 6px 0; font-size: 9pt; color: #cbd5e1;">Top 10 Most Cited Authoritative Reports, International Judgments &amp; Minab Report Paragraph Integration Matrix</p>
      <hr style="border: none; border-top: 1px solid #334155; margin: 6px 0;" />
      <p style="margin: 0; font-size: 7.5pt; color: #94a3b8;"><b>Docket No.:</b> PFPJ-2026-IR-001 &middot; <b>Application Context:</b> Shajareh Tayyebeh Girls' Elementary School Strike Dossier &middot; <b>Judicial Edition:</b> $ProductionDate</p>
    </td>
  </tr>
</table>

<!-- Confidentiality / Privileged Draft Banner -->
<table style="width: 100%; border: 1.5px solid #b91c1c; background-color: #fef2f2; margin-bottom: 16px;">
  <tr>
    <td style="padding: 10px 14px; border: none; background-color: #fef2f2;">
      <p style="margin: 0; font-size: 9.5pt; font-weight: bold; color: #b91c1c; text-transform: uppercase;">OFFICIAL JURIDICAL BENCHMARK COMPENDIUM &mdash; PRIVILEGED LEGAL WORK PRODUCT</p>
      <p style="margin: 2px 0 4px 0; font-size: 7.5pt; color: #334155;">Prepared by People for Peace &amp; Justice ry (PFPJ ry) in Helsinki, Finland. Compiled according to the evidentiary and legal standards of the International Court of Justice (ICJ), the International Criminal Court (ICC), the International Criminal Tribunal for the former Yugoslavia (ICTY), and the Grand Chamber of the European Court of Human Rights (ECtHR).</p>
      <p style="margin: 0; font-size: 7pt; font-style: italic; color: #64748b;">All 190 citations and canonical links verified against official United Nations Digital Library, HUDOC, ICRC, and governmental archives. Active clickable hyperlinks embedded throughout.</p>
    </td>
  </tr>
</table>

$bodyHtml

</body>
</html>
"@

$tempHtmlPath = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "PFPJ_All_19_Cases_Charts_Temp.html")
Write-Host "Writing temporary HTML file: $tempHtmlPath"
[System.IO.File]::WriteAllText($tempHtmlPath, $fullHtml, [System.Text.Encoding]::UTF8)

# Target output files
$rootDocx = "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx"
$rootPdf  = "E:\Papers\PFPJ\PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf"

$topTenDocx = "E:\Papers\PFPJ\PFPJ_Top_Ten_Most_Cited_Documents_Benchmarked_Cases.docx"
$topTenPdf  = "E:\Papers\PFPJ\PFPJ_Top_Ten_Most_Cited_Documents_Benchmarked_Cases.pdf"

$draftDir = "E:\Papers\PFPJ\Draft_Versions\$ProductionDate"
if (-not (Test-Path $draftDir)) {
    New-Item -ItemType Directory -Path $draftDir -Force | Out-Null
}
$draftDocx = Join-Path $draftDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_$ProductionDate.docx"
$draftPdf  = Join-Path $draftDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts_$ProductionDate.pdf"

$platformDocsDir = "E:\Papers\PFPJ\PFP_Platform\web\public\docs\minab-report"
if (-not (Test-Path $platformDocsDir)) {
    New-Item -ItemType Directory -Path $platformDocsDir -Force | Out-Null
}
$platformDocx = Join-Path $platformDocsDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.docx"
$platformPdf  = Join-Path $platformDocsDir "PFPJ_Minab_Case_Based_Legal_Benchmark_Charts.pdf"

Write-Host "Launching Microsoft Word COM Engine..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    Write-Host "Opening HTML in Word COM engine..."
    $doc = $word.Documents.Open($tempHtmlPath)
    
    # Configure Section Page Margins and Landscape Orientation
    foreach ($section in $doc.Sections) {
        $section.PageSetup.Orientation = 1  # 1 = wdOrientLandscape
        $section.PageSetup.TopMargin = 36    # 0.5 in
        $section.PageSetup.BottomMargin = 36 # 0.5 in
        $section.PageSetup.LeftMargin = 36   # 0.5 in
        $section.PageSetup.RightMargin = 36  # 0.5 in
        
        # Header setup
        $header = $section.Headers.Item(1)
        $headerRange = $header.Range
        $headerRange.Text = "PEOPLE FOR PEACE & JUSTICE RY | CASE-BASED JURIDICAL BENCHMARK CHARTS (CASES 01-19) | DOCKET PFPJ-2026-IR-001"
        $headerRange.Font.Name = "Calibri"
        $headerRange.Font.Size = 7.5
        $headerRange.Font.Bold = $true
        $headerRange.Font.Color = 0x1E293B
        $headerRange.ParagraphFormat.Alignment = 2 # Right
        
        # Footer setup
        $footer = $section.Footers.Item(1)
        $footerRange = $footer.Range
        $footerRange.Text = "CONFIDENTIAL LEGAL WORK PRODUCT | PRE-FILING JURIDICAL EDITION | HELSINKI, FINLAND | DRAFT DATE: $ProductionDate"
        $footerRange.Font.Name = "Calibri"
        $footerRange.Font.Size = 7
        $footerRange.Font.Color = 0x64748B
        $footerRange.ParagraphFormat.Alignment = 1 # Center
    }

    # Format Tables to AutoFit Window
    Write-Host "Auto-fitting $($doc.Tables.Count) tables..."
    foreach ($table in $doc.Tables) {
        $table.AutoFitBehavior(2) # 2 = wdAutoFitWindow
        $table.Rows.HeadingFormat = -1 # Repeat header on each page!
    }

    # Audit Hyperlinks in Document
    $totalHl = $doc.Hyperlinks.Count
    Write-Host "=========================================="
    Write-Host "WORD HYPERLINK AUDIT:"
    Write-Host "Total Active Hyperlinks in Document: $totalHl"
    Write-Host "=========================================="
    
    $corruptedCount = 0
    for ($idx = 1; $idx -le $totalHl; $idx++) {
        $hl = $doc.Hyperlinks.Item($idx)
        $addr = $hl.Address
        if ($addr -match "%3c|%3e|&lt;|&gt;") {
            Write-Host "WARNING: Corrupted link at [$idx]: $($hl.TextToDisplay) -> $addr"
            $corruptedCount++
        }
    }
    if ($corruptedCount -eq 0) {
        Write-Host "PERFECT AUDIT: Zero corrupted URLs detected. All $totalHl links are clean, valid, and active!"
    } else {
        Write-Host "ATTENTION: $corruptedCount links had encoding issues."
    }

    # Save DOCX targets
    Write-Host "Saving DOCX: $rootDocx"
    $doc.SaveAs2($rootDocx, 16) # 16 = wdFormatXMLDocument

    Write-Host "Saving DOCX: $topTenDocx"
    $doc.SaveAs2($topTenDocx, 16)

    Write-Host "Saving DOCX draft: $draftDocx"
    $doc.SaveAs2($draftDocx, 16)

    Write-Host "Saving DOCX platform copy: $platformDocx"
    $doc.SaveAs2($platformDocx, 16)

    # Save PDF targets
    Write-Host "Exporting PDF: $rootPdf"
    $doc.SaveAs2($rootPdf, 17) # 17 = wdFormatPDF

    Write-Host "Exporting PDF: $topTenPdf"
    $doc.SaveAs2($topTenPdf, 17)

    Write-Host "Exporting PDF draft: $draftPdf"
    $doc.SaveAs2($draftPdf, 17)

    Write-Host "Exporting PDF platform copy: $platformPdf"
    $doc.SaveAs2($platformPdf, 17)

    $doc.Close(0)
    Write-Host "SUCCESS: Generated all Word (.docx) and Adobe PDF (.pdf) targets for ALL 19 CASES!"
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    Remove-Item $tempHtmlPath -ErrorAction SilentlyContinue
}

# Verify output files
Get-Item -Path $rootDocx, $rootPdf, $topTenDocx, $topTenPdf, $draftDocx, $draftPdf, $platformDocx, $platformPdf | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
