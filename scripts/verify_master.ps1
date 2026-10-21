$filePath = 'E:\Papers\PFPJ\Campaigns\minab\justiceForMinab\docs\FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md'
$text = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)

$checks = @(
    "8 nonies",
    "14 ter",
    "16 quater",
    "30 bis",
    "36 bis",
    "38 quater",
    "43 ter",
    "45 ter",
    "47 quater",
    "48 octies",
    "48 sexies bis",
    "50 bis",
    "52 ter",
    "57 quater",
    "61 ter",
    "63 bis",
    "72 ter",
    "76 ter",
    "78 ter",
    "81 septies",
    "84 bis",
    "85 quinquies",
    "85 ter",
    "90 quater",
    "91 ter",
    "10.2 Section 1: State Responsibility",
    "10.3 Section 2: Individual Criminal Responsibility",
    "COUNT 1: WAR CRIME",
    "COUNT 2: WAR CRIME",
    "COUNT 3: WAR CRIME",
    "COUNT 4: WAR CRIME",
    "COUNT 5: WAR CRIME",
    "300,000,000 USD",
    "10.4 Orders Concerning Judicial Preservation",
    "10.5 Contingent Prosecutorial Directions"
)

$allFound = $true
foreach ($chk in $checks) {
    if ($text.Contains($chk)) {
        Write-Output "[PASS] Found: $chk"
    } else {
        Write-Output "[FAIL] Missing: $chk"
        $allFound = $false
    }
}

if ($allFound) {
    Write-Output "=== ALL 35 VERIFICATION CHECKS PASSED PERFECTLY ==="
} else {
    Write-Output "=== SOME CHECKS FAILED ==="
}
