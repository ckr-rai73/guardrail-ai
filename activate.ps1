# activate.ps1

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$sdksDir = Join-Path $workspace ".sdks"

$jdkDir = Join-Path $sdksDir "jdk"
$androidSdkRoot = Join-Path $sdksDir "android-sdk"
$flutterDir = Join-Path $sdksDir "flutter"

if (-not (Test-Path $sdksDir)) {
    Write-Error "SDKs directory not found at $sdksDir. Please run .\setup_env.ps1 first."
    return
}

# Set Environment Variables
$env:JAVA_HOME = $jdkDir
$env:ANDROID_HOME = $androidSdkRoot

# Build Paths to prepend
$javaBin = Join-Path $jdkDir "bin"
$androidPlatformTools = Join-Path $androidSdkRoot "platform-tools"
$androidCmdlineTools = Join-Path $androidSdkRoot "cmdline-tools\latest\bin"
$flutterBin = Join-Path $flutterDir "bin"
$mingitCmd = Join-Path $flutterDir "bin\mingit\cmd"

# Prepend to PATH 
$env:PATH = "$flutterBin;$mingitCmd;$javaBin;$androidPlatformTools;$androidCmdlineTools;$($env:PATH)"

Write-Host "Development Environment Activated!" -ForegroundColor Cyan
Write-Host "  JAVA_HOME:    $env:JAVA_HOME" -ForegroundColor Green
Write-Host "  ANDROID_HOME: $env:ANDROID_HOME" -ForegroundColor Green
Write-Host "  Flutter Bin:  $flutterBin" -ForegroundColor Green
Write-Host "  Git Bin:      $mingitCmd" -ForegroundColor Green

Write-Host ""
Write-Host "Checking versions:" -ForegroundColor Yellow
java -version
flutter --version
