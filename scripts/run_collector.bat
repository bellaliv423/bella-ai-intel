@echo off
echo [%date% %time%] BELLA AI Intel - Start
cd /d D:\bella-ai-intel

echo [Step 1] Collecting...
python scripts\collector.py --source all

echo [Step 2] Analyzing...
python scripts\analyzer.py

echo [Step 3] Git push...
git add data\latest.json data\recommendations.json
git commit -m "Auto-collect + analyze AI intel %date% %time:~0,5%"
git push origin master

echo [%date% %time%] BELLA AI Intel - Done
