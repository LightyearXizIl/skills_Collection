param(
    [Parameter(Mandatory = $true)]
    [string]$Destination
)

$ErrorActionPreference = 'Stop'
$skillRoot = Split-Path -Parent $PSScriptRoot
$templateRoot = Join-Path $skillRoot 'assets\template'
$resolvedDestination = [System.IO.Path]::GetFullPath($Destination)

if (-not (Test-Path -LiteralPath $templateRoot -PathType Container)) {
    throw "Template directory is missing: $templateRoot"
}

if (Test-Path -LiteralPath $resolvedDestination) {
    $existingItems = @(Get-ChildItem -LiteralPath $resolvedDestination -Force)
    if ($existingItems.Count -gt 0) {
        throw "Destination is not empty; refusing to overwrite: $resolvedDestination"
    }
} else {
    New-Item -ItemType Directory -Path $resolvedDestination | Out-Null
}

Copy-Item -Path (Join-Path $templateRoot '*') -Destination $resolvedDestination -Recurse -Force
Write-Output "Created Remotion Vox project at: $resolvedDestination"
Write-Output 'Next: npm install, npm run typecheck, npm run studio'
