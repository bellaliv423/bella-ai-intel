@echo off
chcp 65001 >nul
echo [%date% %time%] BELLA AI Intel - Start
cd /d D:\bella-ai-intel

echo [Step 1] Collecting (Release Notes + Reddit)...
python scripts\collector.py --source all

echo [Step 2] Analyzing (Dream Team recommendations)...
python scripts\analyzer.py --no-email

echo [Step 3] Git push...
git add data\latest.json data\recommendations.json data\archive\
git commit -m "Auto-collect + analyze AI intel %date% %time:~0,5%"
git push origin master

echo [%date% %time%] BELLA AI Intel - Done
