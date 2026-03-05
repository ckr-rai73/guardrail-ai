# setup_env.ps1

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$sdksDir = Join-Path $workspace ".sdks"

if (-not (Test-Path $sdksDir)) {
    New-Item -ItemType Directory -Force -Path $sdksDir | Out-Null
}

Write-Host "Creating local .sdks directory at $sdksDir" -ForegroundColor Cyan

# --- 1. JDK Setup ---
$jdkUrl = "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/17.0.12+7/openlogic-openjdk-17.0.12+7-windows-x64.zip"
$jdkZip = Join-Path $sdksDir "jdk.zip"
$jdkExtractDir = Join-Path $sdksDir "jdk-extracted"
$jdkDir = Join-Path $sdksDir "jdk"

if (-not (Test-Path $jdkDir)) {
    Write-Host "Downloading OpenJDK 17..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $jdkUrl -OutFile $jdkZip
    
    Write-Host "Extracting OpenJDK 17..." -ForegroundColor Yellow
    Expand-Archive -Path $jdkZip -DestinationPath $jdkExtractDir -Force
    
    # Move the inner folder (e.g., openlogic-openjdk-17.0.12+7-windows-x64) to 'jdk'
    $innerJdkDir = Get-ChildItem -Path $jdkExtractDir -Directory | Select-Object -First 1
    Move-Item -Path $innerJdkDir.FullName -Destination $jdkDir -Force
    
    # Cleanup
    Remove-Item -Path $jdkZip -Force
    Remove-Item -Path $jdkExtractDir -Force -Recurse
    Write-Host "JDK 17 installed." -ForegroundColor Green
} else {
    Write-Host "JDK 17 already exists at $jdkDir" -ForegroundColor Green
}

# --- 2. Android SDK Setup ---
$androidCmdlineToolsUrl = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
$androidZip = Join-Path $sdksDir "cmdline-tools.zip"

$androidSdkRoot = Join-Path $sdksDir "android-sdk"
$cmdlineToolsTarget = Join-Path $androidSdkRoot "cmdline-tools\latest"

if (-not (Test-Path $cmdlineToolsTarget)) {
    Write-Host "Downloading Android SDK Command-line Tools..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $androidCmdlineToolsUrl -OutFile $androidZip
    
    Write-Host "Extracting Android SDK Command-line Tools..." -ForegroundColor Yellow
    $tempExtractDir = Join-Path $sdksDir "temp_cmdline"
    Expand-Archive -Path $androidZip -DestinationPath $tempExtractDir -Force
    
    # Move extracted contents to cmdline-tools/latest
    New-Item -ItemType Directory -Force -Path $cmdlineToolsTarget | Out-Null
    Copy-Item -Path (Join-Path $tempExtractDir "cmdline-tools\*") -Destination $cmdlineToolsTarget -Recurse -Force
    
    # Cleanup
    Remove-Item -Path $androidZip -Force
    Remove-Item -Path $tempExtractDir -Force -Recurse
    Write-Host "Android Command-line Tools installed." -ForegroundColor Green
} else {
     Write-Host "Android Command-line Tools already exist." -ForegroundColor Green
}

# Use the temporarily installed java to run sdkmanager
$env:JAVA_HOME = $jdkDir
$javaBin = Join-Path $jdkDir "bin"
$env:PATH = "$javaBin;$($env:PATH)"

$sdkmanager = Join-Path $cmdlineToolsTarget "bin\sdkmanager.bat"

Write-Host "Accepting Android licenses..." -ForegroundColor Yellow
# Run yes and pipe to sdkmanager
cmd.exe /c "echo y| $sdkmanager --licenses"

Write-Host "Installing Android platforms and build-tools..." -ForegroundColor Yellow
& $sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# --- 3. Flutter Setup ---
$flutterUrl = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.24.0-stable.zip"
$flutterZip = Join-Path $sdksDir "flutter.zip"
$flutterDir = Join-Path $sdksDir "flutter"

if (-not (Test-Path $flutterDir)) {
    Write-Host "Downloading Flutter SDK..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $flutterUrl -OutFile $flutterZip
    
    Write-Host "Extracting Flutter SDK..." -ForegroundColor Yellow
    Expand-Archive -Path $flutterZip -DestinationPath $sdksDir -Force
    
    # Cleanup
    Remove-Item -Path $flutterZip -Force
    Write-Host "Flutter SDK installed." -ForegroundColor Green
} else {
    Write-Host "Flutter SDK already exists." -ForegroundColor Green
}

# --- 4. Configure Environment Temporarily for Setup Verification ---
$flutterBin = Join-Path $flutterDir "bin"
$env:PATH = "$flutterBin;$($env:PATH)"

# Configure Flutter to point to our custom Android SDK
Write-Host "Configuring Flutter to use the local Android SDK..." -ForegroundColor Yellow
flutter config --android-sdk $androidSdkRoot
flutter config --no-analytics

Write-Host "Running flutter doctor..." -ForegroundColor Yellow
flutter doctor

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To use these tools in a new terminal, run: '. .\activate.ps1'" -ForegroundColor Cyan
