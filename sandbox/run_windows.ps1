param(
    [string]$Image = "mercury-sandbox:latest",
    [string]$Plugin = "incident_reporter",
    [string]$Phases = "run"
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path.Replace("\", "/")
$command = "run $Plugin $Phases"

Write-Host "Running plugin '$Plugin' in Docker isolation"
docker run --rm `
    --network none `
    --read-only `
    --tmpfs /tmp:rw,noexec,nosuid,size=64m `
    -e MERCURY_SAFE=1 `
    -e PYTHONDONTWRITEBYTECODE=1 `
    -v "${repoRoot}:/app:ro" `
    -w /app `
    $Image `
    python run.py -c $command
