$ErrorActionPreference = "Stop"

$versionLine = Select-String 'version\s*=' pyproject.toml
$VERSION = $versionLine.ToString().Split('"')[1]

$OUT = "lite_dist"
$ZIP = "mercury-framework-lite-$VERSION.zip"

Remove-Item $OUT -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $ZIP -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory $OUT | Out-Null

$include = @(
    "mercury",
    "mercury_plugins",
    "samples",
    "run.py",
    "cli.py",
    "requirements.txt",
    "README.md",
    "LICENSE",
    "RESPONSIBLE_USE.md",
    "PLUGIN_AUTHOR_GUIDE.md"
)

foreach ($item in $include) {
    Copy-Item $item $OUT -Recurse -Force
}

Compress-Archive -Path "$OUT\*" -DestinationPath $ZIP -Force

Write-Host "ZIP created: $ZIP"
