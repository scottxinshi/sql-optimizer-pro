@echo off
echo ========================================
echo SQL Optimizer Pro - Railway Deployment
echo ========================================
echo.

echo Step 1: Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed or not in PATH.
    echo Please restart your terminal after installing Git.
    echo Or follow the manual deployment guide in DEPLOY_NOW.md
    pause
    exit /b 1
)

echo Git is installed. Proceeding with deployment...
echo.

echo Step 2: Initializing Git repository...
git init
git add .
git commit -m "Initial commit - SQL Optimizer Pro by Scott Xin Shi"
echo.

echo Step 3: Git repository ready!
echo.
echo Next steps:
echo 1. Create a GitHub repository at https://github.com
echo 2. Name it: sql-optimizer-pro
echo 3. Run these commands:
echo    git branch -M main
echo    git remote add origin https://github.com/YOUR_USERNAME/sql-optimizer-pro.git
echo    git push -u origin main
echo 4. Go to https://railway.app and deploy from GitHub
echo.
echo For detailed instructions, see DEPLOY_NOW.md
echo.
pause 