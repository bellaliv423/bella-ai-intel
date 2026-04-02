@echo off
echo ============================================
echo   Leader Profiles 6x PNG Export
echo ============================================
echo.

cd /d D:\bella-ai-intel\wallpapers

echo [1/1] 6 Leaders banner (1920x320)...
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':320}); pg.goto('file:///D:/bella-ai-intel/wallpapers/profiles/leader_profiles.html'); pg.wait_for_timeout(3000); pg.screenshot(path='profiles/leaders_banner.png'); b.close(); p.stop(); print('[OK] Leaders banner done!')"

echo.
echo [Copy] To bella-nest gallery...
copy /Y "profiles\leaders_banner.png" "D:\bella-nest\public\gallery\leaders_banner.png"

echo.
echo ============================================
echo   Done! Check: profiles\leaders_banner.png
echo   -> Also copied to bella-nest gallery!
echo ============================================
pause
