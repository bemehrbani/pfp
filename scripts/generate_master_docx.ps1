# scripts/generate_master_docx.ps1
# Generates professional MS Word (.docx) editions of the Minab Master Report

param (
    [string]$SourceMd = "E:\Papers\PFPJ\Campaigns\minab\justiceForMinab\docs\FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md",
    [string]$ProductionDate = "2026-10-18"
)

$ErrorActionPreference = "Stop"

Write-Host ("Reading Markdown source: " + $SourceMd)
if (-not (Test-Path $SourceMd)) {
    throw ("Source Markdown file not found: " + $SourceMd)
}

$lines = Get-Content -Path $SourceMd -Encoding utf8

function Format-Inline ($text) {
    if ([string]::IsNullOrEmpty($text)) { return "" }
    $text = $text -replace '&(?!#?[a-zA-Z0-9]+;)', '&amp;'
    
    # Bold + Italic
    $text = [regex]::Replace($text, '\*\*\*(.*?)\*\*\*', '<b><i>$1</i></b>')
    # Bold
    $text = [regex]::Replace($text, '\*\*(.*?)\*\*', '<b>$1</b>')
    # Italic
    $text = [regex]::Replace($text, '(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', '<i>$1</i>')
    $text = [regex]::Replace($text, '(?<!_)_(?!_)(.*?)(?<!_)_(?!_)', '<i>$1</i>')
    # Inline code
    $text = [regex]::Replace($text, '`([^`]+)`', '<code style="font-family: Consolas, monospace; background-color: #f1f5f9; padding: 2px 4px; border-radius: 3px; font-size: 0.9em; color: #831843;">$1</code>')
    # Markdown links
    $text = [regex]::Replace($text, '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2" style="color: #2563eb; text-decoration: underline;">$1</a>')
    # Math / Ballistic notations
    $text = $text -replace '\$M_L = ([0-9.]+)\$', '<i>M</i><sub>L</sub> = $1'
    $text = $text -replace '\$\\Delta t = ([0-9.]+) seconds\$', '&Delta;<i>t</i> = $1 seconds'
    return $text
}

$html = New-Object System.Text.StringBuilder
$inTable = $false
$inQuote = $false
$inUl = $false
$tableRows = New-Object System.Collections.Generic.List[string]

function Close-Blocks {
    if ($script:inQuote) {
        $html.AppendLine("</blockquote>") | Out-Null
        $script:inQuote = $false
    }
    if ($script:inUl) {
        $html.AppendLine("</ul>") | Out-Null
        $script:inUl = $false
    }
}

function Render-Table ($rows) {
    if ($rows.Count -eq 0) { return }
    $html.AppendLine("<table class='judicial-table' style='width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 9pt; font-family: Calibri, sans-serif;'>") | Out-Null
    $isFirst = $true
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

        $html.AppendLine("  <tr>") | Out-Null
        foreach ($c in $cells) {
            $cellText = Format-Inline ($c.Trim())
            if ($isFirst) {
                $html.AppendLine("    <th style='background-color: #0f172a; color: #ffffff; padding: 8px 10px; border: 1px solid #94a3b8; text-align: left; font-weight: bold;'>$cellText</th>") | Out-Null
            } else {
                $html.AppendLine("    <td style='padding: 6px 10px; border: 1px solid #cbd5e1; vertical-align: top; background-color: #ffffff;'>$cellText</td>") | Out-Null
            }
        }
        $html.AppendLine("  </tr>") | Out-Null
        $isFirst = $false
    }
    $html.AppendLine("</table>") | Out-Null
}

# HTML Page Header with Callout Banner
$headerHtml = @'
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 10.5pt;
    line-height: 1.4;
    color: #1e293b;
    margin: 30px;
  }
  h1 { font-family: 'Georgia', serif; font-size: 17pt; color: #0f172a; margin-top: 24px; margin-bottom: 8px; font-weight: bold; border-bottom: 2px solid #0f172a; padding-bottom: 4px; text-transform: uppercase; }
  h2 { font-family: 'Georgia', serif; font-size: 14pt; color: #1e293b; margin-top: 20px; margin-bottom: 6px; font-weight: bold; border-bottom: 1px solid #94a3b8; padding-bottom: 3px; }
  h3 { font-family: 'Calibri', sans-serif; font-size: 12pt; color: #0f172a; margin-top: 16px; margin-bottom: 4px; font-weight: bold; }
  h4 { font-family: 'Calibri', sans-serif; font-size: 10.5pt; color: #334155; margin-top: 12px; margin-bottom: 4px; font-weight: bold; font-style: italic; }
  p { margin: 0 0 6px 0; text-align: justify; }
  blockquote { margin: 10px 0 10px 16px; padding: 8px 14px; border-left: 3.5px solid #0f172a; background-color: #f8fafc; font-style: italic; color: #334155; }
  ul { margin: 4px 0 8px 20px; padding-left: 8px; }
  li { margin-bottom: 3px; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; }
  th, td { border: 1px solid #cbd5e1; padding: 6px 8px; vertical-align: top; }
  th { background-color: #0f172a; color: white; font-weight: bold; }
</style>
</head>
<body>

<!-- Working Draft Banner Table -->
<table style="width: 100%; border: 1.5px solid #b91c1c; background-color: #fef2f2; margin-bottom: 20px;">
  <tr>
    <td style="padding: 14px 18px; border: none; background-color: #fef2f2;">
      <p style="margin: 0; font-size: 12pt; font-weight: bold; color: #b91c1c; text-transform: uppercase;">WORKING DRAFT &mdash; PRIVATELY SHARED FOR FEEDBACK</p>
      <p style="margin: 3px 0 6px 0; font-size: 8.5pt; font-weight: bold; color: #991b1b; text-transform: uppercase;">CONFIDENTIAL &amp; PRIVILEGED &middot; FOR PRE-FILING REVIEW &amp; EDITORIAL CONSULTATION ONLY</p>
      <p style="margin: 0 0 4px 0; font-size: 8.5pt; color: #334155;">This document constitutes an official preliminary working draft prepared by People for Peace &amp; Justice ry (PFPJ ry) in relation to Docket No. PFPJ-2026-IR-001. It is circulated on a strictly confidential basis to designated legal counsel, forensic specialists, and reviewers for feedback. It must not be cited, copied, or circulated in public without prior written authorization.</p>
      <p style="margin: 0; font-size: 8pt; font-style: italic; color: #64748b;">Status: Working Draft (Pre-Filing Judicial Edition) &middot; Helsinki, Finland</p>
    </td>
  </tr>
</table>
'@

$html.AppendLine($headerHtml) | Out-Null

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $trimmed = $line.Trim()

    if ($trimmed -match '^<a id="([^"]+)"></a>$') {
        $anchor = $matches[1]
        $html.AppendLine("<a name='$anchor'></a>") | Out-Null
        continue
    }

    if ($trimmed.StartsWith('|') -and $trimmed.EndsWith('|')) {
        Close-Blocks
        $tableRows.Add($trimmed)
        $inTable = $true
        continue
    } else {
        if ($inTable) {
            Render-Table ($tableRows)
            $tableRows.Clear()
            $inTable = $false
        }
    }

    if ($trimmed -match '^(---|\*\*\*|___)$') {
        Close-Blocks
        $html.AppendLine("<hr style='border: none; border-top: 1px solid #cbd5e1; margin: 18px 0;' />") | Out-Null
        continue
    }

    if ($trimmed -match '^(#{1,5})\s+(.*)$') {
        Close-Blocks
        $level = $matches[1].Length
        $htext = Format-Inline ($matches[2])
        
        if ($level -eq 1) {
            $html.AppendLine("<h1>$htext</h1>") | Out-Null
        } elseif ($level -eq 2) {
            $html.AppendLine("<h2>$htext</h2>") | Out-Null
        } elseif ($level -eq 3) {
            $html.AppendLine("<h3>$htext</h3>") | Out-Null
        } else {
            $html.AppendLine("<h4>$htext</h4>") | Out-Null
        }
        continue
    }

    if ($trimmed.StartsWith('>')) {
        if (-not $script:inQuote) {
            Close-Blocks
            $html.AppendLine("<blockquote>") | Out-Null
            $script:inQuote = $true
        }
        $qtext = $trimmed.Substring(1).Trim()
        $qformatted = Format-Inline ($qtext)
        $html.AppendLine("<p style='margin: 3px 0;'>$qformatted</p>") | Out-Null
        continue
    } else {
        if ($script:inQuote) {
            $html.AppendLine("</blockquote>") | Out-Null
            $script:inQuote = $false
        }
    }

    if ($trimmed -match '^(\*|-)\s+(.*)$') {
        if (-not $script:inUl) {
            Close-Blocks
            $html.AppendLine("<ul>") | Out-Null
            $script:inUl = $true
        }
        $litext = Format-Inline ($matches[2])
        $html.AppendLine("  <li>$litext</li>") | Out-Null
        continue
    }

    if ([string]::IsNullOrWhiteSpace($trimmed)) {
        Close-Blocks
        continue
    }

    Close-Blocks
    $pformatted = Format-Inline ($trimmed)
    $html.AppendLine("<p>$pformatted</p>") | Out-Null
}

Close-Blocks
if ($inTable) {
    Render-Table ($tableRows)
}

$html.AppendLine("</body></html>") | Out-Null

$tempHtmlPath = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "PFPJ_Minab_Report_Temp.html")
Write-Host ("Writing temporary HTML file: " + $tempHtmlPath)
[System.IO.File]::WriteAllText($tempHtmlPath, $html.ToString(), [System.Text.Encoding]::UTF8)

# Destination paths
$destDocsDir = [System.IO.Path]::GetDirectoryName($SourceMd)
$draftsDir = ("E:\Papers\PFPJ\Draft_Versions\" + $ProductionDate)
if (-not (Test-Path $draftsDir)) {
    New-Item -ItemType Directory -Path $draftsDir -Force | Out-Null
}
$platformDocsDir = "E:\Papers\PFPJ\PFP_Platform\web\public\docs\minab-report"
if (-not (Test-Path $platformDocsDir)) {
    New-Item -ItemType Directory -Path $platformDocsDir -Force | Out-Null
}

$isAnnex = $SourceMd -match "MASTER_EXHIBIT_DOSSIER"

if ($isAnnex) {
    $mainDocxDest = [System.IO.Path]::Combine($destDocsDir, "MASTER_EXHIBIT_DOSSIER.docx")
    $datedDocxDest = [System.IO.Path]::Combine($draftsDir, ("PFPJ_Minab_Master_Exhibit_Dossier_Annex_" + $ProductionDate + "_Draft.docx"))
    $platformDocxDest = [System.IO.Path]::Combine($platformDocsDir, "PFPJ_Minab_Master_Exhibit_Dossier_Annex.docx")
    $headerText = "WORKING DRAFT -- PRIVATELY SHARED FOR FEEDBACK | MASTER EXHIBIT COMPENDIUM"
    $footerText = "CONFIDENTIAL | PEOPLE FOR PEACE & JUSTICE RY | EXHIBIT DOSSIER PFPJ-2026-IR-001 | DRAFT DATE: " + $ProductionDate
} else {
    $mainDocxDest = [System.IO.Path]::Combine($destDocsDir, "FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.docx")
    $datedDocxDest = [System.IO.Path]::Combine($draftsDir, ("PFPJ_Minab_Factual_Determination_Main_Report_" + $ProductionDate + "_Draft.docx"))
    $platformDocxDest = [System.IO.Path]::Combine($platformDocsDir, "PFPJ_Minab_Master_Factual_Determination_Report.docx")
    $headerText = "WORKING DRAFT -- PRIVATELY SHARED FOR FEEDBACK | NOT FOR PUBLIC CITATION"
    $footerText = "CONFIDENTIAL | PEOPLE FOR PEACE & JUSTICE RY | DOCKET PFPJ-2026-IR-001 | DRAFT DATE: " + $ProductionDate
}

Write-Host "Launching Microsoft Word COM engine to compile DOCX..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($tempHtmlPath)
    
    # Configure Section Page Margins: 0.75 in (54 pt)
    foreach ($section in $doc.Sections) {
        $section.PageSetup.TopMargin = 54
        $section.PageSetup.BottomMargin = 54
        $section.PageSetup.LeftMargin = 54
        $section.PageSetup.RightMargin = 54
        
        # Header setup
        $header = $section.Headers.Item(1)
        $headerRange = $header.Range
        $headerRange.Text = $headerText
        $headerRange.Font.Name = "Calibri"
        $headerRange.Font.Size = 8.5
        $headerRange.Font.Bold = $true
        $headerRange.Font.Color = 0x1C1CB9
        $headerRange.ParagraphFormat.Alignment = 2
        
        # Footer setup
        $footer = $section.Footers.Item(1)
        $footerRange = $footer.Range
        $footerRange.Text = $footerText
        $footerRange.Font.Name = "Calibri"
        $footerRange.Font.Size = 8
        $footerRange.Font.Color = 0x8B7464
        $footerRange.ParagraphFormat.Alignment = 1
    }

    # Format Tables to AutoFit Window
    foreach ($table in $doc.Tables) {
        $table.AutoFitBehavior(2)
    }

    # Save to primary location
    Write-Host ("Saving Word document: " + $mainDocxDest)
    $doc.SaveAs2($mainDocxDest, 16)

    # Save to dated Draft_Versions
    Write-Host ("Saving dated draft copy: " + $datedDocxDest)
    $doc.SaveAs2($datedDocxDest, 16)

    # Save to platform web docs
    Write-Host ("Saving platform web copy: " + $platformDocxDest)
    $doc.SaveAs2($platformDocxDest, 16)

    $doc.Close()
    Write-Host "Successfully generated all DOCX targets!"
}
finally {
    $word.Quit()
    Remove-Item $tempHtmlPath -ErrorAction SilentlyContinue
}

# Verify output files
Get-Item -Path $mainDocxDest, $datedDocxDest, $platformDocxDest | Select-Object FullName, Length, LastWriteTime
