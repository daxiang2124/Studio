@echo off
set outPath=%cd%

set vAndroidstudio=%outPath%\androidstudio\out
set vAabtool=%outPath%\build_aab_tool-master\out
set vEclipse=%outPath%\eclipse\out
set vGames=%outPath%\games\out
set vKey=%outPath%\key\out
set vProguard=%outPath%\proguard\out
set vPenerator=%outPath%\resource_enerator\out
set vScatter=%outPath%\scatter\out
set vZipDis=%outPath%\zip_disassembly\out


call:deleteDirectory %vAndroidstudio%
call:deleteDirectory %vAabtool%
call:deleteDirectory %vEclipse%
call:deleteDirectory %vGames%
call:deleteDirectory %vKey%
call:deleteDirectory %vProguard%
call:deleteDirectory %vPenerator%
call:deleteDirectory %vScatter%
call:deleteDirectory %vZipDis%


pause
exit


:deleteDirectory
	echo deleteDirectory------------------------------------------
	set dirPath=%1
	echo. dirPath=%dirPath%
	if exist %dirPath% (
		rmdir /s /q %dirPath%
	)
	goto:eof