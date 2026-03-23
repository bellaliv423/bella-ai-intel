@echo off
cd /d D:\bella-ai-intel
python scripts\collector.py --source all
cd /d D:\bella-ai-intel
git add data\latest.json
git commit -m "Auto-collect AI intel %date% %time:~0,5%"
git push origin master
