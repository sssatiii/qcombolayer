# QcomboLayer Development Sync Script
# PowerShell version for better cross-platform support

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   QcomboLayer Development Sync" -ForegroundColor Cyan  
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$sourcePath = "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
$destPath = "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\QcomboLayer"

Write-Host "Source: $sourcePath" -ForegroundColor Yellow
Write-Host "Destination: $destPath" -ForegroundColor Yellow
Write-Host ""

try {
    # Check if source exists
    if (-not (Test-Path $sourcePath)) {
        throw "Source directory not found: $sourcePath"
    }

    # Create destination directory if it doesn't exist
    if (-not (Test-Path $destPath)) {
        New-Item -ItemType Directory -Path $destPath -Force | Out-Null
        Write-Host "✅ Created destination directory" -ForegroundColor Green
    }

    # Sync files (excluding cache and version control files)
    Write-Host "🔄 Syncing files..." -ForegroundColor Blue
    
    # Get all files from source (excluding unwanted files)
    $excludePatterns = @("*.pyc", "*.pyo", "__pycache__", ".git", ".gitignore", "*.zip", "*.log")
    $sourceFiles = Get-ChildItem -Path $sourcePath -Recurse -File | Where-Object {
        $file = $_
        -not ($excludePatterns | Where-Object { $file.Name -like $_ })
    }

    foreach ($file in $sourceFiles) {
        $relativePath = $file.FullName.Substring($sourcePath.Length + 1)
        $destFile = Join-Path $destPath $relativePath
        $destDir = Split-Path $destFile -Parent

        # Create directory if it doesn't exist
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }

        # Copy file if it's newer or doesn't exist
        if (-not (Test-Path $destFile) -or $file.LastWriteTime -gt (Get-Item $destFile).LastWriteTime) {
            Copy-Item $file.FullName $destFile -Force
            Write-Host "  📄 Updated: $relativePath" -ForegroundColor Gray
        }
    }

    # Clean up deleted files
    if (Test-Path $destPath) {
        $destFiles = Get-ChildItem -Path $destPath -Recurse -File
        foreach ($destFile in $destFiles) {
            $relativePath = $destFile.FullName.Substring($destPath.Length + 1)
            $sourceFile = Join-Path $sourcePath $relativePath
            
            if (-not (Test-Path $sourceFile)) {
                Remove-Item $destFile.FullName -Force
                Write-Host "  🗑️  Removed: $relativePath" -ForegroundColor Red
            }
        }
    }

    Write-Host ""
    Write-Host "✅ Sync completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Open QGIS" -ForegroundColor White
    Write-Host "2. Install 'Plugin Reloader' if not installed yet" -ForegroundColor White
    Write-Host "3. Press F5 or use Plugin Reloader to reload QcomboLayer" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "❌ Sync failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
