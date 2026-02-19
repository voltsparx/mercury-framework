param(
    [string]$Image = "mercury-sandbox:latest"
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$dockerfile = Join-Path $PSScriptRoot "Dockerfile"

Write-Host "Building Docker image $Image from $dockerfile"
docker build -f $dockerfile -t $Image $repoRoot
