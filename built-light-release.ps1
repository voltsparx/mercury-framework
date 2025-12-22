$ErrorActionPreference = "Stop"

$ZIP_NAME = "mercury-framework-lite.zip"
$TEMP_DIR = "mercury-lite"

if (Test-Path $TEMP_DIR) { Remove-Item $TEMP_DIR -Recurse -Force }
if (Test-Path $ZIP_NAME) { Remove-Item $ZIP_NAME -Force }

New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null

$INCLUDE = @(
  "mercury",
  "mercury_plugins",
  "run.py",
  "cli.py",
  "sandbox",
  "requirements.txt",
  "README.md",
  "LICENSE",
  "INSTALL.md",
  "RESPONSIBLE_USE.md",
  "PLUGIN_AUTHOR_GUIDE.md",
  "RELEASE.md",
  "RELEASE_NOTES.md"
)

foreach ($item in $INCLUDE) {
  if (Test-Path $item) {
    Copy-Item $item -Destination $TEMP_DIR -Recurse -Force
  }
}

Compress-Archive -Path "$TEMP_DIR\*" -DestinationPath $ZIP_NAME

Remove-Item $TEMP_DIR -Recurse -Force

Write-Host "✔ Lite release created: $ZIP_NAME"
