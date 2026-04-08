@echo off
REM ===========================================================
REM MAX Assets Renderer
REM Renders all Max-related PNGs (profile, banner, wallpaper, 3 insta)
REM Total output: 7 PNGs
REM ===========================================================
cd /d "%~dp0"

echo.
echo === MAX Assets Renderer ===
echo Working directory: %CD%
echo.

REM Check Node + Playwright installed
if not exist "node_modules\playwright" (
  echo [!] playwright not installed. Installing...
  call npm install playwright
  call npx playwright install chromium
)

echo Running renderer...
echo.
node render_max_assets.js

echo.
echo ===========================================================
echo DONE. Generated files:
echo.
echo [Profiles]
echo   D:\bella-ai-intel\wallpapers\profiles\profile_max_1080x1080.png
echo   D:\bella-ai-intel\wallpapers\profiles\max.png
echo   D:\bella-ai-intel\wallpapers\profiles\leader_profiles_full.png
echo.
echo [Wallpaper]
echo   D:\bella-ai-intel\wallpapers\dreamteam_pc_1920x1080.png  (v8)
echo.
echo [Instagram]
echo   D:\bella-ai-intel\wallpapers\instagram\insta_profile_4bros_320.png
echo   D:\bella-ai-intel\wallpapers\instagram\insta_post_16_1080.png
echo   D:\bella-ai-intel\wallpapers\instagram\insta_story_max_1080x1920.png
echo ===========================================================
pause
