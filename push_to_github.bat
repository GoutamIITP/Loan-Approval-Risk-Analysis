@echo off
REM Quick GitHub Push Script
REM This helps you push your code to GitHub

echo ==========================================
echo 🚀 Push to GitHub - FinCrime Loan System
echo ==========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

REM Check if git is initialized
git status >nul 2>&1
if errorlevel 1 (
    echo 📦 Initializing Git repository...
    git init
    echo ✅ Git initialized
    echo.
)

REM Show current status
echo 📊 Current Git Status:
echo ==========================================
git status
echo ==========================================
echo.

REM Ask user to continue
echo.
set /p CONTINUE="Do you want to add all files and commit? (Y/N): "
if /i not "%CONTINUE%"=="Y" (
    echo.
    echo ❌ Cancelled by user
    pause
    exit /b 0
)

REM Add all files
echo.
echo 📦 Adding all files...
git add .
echo ✅ Files added
echo.

REM Get commit message
echo.
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Initial commit: Complete FinCrime Loan Risk Assessment System
)

REM Commit
echo.
echo 💾 Committing changes...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo.
    echo ⚠️  Nothing to commit or commit failed
    echo.
    pause
    exit /b 1
)
echo ✅ Changes committed
echo.

REM Check if remote exists
git remote -v | findstr origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo 🔗 No remote repository configured
    echo.
    echo Please enter your GitHub repository URL:
    echo Example: https://github.com/YOUR_USERNAME/fincrime-loan-risk-system.git
    echo.
    set /p REPO_URL="Repository URL: "
    
    if "%REPO_URL%"=="" (
        echo.
        echo ❌ No URL provided
        echo.
        echo To add remote manually, use:
        echo git remote add origin YOUR_REPO_URL
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo 🔗 Adding remote repository...
    git remote add origin %REPO_URL%
    echo ✅ Remote added
    echo.
)

REM Show remote
echo 🔗 Remote repository:
git remote -v
echo.

REM Ask to push
echo.
set /p PUSH="Ready to push to GitHub? (Y/N): "
if /i not "%PUSH%"=="Y" (
    echo.
    echo ❌ Push cancelled
    echo.
    echo To push manually later, use:
    echo git push -u origin main
    echo.
    pause
    exit /b 0
)

REM Rename branch to main if needed
echo.
echo 🔄 Ensuring branch is named 'main'...
git branch -M main
echo.

REM Push to GitHub
echo 🚀 Pushing to GitHub...
echo.
echo ⚠️  You may be prompted for GitHub credentials
echo    Use your Personal Access Token as password
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Push failed!
    echo.
    echo Common issues:
    echo 1. Authentication failed - Use Personal Access Token
    echo 2. Repository doesn't exist - Create it on GitHub first
    echo 3. Network issues - Check your internet connection
    echo.
    echo See GITHUB_SETUP.md for detailed help
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ Successfully pushed to GitHub!
echo ==========================================
echo.
echo 🎉 Your code is now on GitHub!
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Add topics and description
echo 3. Share with others!
echo.
pause
