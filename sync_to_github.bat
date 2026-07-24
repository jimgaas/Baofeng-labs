@echo off
cd /d C:\Users\erikg\Desktop\Baofeng
git status
pause
git add .
set /p msg=Commit message: 
git commit -m "%msg%"
git push
pause