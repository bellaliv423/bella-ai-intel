@echo off
echo ============================================
echo   EP02 Windy's Strategy Session - PNG Export
echo ============================================
echo.

cd /d D:\bella-ai-intel\wallpapers

echo [1/1] Post (1080x1080)...
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1080}); pg.goto('file:///D:/bella-ai-intel/wallpapers/vlog/ep02_windy_strategy_session.html'); pg.wait_for_timeout(3000); pg.screenshot(path='vlog/ep02_post_1080x1080.png'); b.close(); p.stop(); print('[OK] Post 1080x1080 done!')"

echo.
echo [2/2] Copying to bella-nest gallery...
copy /Y "vlog\ep02_post_1080x1080.png" "D:\bella-nest\public\gallery\ep02_post_1080x1080.png"

echo.
echo ============================================
echo   Done! PNG: D:\bella-nest\public\gallery\ep02_post_1080x1080.png
echo ============================================
pause
