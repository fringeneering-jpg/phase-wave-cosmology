# --- CONFIGURATION (Edit these before pasting) ---
$Folder = "C:\Users\jaden\Downloads\PWC-Check\PWC\scriptss
$Output = "C:\Users\jaden\Downloads\PWC-Check\PWC\scripts"
$Search = $false                     # <--- Set to $true to open Google Scholar tabs, $false to skip
$Ocr    = $false                     # <--- Set to $true if you have ocrmypdf installed and want OCR

# --- SCRIPT EXECUTION (Copy and paste everything below directly into PowerShell) ---
$ErrorActionPreference = "Stop"

$SEARCHES = @(
    'Folkner 1997 Pathfinder ephemeris range residuals Viking',
    'Jacobson 2006 Saturn DE405 range residuals ephemeris',
    '"Use of MESSENGER radioscience data" range bias',
    '"Standish" "DE410" "2003" filetype:pdf',
    '"499.00478368061" "499.004783826"',
    '"ephemeris" "systematic errors of unknown origin"'
)

$PATTERNS = [ordered]@{
    "pre_fit"              = "\bpre[\s-]?fit\b"
    "post_fit"             = "\bpost[\s-]?fit\b"
    "range_bias"           = "\brang(?:e|ing)\s+bias(?:es)?\b"
    "bias"                 = "\bbias(?:es|ed)?\b"
    "residual"             = "\bresiduals?\b"
    "previous_values"      = "\b(?:previous|former|old)\s+values?\b"
    "parameter_adjustment" = "\b(?:adjust(?:ed|ment|ments)?|estimated|fitted|re[\s-]?determined|corrections?)\b"
    "systematics"          = "\bsystematic\s+errors?\b|\bunknown\s+origin\b"
    "AU_scale"             = "499[.,]004783|astronomical\s+unit|\btau\s*[_-]?\s*A\b|\u03C4\s*[_-]?\s*A"
    "mass_GM"              = "\bGM\b|\bgravitational\s+parameters?\b|\bplanet(?:ary)?\s+masses\b|\bmass\s+ratios?\b"
    "ephemeris_version"    = "\bDE[\s-]?(?:200|403|405|410|421|430|431)\b"
}

$COMPILED = @{}
foreach ($key in $PATTERNS.Keys) {
    $COMPILED[$key] = [regex]::new($PATTERNS[$key], [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
}

function Extract-Pages ([string]$PdfPath) {
    if (Get-Command "pdftotext" -ErrorAction SilentlyContinue) {
        $rawBytes = & pdftotext -enc UTF-8 $PdfPath - 2>$null
        $rawText = [string]::Join("`n", $rawBytes)
        $pages = $rawText -split "`f"
        if ($pages.Count -gt 1 -and [string]::IsNullOrEmpty($pages[-1])) {
            $pages = $pages[0..($pages.Count - 2)]
        }
        return ,$pages
    } elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
        $pyCode = "import sys, json; from pypdf import PdfReader; r = PdfReader(sys.argv[1]); print(json.dumps([p.extract_text() or '' for p in r.pages]))"
        $json = & python -c $pyCode $PdfPath
        if ($LASTEXITCODE -ne 0) {
            throw "Python pypdf extraction failed for '$PdfPath'."
        }
        $pages = $json | ConvertFrom-Json
        return ,([string[]]$pages)
    } else {
        throw "Neither 'pdftotext' nor 'python' (with pypdf) was found in PATH to extract PDF text."
    }
}

function Get-SearchablePages ([System.IO.FileInfo]$Pdf, [string]$OutputDir, [bool]$UseOcr) {
    $pages = Extract-Pages -PdfPath $Pdf.FullName
    $sparse = $false
    foreach ($text in $pages) {
        $cleaned = $text -replace "\s+", ""
        if ($cleaned.Length -lt 80) {
            $sparse = $true
            break
        }
    }
    if (-not $UseOcr -or -not $sparse) {
        return [PSCustomObject]@{
            Pages        = $pages
            ProcessedPdf = $Pdf.FullName
        }
    }
    $ocrDir = Join-Path $OutputDir "ocr"
    if (-not (Test-Path $ocrDir)) {
        New-Item -ItemType Directory -Path $ocrDir -Force | Out-Null
    }
    $destination = Join-Path $ocrDir $Pdf.Name
    & ocrmypdf --skip-text --rotate-pages --deskew $Pdf.FullName $destination
    if ($LASTEXITCODE -ne 0) {
        throw "ocrmypdf failed with exit code $LASTEXITCODE"
    }
    $ocrPages = Extract-Pages -PdfPath $destination
    return [PSCustomObject]@{
        Pages        = $ocrPages
        ProcessedPdf = $destination
    }
}

function Find-Passages ([string]$Text, [int]$Radius = 550) {
    if ([string]::IsNullOrEmpty($Text)) { return @() }
    $matchesList = [System.Collections.Generic.List[PSCustomObject]]::new()
    foreach ($label in $COMPILED.Keys) {
        $regex = $COMPILED[$label]
        $regMatches = $regex.Matches($Text)
        foreach ($m in $regMatches) {
            $start = [Math]::Max(0, $m.Index - $Radius)
            $end = [Math]::Min($Text.Length, $m.Index + $m.Length + $Radius)
            $matchesList.Add([PSCustomObject]@{
                Start = $start
                End   = $end
                Label = $label
            })
        }
    }
    if ($matchesList.Count -eq 0) { return @() }
    $sorted = $matchesList | Sort-Object Start, End
    $merged = [System.Collections.Generic.List[PSCustomObject]]::new()
    foreach ($item in $sorted) {
        if ($merged.Count -gt 0 -and $item.Start -le $merged[$merged.Count - 1].End) {
            $last = $merged[$merged.Count - 1]
            $last.End = [Math]::Max($last.End, $item.End)
            [void]$last.Labels.Add($item.Label)
        } else {
            $labelSet = [System.Collections.Generic.HashSet[string]]::new()
            [void]$labelSet.Add($item.Label)
            $merged.Add([PSCustomObject]@{
                Start  = $item.Start
                End    = $item.End
                Labels = $labelSet
            })
        }
    }
    $results = foreach ($m in $merged) {
        $sortedLabels = ($m.Labels | Sort-Object) -join "; "
        $passageLength = $m.End - $m.Start
        $passage = $Text.Substring($m.Start, $passageLength)
        [PSCustomObject]@{
            Labels  = $sortedLabels
            Passage = $passage
        }
    }
    return ,$results
}

if (-not (Test-Path $Output)) {
    New-Item -ItemType Directory -Path $Output -Force | Out-Null
}
$OutputResolved = (Resolve-Path $Output).Path

$searchesFile = Join-Path $OutputResolved "searches.txt"
$searchLines = [System.Collections.Generic.List[string]]::new()
foreach ($query in $SEARCHES) {
    $encoded = [System.Uri]::EscapeDataString($query)
    $link = "https://scholar.google.com/scholar?q=$encoded"
    $searchLines.Add("$query`n$link`n")
    if ($Search) {
        Start-Process $link
    }
}
[System.IO.File]::WriteAllLines($searchesFile, $searchLines, [System.Text.UTF8Encoding]::new($false))

$rows = [System.Collections.Generic.List[PSCustomObject]]::new()
$errors = [System.Collections.Generic.List[string]]::new()

if (Test-Path $Folder) {
    $pdfFiles = Get-ChildItem -Path $Folder -Filter "*.pdf" | Sort-Object Name
} else {
    Write-Warning "Folder '$Folder' does not exist. Skipping PDF scan."
    $pdfFiles = @()
}

foreach ($pdf in $pdfFiles) {
    try {
        $res = Get-SearchablePages -Pdf $pdf -OutputDir $OutputResolved -UseOcr $Ocr
        $pages = $res.Pages
        $processed = $res.ProcessedPdf
        $textFile = Join-Path $OutputResolved "$($pdf.BaseName).txt"
        $textBuilder = [System.Text.StringBuilder]::new()
        for ($i = 0; $i -lt $pages.Count; $i++) {
            $pageNumber = $i + 1
            $pageText = [string]$pages[$i]
            [void]$textBuilder.Append("`n===== PDF PAGE $pageNumber =====`n$pageText`n")
            $passages = Find-Passages -Text $pageText
            foreach ($p in $passages) {
                $rows.Add([PSCustomObject][ordered]@{
                    source_pdf                  = $pdf.Name
                    processed_pdf               = $processed
                    pdf_page                    = $pageNumber
                    matched_topics              = $p.Labels
                    passage                     = $p.Passage
                    observable                  = ""
                    units                       = ""
                    old_ephemeris               = ""
                    new_ephemeris               = ""
                    old_value                   = ""
                    new_value                   = ""
                    uncertainty                 = ""
                    data_span                   = ""
                    fit_status                  = ""
                    author_explanation          = ""
                    verified_against_page_image = ""
                })
            }
        }
        [System.IO.File]::WriteAllText($textFile, $textBuilder.ToString(), [System.Text.UTF8Encoding]::new($false))
    } catch {
        $errors.Add("$($pdf.Name): $($_.Exception.Message)")
    }
}

$csvPath = Join-Path $OutputResolved "passages.csv"
if ($rows.Count -gt 0) {
    $rows | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
} else {
    $header = '"source_pdf","processed_pdf","pdf_page","matched_topics","passage","observable","units","old_ephemeris","new_ephemeris","old_value","new_value","uncertainty","data_span","fit_status","author_explanation","verified_against_page_image"'
    [System.IO.File]::WriteAllText($csvPath, "$header`r`n", [System.Text.UTF8Encoding]::new($false))
}

$errorsPath = Join-Path $OutputResolved "errors.txt"
[System.IO.File]::WriteAllText($errorsPath, ($errors -join "`n"), [System.Text.UTF8Encoding]::new($false))

Write-Host "Extracted $($rows.Count) candidate passages."
Write-Host "Output: $OutputResolved"
if ($errors.Count -gt 0) {
    Write-Host "$($errors.Count) files failed; see errors.txt."
}