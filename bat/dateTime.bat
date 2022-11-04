@echo off


echo ---------------date-----------------
echo date=%date%
echo date04=%date:~0,4%
echo date52=%date:~5,2%
echo date82=%date:~8,2%

echo %date% /t

echo ---------------time-----------------
echo time=%time%
echo time02=%time:~0,2%
echo time32=%time:~3,2%
echo time68=%time:~6,2%
echo time82=%time:~9,2%

echo ---------------folder-----------------
set folder=%date:~0,4%-%date:~5,2%-%date:~8,2%-%time:~0,2%%time:~3,2%-%time:~6,2%%time:~9,2%
echo folder=%folder%






pause