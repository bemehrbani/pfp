# scripts/audit_markdown_links.ps1
$filePath = "E:\Papers\PFPJ\Campaigns\minab\legal_benchmarks\COMPREHENSIVE_BENCHMARKING_ALL_19_CASES.md"
$text = Get-Content -Path $filePath -Raw -Encoding utf8

$regex = '\[([^\]]+)\]\(([^)]+)\)'
$matches = [regex]::Matches($text, $regex)

Write-Host "Total Markdown Links Found: $($matches.Count)"

$invalidUrls = @()
$emptyAnchors = @()

for ($i = 0; $i -lt $matches.Count; $i++) {
    $m = $matches[$i]
    $anchor = $m.Groups[1].Value
    $url = $m.Groups[2].Value.Trim()
    
    if ([string]::IsNullOrWhiteSpace($anchor)) {
        $emptyAnchors += "Link ${i}: Empty anchor, URL: $url"
    }
    if ($url -notmatch '^https?://') {
        $invalidUrls += "Link ${i}: URL does not start with http(s): '$url' (Anchor: '$anchor')"
    }
    if ($url -match '[<>"\{\}\|\\^`]') {
        $invalidUrls += "Link ${i}: URL contains invalid character: '$url' (Anchor: '$anchor')"
    }
}

Write-Host "Invalid URLs Count: $($invalidUrls.Count)"
foreach ($inv in $invalidUrls) {
    Write-Host "  $inv"
}

Write-Host "Empty Anchors Count: $($emptyAnchors.Count)"
foreach ($ea in $emptyAnchors) {
    Write-Host "  $ea"
}

Write-Host "Sample first 15 links:"
for ($i = 0; $i -lt [Math]::Min(15, $matches.Count); $i++) {
    Write-Host "  [$i] $($matches[$i].Groups[1].Value) -> $($matches[$i].Groups[2].Value)"
}
