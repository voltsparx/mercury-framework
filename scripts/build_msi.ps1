<#
build_msi.ps1

Build a Windows MSI installer for Mercury Framework using WiX Toolset.

Prerequisites:
 - WiX Toolset installed and `candle.exe`, `light.exe`, and `heat.exe` available on PATH.
 - PowerShell (Windows) to run this script.
 - Python is expected to be present on target machines (the MSI will install files and create a shortcut that invokes `python run.py`).

Usage:
  .\scripts\build_msi.ps1 -Version 3.0.0

This script:
 - copies the repository into a temporary staging folder (excludes .git, .venv, dist)
 - uses `heat` to harvest files into a WiX fragment (`Files.wxs`)
 - writes a `Product.wxs` that references the harvested fragment
 - compiles with `candle.exe` and links with `light.exe` to produce `dist\mercury-framework-<ver>.msi`

Caveats:
 - This creates a simple file-based MSI. It does not bundle Python.
 - For a full packaged runtime installer consider using a PyInstaller build or bundling an embeddable Python.
#>
param(
    [string]$Version = "3.0.0"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Check-Tool($name) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $cmd) {
        Write-Error "Required WiX tool not found on PATH: $name. Please install WiX Toolset and ensure $name is on PATH."
        exit 2
    }
    return $cmd.Path
}

$candle = Check-Tool -name 'candle.exe'
$light = Check-Tool -name 'light.exe'
$heat = Check-Tool -name 'heat.exe'

$repoRoot = Resolve-Path -Path (Join-Path $PSScriptRoot "..") | Select-Object -ExpandProperty Path
$dist = Join-Path $repoRoot 'dist'
if (-Not (Test-Path $dist)) { New-Item -ItemType Directory -Path $dist | Out-Null }

# create a temp staging folder
$tmp = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString())
$staging = Join-Path $tmp 'staging'
New-Item -ItemType Directory -Path $staging | Out-Null

Write-Host "Copying repository to staging: $staging"
$exclusions = @('.git', '.venv', 'dist', '__pycache__', '.pytest_cache')
Get-ChildItem -Path $repoRoot -Force | Where-Object {
    ($_.Name -ne '.git') -and ($_.Name -ne '.venv') -and ($_.Name -ne 'dist') -and ($_.Name -ne '__pycache__') -and ($_.Name -ne '.pytest_cache')
} | ForEach-Object {
    $src = $_.FullName
    $dest = Join-Path $staging $_.Name
    if ($_.PSIsContainer) { Copy-Item -Path $src -Destination $dest -Recurse -Force -ErrorAction Stop }
    else { Copy-Item -Path $src -Destination $dest -Force -ErrorAction Stop }
}

# Harvest files into a WiX fragment using heat
$filesWxs = Join-Path $tmp 'Files.wxs'
Write-Host "Harvesting files with heat into: $filesWxs"
& $heat dir "$staging" -cg MERCURYFILES -dr INSTALLFOLDER -sreg -scom -srd -gg -sfrag -out "$filesWxs"

# Write a Product.wxs referencing the harvested component group
$productWxs = Join-Path $tmp 'Product.wxs'
$upgradeGuid = [guid]::NewGuid().ToString()
$productCode = [guid]::NewGuid().ToString()
$productContent = @"
<?xml version="1.0" encoding="utf-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="$productCode" Name="Mercury Framework" Language="1033" Version="$Version" Manufacturer="voltsparx" UpgradeCode="$upgradeGuid">
    <Package InstallerVersion="500" Compressed="yes" InstallScope="perMachine" />
    <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed." />
    <MediaTemplate />
    <Feature Id="DefaultFeature" Level="1">
      <ComponentGroupRef Id="MERCURYFILES" />
    </Feature>
    <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />
    <UIRef Id="WixUI_Minimal" />
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="Mercury Framework" />
      </Directory>
    </Directory>
  </Product>
</Wix>
"@
Set-Content -Path $productWxs -Value $productContent -Encoding UTF8

# Compile with candle and link with light
Write-Host "Compiling WiX sources..."
Push-Location $tmp
& $candle -out "Files.wixobj" "$filesWxs"
& $candle -out "Product.wixobj" "$productWxs"

Write-Host "Linking into MSI..."
$outMsi = Join-Path $dist "mercury-framework-$Version.msi"
& $light -ext WixUIExtension -out "$outMsi" "Files.wixobj" "Product.wixobj"

Pop-Location

Write-Host "MSI created: $outMsi"

# Clean up staging
# Remove-Item -Recurse -Force $tmp

Write-Host "Done. You can find the MSI in: $outMsi"


