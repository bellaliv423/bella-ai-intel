@echo off
echo ============================================
echo   EP01 Goldi's Monday Briefing - PNG Export
echo ============================================
echo.

cd /d D:\bella-ai-intel\wallpapers

echo [1/2] Post (1080x1080)...
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1080}); pg.goto('file:///D:/bella-ai-intel/wallpapers/vlog/ep01_goldi_monday_briefing.html'); pg.wait_for_timeout(3000); pg.screenshot(path='vlog/ep01_post_1080x1080.png'); b.close(); p.stop(); print('[OK] Post 1080x1080 done!')"

echo [2/2] Story (1080x1920)...
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto('file:///D:/bella-ai-intel/wallpapers/vlog/ep01_story_1080x1920.html'); pg.wait_for_timeout(3000); pg.screenshot(path='vlog/ep01_story_1080x1920.png'); b.close(); p.stop(); print('[OK] Story 1080x1920 done!')"

echo.
echo [3/3] Copying to bella-nest gallery...
copy /Y "vlog\ep01_post_1080x1080.png" "D:\bella-nest\public\gallery\ep01_post_1080x1080.png"
copy /Y "vlog\ep01_story_1080x1920.png" "D:\bella-nest\public\gallery\ep01_story_1080x1920.png"

echo.
echo ============================================
echo   All done!
echo   PNG: D:\bella-ai-intel\wallpapers\vlog\
echo   Gallery: D:\bella-nest\public\gallery\
echo
echo   Next: gallery.json will auto-update!
echo ============================================
pause
