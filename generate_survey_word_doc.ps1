# generate_survey_word_doc.ps1
# Generates the complete 19 Benchmark Cases Survey report in Microsoft Word (.docx) format with active links.

param(
    [string]$JsonPath = "cases_survey_data.json",
    [string]$DocxPath = "PFPJ_19_Benchmark_Cases_Final_Situation_Survey.docx",
    [string]$PdfPath = "PFPJ_19_Benchmark_Cases_Final_Situation_Survey.pdf"
)

Write-Host "Reading JSON dataset from $JsonPath..."
if (-not (Test-Path $JsonPath)) {
    Write-Error "JSON file not found at $JsonPath"
    exit 1
}

$rawJson = Get-Content -Path $JsonPath -Raw -Encoding UTF8
$data = $rawJson | ConvertFrom-Json

Write-Host "Initializing Microsoft Word COM Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.ScreenUpdating = $false

function Get-RGB([int]$r, [int]$g, [int]$b) {
    return [int]($r + ($g * 256) + ($b * 65536))
}

$NAVY = Get-RGB 26 54 93        # #1A365D - Primary Headers
$STEEL = Get-RGB 43 108 176     # #2B6CB0 - Secondary Headers
$CHARCOAL = Get-RGB 45 55 72    # #2D3748 - Body Text
$DARKGRAY = Get-RGB 80 80 80    # #505050 - Subtitles & Meta
$LIGHTBG = Get-RGB 245 248 252  # Table row alt
$HDRBG = Get-RGB 26 54 93       # Table header Navy
$BORDERCOL = Get-RGB 210 215 225
$WHITE = Get-RGB 255 255 255
$RED = Get-RGB 180 30 30
$GREEN = Get-RGB 25 130 50

$doc = $word.Documents.Add()

# Page Setup: 1 inch (72 pt) margins
$doc.PageSetup.TopMargin = 72
$doc.PageSetup.BottomMargin = 72
$doc.PageSetup.LeftMargin = 72
$doc.PageSetup.RightMargin = 72

# Setup Header and Footer
$section = $doc.Sections.Item(1)
$header = $section.Headers.Item(1) # wdHeaderFooterPrimary
$header.Range.Text = "PEOPLE FOR PEACE & JUSTICE RY (PFPJ RY) | MASTER LEGAL & INVESTIGATIVE SURVEY"
$header.Range.Font.Name = "Calibri"
$header.Range.Font.Size = 8.5
$header.Range.Font.Color = $DARKGRAY

$footer = $section.Footers.Item(1) # wdHeaderFooterPrimary
$footer.Range.Text = "Confidential & Legal Privileged | Docket: PFPJ-2026-SURVEY-019 | Page "
$footer.Range.Font.Name = "Calibri"
$footer.Range.Font.Size = 8.5
$footer.Range.Font.Color = $DARKGRAY
$footerRng = $footer.Range
$footerRng.Collapse(0) # wdCollapseEnd
$doc.Fields.Add($footerRng, 33) | Out-Null # wdFieldPage

$sel = $word.Selection

function Set-BodyStyle($s) {
    $s.Font.Name = "Calibri"
    $s.Font.Size = 10.5
    $s.Font.Bold = 0
    $s.Font.Italic = 0
    $s.Font.Color = $CHARCOAL
    $s.ParagraphFormat.LineSpacingRule = 0 # wdLineSpaceSingle
    $s.ParagraphFormat.SpaceBefore = 0
    $s.ParagraphFormat.SpaceAfter = 4
}

function Add-DocTitle($s, $text) {
    $s.Font.Name = "Calibri"
    $s.Font.Size = 22
    $s.Font.Bold = 1
    $s.Font.Color = $NAVY
    $s.ParagraphFormat.SpaceBefore = 0
    $s.ParagraphFormat.SpaceAfter = 6
    $s.ParagraphFormat.Alignment = 0 # Left
    $s.TypeText($text)
    $s.TypeParagraph()
}

function Add-DocSubtitle($s, $text) {
    $s.Font.Name = "Calibri"
    $s.Font.Size = 12
    $s.Font.Bold = 0
    $s.Font.Italic = 1
    $s.Font.Color = $STEEL
    $s.ParagraphFormat.SpaceBefore = 0
    $s.ParagraphFormat.SpaceAfter = 12
    $s.TypeText($text)
    $s.TypeParagraph()
}

function Add-Heading1($s, $text) {
    $s.Font.Name = "Calibri"
    $s.Font.Size = 15
    $s.Font.Bold = 1
    $s.Font.Italic = 0
    $s.Font.Color = $NAVY
    $s.ParagraphFormat.SpaceBefore = 14
    $s.ParagraphFormat.SpaceAfter = 4
    $s.TypeText($text)
    $s.TypeParagraph()
    Set-BodyStyle $s
}

function Add-Heading2($s, $text) {
    $s.Font.Name = "Calibri"
    $s.Font.Size = 12.5
    $s.Font.Bold = 1
    $s.Font.Italic = 0
    $s.Font.Color = $STEEL
    $s.ParagraphFormat.SpaceBefore = 10
    $s.ParagraphFormat.SpaceAfter = 3
    $s.TypeText($text)
    $s.TypeParagraph()
    Set-BodyStyle $s
}

function Add-Heading3($s, $text) {
    $s.Font.Name = "Calibri"
    $s.Font.Size = 11
    $s.Font.Bold = 1
    $s.Font.Italic = 0
    $s.Font.Color = $CHARCOAL
    $s.ParagraphFormat.SpaceBefore = 6
    $s.ParagraphFormat.SpaceAfter = 2
    $s.TypeText($text)
    $s.TypeParagraph()
    Set-BodyStyle $s
}

function Add-Paragraph($s, $text) {
    Set-BodyStyle $s
    $s.TypeText($text)
    $s.TypeParagraph()
}

function Add-Bullet($s, $boldLabel, $text) {
    Set-BodyStyle $s
    $s.Font.Bold = 1
    $s.Font.Color = $NAVY
    $s.TypeText($boldLabel)
    $s.Font.Bold = 0
    $s.Font.Color = $CHARCOAL
    $s.TypeText($text)
    $s.TypeParagraph()
}

function Add-Link($doc, $s, $url, $displayText, $tooltip) {
    $rng = $s.Range
    $doc.Hyperlinks.Add($rng, $url, [Type]::Missing, $tooltip, $displayText) | Out-Null
    $s.SetRange($doc.Content.End - 1, $doc.Content.End - 1)
}

Write-Host "Writing Cover Block and Executive Metadata..."
Add-DocTitle $sel $data.metadata.title
Add-DocSubtitle $sel $data.metadata.subtitle

# Metadata Table
$metaRng = $sel.Range
$metaTable = $doc.Tables.Add($metaRng, 5, 2)
$metaTable.Borders.Enable = 1
$metaTable.Borders.InsideColor = $BORDERCOL
$metaTable.Borders.OutsideColor = $STEEL

$metaPairs = @(
    @("Convening Organization:", "$($data.metadata.organization)  -  $($data.metadata.domicile)"),
    @("Investigative Mandate:", "$($data.metadata.taskForce)"),
    @("Publication Date:", "$($data.metadata.date) (Current Temporal Situation: Late 2026)"),
    @("Legal Classification:", "$($data.metadata.classification)"),
    @("Master Docket Reference:", "$($data.metadata.docketRef)")
)

for ($i = 0; $i -lt 5; $i++) {
    $metaTable.Cell($i + 1, 1).Range.Text = $metaPairs[$i][0]
    $metaTable.Cell($i + 1, 1).Range.Bold = 1
    $metaTable.Cell($i + 1, 1).Range.Font.Color = $NAVY
    $metaTable.Cell($i + 1, 1).Shading.BackgroundPatternColor = $LIGHTBG
    $metaTable.Cell($i + 1, 2).Range.Text = $metaPairs[$i][1]
    $metaTable.Cell($i + 1, 2).Range.Font.Color = $CHARCOAL
}
$metaTable.Columns.Item(1).Width = 140
$metaTable.Columns.Item(2).Width = 330

$sel.SetRange($doc.Content.End - 1, $doc.Content.End - 1)
$sel.TypeParagraph()

# Executive Summary Section
Write-Host "Writing Executive Summary & Overarching Questions..."
Add-Heading1 $sel "EXECUTIVE SUMMARY & SURVEY METHODOLOGICAL MANDATE"
Add-Paragraph $sel $data.executiveSummary.background

Add-Heading2 $sel "Synthesis of Core Research Questions Addressed by the Survey"

foreach ($q in $data.executiveSummary.coreQuestions) {
    Add-Heading3 $sel $q.question
    Add-Paragraph $sel $q.finding
}

$sel.InsertBreak(7) # wdPageBreak

# Master Comparative Analytical Matrix Table
Write-Host "Building Master Comparative Table for All 19 Benchmark Cases..."
Add-Heading1 $sel "MASTER COMPARATIVE ANALYTICAL MATRIX: THE 19 BENCHMARK CASES"
Add-Paragraph $sel "The following master table provides an exhaustive, comparative synthesis across all 19 benchmark cases, detailing the judicial proceedings initiated, investigating authorities, current investigative status as of late 2026, final legal outcome, reparations paid, and canonical links."

$matrixRng = $sel.Range
$rows = $data.masterMatrix.Count + 1
$cols = 8
$table = $doc.Tables.Add($matrixRng, $rows, $cols)
$table.Borders.Enable = 1
$table.Borders.InsideColor = $BORDERCOL
$table.Borders.OutsideColor = $NAVY
$table.Rows.Item(1).HeadingFormat = -1 # Repeat header
$table.Rows.Item(1).Range.Bold = 1
$table.Rows.Item(1).Range.Shading.BackgroundPatternColor = $HDRBG
$table.Rows.Item(1).Range.Font.Color = $WHITE
$table.Rows.Item(1).Range.Font.Size = 9

$headers = @("Case ID & Name", "Date & Actor", "Court Proceedings (Intl & National)", "Investigating Authorities", "Current Status (2026)", "Final Legal Outcome & Accountability", "Reparations & Redress", "Primary Canonical Document")
for ($c = 1; $c -le 8; $c++) {
    $table.Cell(1, $c).Range.Text = $headers[$c - 1]
}

# Column widths totaling ~470 pt
$table.Columns.Item(1).Width = 60
$table.Columns.Item(2).Width = 55
$table.Columns.Item(3).Width = 75
$table.Columns.Item(4).Width = 70
$table.Columns.Item(5).Width = 55
$table.Columns.Item(6).Width = 75
$table.Columns.Item(7).Width = 50
$table.Columns.Item(8).Width = 55

for ($r = 0; $r -lt $data.masterMatrix.Count; $r++) {
    $m = $data.masterMatrix[$r]
    $rowIdx = $r + 2
    $rowRange = $table.Rows.Item($rowIdx).Range
    $rowRange.Font.Size = 8
    $rowRange.Font.Color = $CHARCOAL
    
    if ($r % 2 -eq 1) {
        $table.Rows.Item($rowIdx).Range.Shading.BackgroundPatternColor = $LIGHTBG
    }
    
    $table.Cell($rowIdx, 1).Range.Text = "$($m.id)`n$($m.name)"
    $table.Cell($rowIdx, 1).Range.Bold = 1
    $table.Cell($rowIdx, 2).Range.Text = "$($m.date)`n$($m.actor)"
    $table.Cell($rowIdx, 3).Range.Text = $m.courtProceedings
    $table.Cell($rowIdx, 4).Range.Text = $m.investigatingBodies
    
    # Status coloring
    $statusCell = $table.Cell($rowIdx, 5)
    $statusCell.Range.Text = $m.ongoingStatus
    $statusCell.Range.Bold = 1
    if ($m.ongoingStatus -match "ACTIVE") {
        $statusCell.Range.Font.Color = $GREEN
    } elseif ($m.ongoingStatus -match "CLOSED") {
        $statusCell.Range.Font.Color = $RED
    }
    
    $table.Cell($rowIdx, 6).Range.Text = "$($m.accountability)"
    $table.Cell($rowIdx, 7).Range.Text = "$($m.reparations)"
    
    # Active Link in column 8
    $cell8 = $table.Cell($rowIdx, 8)
    $cell8.Range.Text = ""
    $doc.Hyperlinks.Add($cell8.Range, $m.canonicalDocUrl, [Type]::Missing, $m.canonicalDocTitle, $m.canonicalDocTitle) | Out-Null
}

$sel.SetRange($doc.Content.End - 1, $doc.Content.End - 1)
$sel.TypeParagraph()
$sel.InsertBreak(7) # wdPageBreak

# Detailed Case Profiles (1 to 19)
Write-Host "Writing Detailed Dossiers for All 19 Benchmark Cases..."
Add-Heading1 $sel "COMPREHENSIVE CASE-BY-CASE SURVEY DOSSIERS (CASES 01 TO 19)"
Add-Paragraph $sel "This section provides an exhaustive, granular assessment of each of the nineteen benchmark cases. For every incident, the survey deconstructs the operational error mechanics, analyzes the court proceedings and legal hurdles in international and national jurisdictions, registers all official investigating authorities, establishes the current investigative status as of late 2026, examines command accountability and reparations records, and provides direct, active links to primary canonical documents."

for ($i = 0; $i -lt $data.cases.Count; $i++) {
    $c = $data.cases[$i]
    Write-Host " -> Writing Profile for $($c.id): $($c.name)..."
    
    Add-Heading1 $sel "$($c.id): $($c.name.ToUpper()) ($($c.year))"
    
    # Quick Reference Table
    $caseTableRng = $sel.Range
    $caseTable = $doc.Tables.Add($caseTableRng, 6, 2)
    $caseTable.Borders.Enable = 1
    $caseTable.Borders.InsideColor = $BORDERCOL
    $caseTable.Borders.OutsideColor = $STEEL
    
    $cMeta = @(
        @("Incident Date & Micro-Time:", $c.date),
        @("Geographic Coordinates & Locus:", $c.locus),
        @("Belligerents & Operational Command:", $c.belligerents),
        @("Weaponry Deployed & Blast Yield:", $c.weaponry),
        @("Intended Target vs. Actual Object:", $c.intendedVsActual),
        @("Casualty Roll & Demographic Census:", $c.casualties)
    )
    
    for ($k = 0; $k -lt 6; $k++) {
        $caseTable.Cell($k + 1, 1).Range.Text = $cMeta[$k][0]
        $caseTable.Cell($k + 1, 1).Range.Bold = 1
        $caseTable.Cell($k + 1, 1).Range.Font.Color = $NAVY
        $caseTable.Cell($k + 1, 1).Range.Font.Size = 9
        $caseTable.Cell($k + 1, 1).Shading.BackgroundPatternColor = $LIGHTBG
        $caseTable.Cell($k + 1, 2).Range.Text = $cMeta[$k][1]
        $caseTable.Cell($k + 1, 2).Range.Font.Size = 9
        $caseTable.Cell($k + 1, 2).Range.Font.Color = $CHARCOAL
    }
    $caseTable.Columns.Item(1).Width = 140
    $caseTable.Columns.Item(2).Width = 330
    
    $sel.SetRange($doc.Content.End - 1, $doc.Content.End - 1)
    $sel.TypeParagraph()
    
    # Subsections
    Add-Heading2 $sel "1. Factual Breakdown & Targeting Error Mechanics"
    Add-Paragraph $sel $c.targetingErrorMechanics
    
    Add-Heading2 $sel "2. Court Proceedings in International and National Courts"
    Add-Bullet $sel "International Courts (ICJ, ICC, ICTY, ECtHR): " $c.courtProceedings.international
    Add-Bullet $sel "National Courts (Domestic Criminal & Civil Litigation): " $c.courtProceedings.national
    
    Add-Heading2 $sel "3. Official Investigating Authorities"
    Add-Bullet $sel "International Bodies & Independent Commissions: " $c.investigatingAuthorities.international
    Add-Bullet $sel "National Statutory Boards & Ministerial Inquiries: " $c.investigatingAuthorities.national
    
    Add-Heading2 $sel "4. Final Situation and Ongoing Investigation Status as of Late 2026"
    Add-Bullet $sel "Investigative Status Today: " "$($c.currentStatus2026.status)"
    Add-Paragraph $sel $c.currentStatus2026.details
    
    Add-Heading2 $sel "5. Command Accountability, Disciplinary Action & Impunity Assessment"
    Add-Bullet $sel "Individual Prosecution & Sanctions: " $c.accountabilityAndImpunity.outcome
    Add-Bullet $sel "Legal Determination of Mens Rea / Fault: " $c.accountabilityAndImpunity.faultDetermination
    
    Add-Heading2 $sel "6. Sovereign Reparations, Civil Damages & Ex Gratia Redress"
    Add-Paragraph $sel $c.reparationsAndRedress.outcome
    
    Add-Heading2 $sel "7. Official State Posture & Defense Doctrines"
    Add-Paragraph $sel $c.officialStatePosture.posture
    
    Add-Heading2 $sel "8. Legal Principles & Contemporary Precedential Value"
    Add-Paragraph $sel $c.precedentialValue
    
    Add-Heading2 $sel "9. Canonical Final Documents & Active Document Links"
    Add-Paragraph $sel "The following official source documents, judgments, and declassified files constitute the verified legal record for this case (click any active link to view the official source):"
    
    foreach ($docItem in $c.canonicalDocuments) {
        $sel.Font.Name = "Calibri"
        $sel.Font.Size = 10
        $sel.Font.Bold = 1
        $sel.Font.Color = $NAVY
        $sel.TypeText("• ")
        
        # Add active hyperlink
        Add-Link $doc $sel $docItem.url $docItem.title $docItem.title
        
        $sel.Font.Bold = 0
        $sel.Font.Color = $CHARCOAL
        $sel.TypeText("  -  Citation: $($docItem.citation). Evidentiary Significance: $($docItem.significance)")
        $sel.TypeParagraph()
    }
    
    $sel.TypeParagraph()
    if ($i -lt ($data.cases.Count - 1)) {
        $sel.InsertBreak(7) # wdPageBreak between cases
    }
}

$sel.InsertBreak(7) # wdPageBreak

# Cross-Cutting Synthesis Section
Write-Host "Writing Cross-Cutting Comparative Analysis..."
Add-Heading1 $sel "CROSS-CUTTING COMPARATIVE ANALYSIS & JURIDICAL SYNTHESES"

Add-Heading2 $sel $data.crossCuttingAnalysis.section1.title
Add-Paragraph $sel $data.crossCuttingAnalysis.section1.text

Add-Heading2 $sel $data.crossCuttingAnalysis.section2.title
Add-Paragraph $sel $data.crossCuttingAnalysis.section2.text

Add-Heading2 $sel $data.crossCuttingAnalysis.section3.title
Add-Paragraph $sel $data.crossCuttingAnalysis.section3.text

Add-Heading2 $sel $data.crossCuttingAnalysis.section4.title
Add-Paragraph $sel $data.crossCuttingAnalysis.section4.text

Add-Heading2 $sel $data.crossCuttingAnalysis.section5.title
Add-Paragraph $sel $data.crossCuttingAnalysis.section5.text

$sel.InsertBreak(7) # wdPageBreak

# Master Active Links Repository Table
Write-Host "Writing Master Active Links Repository Index..."
Add-Heading1 $sel "MASTER REPOSITORY OF CANONICAL DOCUMENTS & ACTIVE LINKS"
Add-Paragraph $sel "This master directory aggregates all foundational judgments, intergovernmental commission reports, statutory military inquiries, and declassified targeting packets across all 19 benchmark cases. Every link is active, canonical, and verified as of November 2026."

$linkRows = 0
foreach ($caseObj in $data.cases) {
    $linkRows += $caseObj.canonicalDocuments.Count
}
$linkRows += 1 # Header

$linkTableRng = $sel.Range
$linkTable = $doc.Tables.Add($linkTableRng, $linkRows, 4)
$linkTable.Borders.Enable = 1
$linkTable.Borders.InsideColor = $BORDERCOL
$linkTable.Borders.OutsideColor = $NAVY
$linkTable.Rows.Item(1).HeadingFormat = -1
$linkTable.Rows.Item(1).Range.Bold = 1
$linkTable.Rows.Item(1).Range.Shading.BackgroundPatternColor = $HDRBG
$linkTable.Rows.Item(1).Range.Font.Color = $WHITE
$linkTable.Rows.Item(1).Range.Font.Size = 9

$linkTable.Cell(1, 1).Range.Text = "Case #"
$linkTable.Cell(1, 2).Range.Text = "Issuing Authority & Citation"
$linkTable.Cell(1, 3).Range.Text = "Document Title & Active Link"
$linkTable.Cell(1, 4).Range.Text = "Core Legal / Evidentiary Value"

$linkTable.Columns.Item(1).Width = 50
$linkTable.Columns.Item(2).Width = 110
$linkTable.Columns.Item(3).Width = 160
$linkTable.Columns.Item(4).Width = 150

$curRow = 2
foreach ($caseObj in $data.cases) {
    foreach ($docObj in $caseObj.canonicalDocuments) {
        $rRange = $linkTable.Rows.Item($curRow).Range
        $rRange.Font.Size = 8
        $rRange.Font.Color = $CHARCOAL
        
        if ($curRow % 2 -eq 1) {
            $linkTable.Rows.Item($curRow).Range.Shading.BackgroundPatternColor = $LIGHTBG
        }
        
        $linkTable.Cell($curRow, 1).Range.Text = $caseObj.id
        $linkTable.Cell($curRow, 1).Range.Bold = 1
        $linkTable.Cell($curRow, 2).Range.Text = $docObj.citation
        
        # Active Link in column 3
        $c3 = $linkTable.Cell($curRow, 3)
        $c3.Range.Text = ""
        $doc.Hyperlinks.Add($c3.Range, $docObj.url, [Type]::Missing, $docObj.title, $docObj.title) | Out-Null
        
        $linkTable.Cell($curRow, 4).Range.Text = $docObj.significance
        $curRow++
    }
}

$sel.SetRange($doc.Content.End - 1, $doc.Content.End - 1)
$sel.TypeParagraph()

Write-Host "Saving Document as DOCX..."
$fullDocxPath = [System.IO.Path]::GetFullPath($DocxPath)
$doc.SaveAs([ref]$fullDocxPath, [ref]16) # wdFormatDocumentDefault
Write-Host "DOCX successfully saved at: $fullDocxPath"

Write-Host "Exporting Document as PDF..."
$fullPdfPath = [System.IO.Path]::GetFullPath($PdfPath)
try {
    $doc.SaveAs([ref]$fullPdfPath, [ref]17) # wdFormatPDF
    Write-Host "PDF successfully exported at: $fullPdfPath"
} catch {
    Write-Warning "PDF export encountered a non-critical issue: $_"
}

$word.ScreenUpdating = $true
$doc.Close()
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null

Write-Host "Master Survey Generation Finished Successfully!"
