<#
build_windows_installer.ps1

Create a Windows installer artifact for Mercury Framework.

This script creates a distributable ZIP in `dist/` and also generates a
simple `install.ps1` helper that extracts the archive to
`$Env:ProgramFiles\MercuryFramework` and creates a Start Menu shortcut.

Requirements: PowerShell (Windows). 7-Zip optional — if present, this script
can optionally use `7z.exe` to create a self-extracting archive.

Usage: .\scripts\build_windows_installer.ps1 -Version 0.3.0
#>
param(
    [string]$Version = "0.3.0",
    [switch]$Use7Zip
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path -Path (Join-Path $PSScriptRoot "..")
$repoRoot = $repoRoot.Path
$dist = Join-Path $repoRoot "dist"
if (-Not (Test-Path $dist)) { New-Item -ItemType Directory -Path $dist | Out-Null }

$pkgName = "mercury-framework"
$outZip = Join-Path $dist "$($pkgName)-$($Version)-win.zip"

Write-Host "Creating distributable ZIP: $outZip"

# Build list of files to include (exclude common VCS and env folders)
$exclusions = @('.git', '.venv', 'dist', '__pycache__', '.pytest_cache')
$files = Get-ChildItem -Path $repoRoot -Recurse -File | Where-Object {
    $rel = $_.FullName.Substring($repoRoot.Length + 1)
    $skip = $false
    foreach ($e in $exclusions) { if ($rel -like "$e*" -or $rel -like "*$([System.IO.Path]::DirectorySeparatorChar)$e*") { $skip = $true; break } }
    -not $skip
}

# Compress-Archive requires paths; write to temp file list
$tmpList = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString() + '.txt')
$files | ForEach-Object { $_.FullName } | Out-File -FilePath $tmpList -Encoding utf8

if (Test-Path $outZip) { Remove-Item $outZip -Force }
Compress-Archive -LiteralPath (Get-Content $tmpList) -DestinationPath $outZip -Force
Remove-Item $tmpList -Force

# Generate a simple install helper that extracts and creates Start Menu shortcut
$installHelper = @'
param(
    [string]$TargetDir = "$env:ProgramFiles\MercuryFramework",
    [string]$ZipPath = "PLACEHOLDER_ZIP_PATH"
)

if (-Not (Test-Path $ZipPath)) { Write-Error "Archive not found: $ZipPath"; exit 2 }

# Ensure target dir
if (-Not (Test-Path $TargetDir)) { New-Item -ItemType Directory -Path $TargetDir | Out-Null }

Write-Host "Extracting $ZipPath to $TargetDir"
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $TargetDir)

# Create Start Menu shortcut
$WshShell = New-Object -ComObject WScript.Shell
$startMenu = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\Mercury Framework"
if (-Not (Test-Path $startMenu)) { New-Item -ItemType Directory -Path $startMenu | Out-Null }
$lnk = $WshShell.CreateShortcut((Join-Path $startMenu "Mercury Framework.lnk"))
$lnk.TargetPath = (Join-Path $TargetDir "run.py")
$lnk.Arguments = ""
$lnk.WorkingDirectory = $TargetDir
$lnk.Description = "Mercury Framework (safe educational scaffold)"
$lnk.Save()

Write-Host "Installed to $TargetDir. Start Menu shortcut created."
'@

$installHelper = $installHelper -replace 'PLACEHOLDER_ZIP_PATH', ($outZip -replace '\\','\\\\')
$installPath = Join-Path $dist 'install.ps1'
Set-Content -Path $installPath -Value $installHelper -Encoding UTF8

Write-Host "Wrote installer helper: $installPath"

# If requested and if 7z is on PATH, create a self-extracting archive (SFX)
if ($Use7Zip) {
    $seven = Get-Command 7z -ErrorAction SilentlyContinue
    if ($seven) {
        $sfxPath = Join-Path $dist "$($pkgName)-$($Version)-installer.exe"
        Write-Host "7z found. Creating SFX installer: $sfxPath"
        # Create temporary 7z archive and then convert to SFX using 7z's SFX module
        $tmp7z = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString() + '.7z')
        & $seven.Source a -r $tmp7z "$repoRoot\*" -xr!*.git -xr!*.venv -xr!dist -xr!__pycache__ -xr!.pytest_cache | Out-Null
        # If default 7z.sfx present, we can concatenate: 7z.sfx + config + archive -> sfx.exe
        $sfxModule = "$env:ProgramFiles\7-Zip\7z.sfx"
        if (-Not (Test-Path $sfxModule)) { $sfxModule = "C:\Program Files\7-Zip\7z.sfx" }
        if (Test-Path $sfxModule) {
            $config = """ ;!@Install@!UTF-8!\nTitle=Mercury Framework Installer\nRunProgram=install.ps1\n;!@InstallEnd@!\n"""
            $cfgPath = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString() + '.txt')
            Set-Content -Path $cfgPath -Value $config -Encoding ASCII
            # build final exe
            Get-Content $sfxModule, $cfgPath, $tmp7z -Encoding Byte -ReadCount 0 | Set-Content -Path $sfxPath -Encoding Byte
            Remove-Item $cfgPath, $tmp7z -Force
            Write-Host "Created SFX installer: $sfxPath"
        } else {
            Write-Warning "7z.sfx module not found; SFX creation skipped."
            Remove-Item $tmp7z -Force
        }
    } else {
        Write-Warning "7z not found on PATH; skipping SFX creation."
    }
}

Write-Host "Windows installer artifacts created in: $dist"

