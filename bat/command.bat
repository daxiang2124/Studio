@echo off

set sType=%1
echo execute batch command=%sType%

if %sType% == cleanDirectory (
	call:cleanDirectory %2
)

if %sType% == createDirectorys (
	call:createDirectorys %2
)

if %sType% == copyDirectoryBaseClient (
	call:copyDirectoryBaseClient %2 %3
)

if %sType% == copyDirectoryBaseClientGame (
	call:copyDirectoryBaseClientGame
)

if %sType% == copyDirectoryGame (
	call:copyDirectoryGame
)

if %sType% == copyTheCompiledGameFile (
	call:copyTheCompiledGameFile %2
)

if %sType% == copyDirectorySpecifiedDirectory (
	call:copyDirectorySpecifiedDirectory %2 %3
)

if %sType% == createMd5File (
	call:createMd5File %2
)

if %sType% == compressedFile (
	call:compressedFile %2 %3
)

if %sType% == compressedFileArgs4 (
	call:compressedFile %2 %3 %4 %5
)

if %sType% == compressedFileBCC (
	call:compressedFileBCC %2 %3 %4 %5
)

if %sType% == deleteDirectory (
	call:deleteDirectory %2
)

if %sType% == copyFile (
	call:copyFile %2 %3
)

if %sType% == copySpecifiedDirectory (
	call:copySpecifiedDirectory %2 %3
)

if %sType% == makefileJksKeystore (
	call:makefileJksKeystore %2 %3 %4 %5 %6 %7
)

if %sType% == copyAndStudioOutApk (
	call:copyAndStudioOutApk %2 %3 %4
)

if %sType% == copyAndStudioCustomerOutApk (
	call:copyAndStudioCustomerOutApk %2 %3 %4
)

if %sType% == deleteFile (
	call:deleteFile %2
)

if %sType% == signApkEclipse (
	call:signApkEclipse %2 %3 %4 %5 %6 %7 %8 %9
)

exit
	
:copyDirectoryBaseClient
	echo copyDirectoryBaseClient------------------------------------------
	set copyPath=%1
	set targetPath=%2
	
	echo. copyPath=%copyPath%
	echo. targetPath=%targetPath%
	
	echo. copy directory base or client

	echo D| xcopy /y /e %copyPath%\client\client\res %targetPath%\client\res
	echo D| xcopy /y /e %copyPath%\client\base\res %targetPath%\base\res
	copy /y %copyPath%\client\base\config.json %targetPath%\base\config.json
	rem echo. copy directory base or client success
	goto:eof
	
:copyDirectoryBaseClientGame
	echo copyDirectoryBaseClientGame------------------------------------------
	echo. copy directory base or client or game
	md ..\client\ciphercode\game
	md ..\client\ciphercode\client\res
	md ..\client\ciphercode\base\res
	xcopy /y /e /exclude:uncopy.txt ..\client\game ..\client\ciphercode\game
	xcopy /y /e ..\client\client\res ..\client\ciphercode\client\res
	xcopy /y /e ..\client\base\res ..\client\ciphercode\base\res
	xcopy /y /e /exclude:uncopy.txt ..\client\client\src\privatemode ..\client\ciphercode\client\src\privatemode
	xcopy /y /e /exclude:uncopy.txt ..\client\client\src\gamematch ..\client\ciphercode\client\src\gamematch
	copy /y ..\client\base\config.json ..\client\ciphercode\base\config.json
	goto:eof
	
:copyDirectoryGame
	echo copyDirectoryGame------------------------------------------
	echo. copy directory game all
	md ..\client\ciphercode\game
	xcopy /y /e /exclude:uncopy.txt ..\client\game ..\client\ciphercode\game
	goto:eof


:copyAndStudioCustomerOutApk
	echo copyAndStudioCustomerOutApk------------------------------------------
	set releaseOrDebug=%1
	set studioName=%2
	set outApkPath=%3
	
	echo. releaseOrDebug=%releaseOrDebug%  studioName=%studioName% outApkPath=%outApkPath%
	
	if exist "..\frameworks\runtime-src\pro.androidstudio\app\assets" (
		rmdir /s /q ..\frameworks\runtime-src\pro.androidstudio\app\assets
	)
	if exist "..\frameworks\runtime-src\pro.androidstudio\app\build" (
		rmdir /s /q ..\frameworks\runtime-src\pro.androidstudio\app\build
	)
	if exist "..\frameworks\runtime-src\pro.androidstudio\app\release" (
		rmdir /s /q ..\frameworks\runtime-src\pro.androidstudio\app\release
	)
	
	set dirPath=..\resAsset
	if exist %dirPath% (
		rmdir /s /q %dirPath%
	)
	mkdir %dirPath%\base
	xcopy /y /e ..\client\ciphercode\base ..\resAsset\base
	
	set copyDirPath=..\frameworks\runtime-src\pro.androidstudio\app\libs
	call:cleanDirectory %copyDirPath%

	if %releaseOrDebug% == release (
		echo. copy release
		xcopy /y /e .\ndk\release %copyDirPath%
	)
	if %releaseOrDebug% == debug (
		echo. copy debug
		xcopy /y /e .\ndk\debug %copyDirPath%
	)
	
	copy /y .\gradle.properties ..\frameworks\runtime-src\pro.androidstudio\gradle.properties
	copy /y .\settings.gradle ..\frameworks\runtime-src\pro.androidstudio\settings.gradle
	
	PUSHD ..\frameworks\runtime-src\pro.androidstudio
		if %releaseOrDebug% == release (
			echo. *********************studio compile release android studio*********************
			call  gradlew.bat :%studioName%:assembleRelease --stacktrace
		)
		
		if %releaseOrDebug% == debug (
			echo. *********************studio compile debug android studio*********************
			call  gradlew.bat :%studioName%:assembleDebug --stacktrace
		)
	POPD
	if  errorlevel 1 (
		echo. Failed to compile apk %releaseOrDebug% 
		pause
		goto:eof
	)
	
	if %releaseOrDebug% == release (
		echo. copy release apk outApkPath=%outApkPath%.apk
		echo f| xcopy /y  ..\frameworks\runtime-src\pro.androidstudio\app\build\outputs\apk\release\*.apk "%outApkPath%.apk"
	)
	if %releaseOrDebug% == debug (
		echo. copy debug apk outApkPath=%outApkPath%-debug.apk
		echo f| xcopy /y  ..\frameworks\runtime-src\pro.androidstudio\app\build\outputs\apk\debug\*.apk "%outApkPath%-debug.apk"
	)
	
	goto:eof

:copyAndStudioOutApk
	echo copyAndStudioOutApk------------------------------------------
	set releaseOrDebug=%1
	set studioName=%2
	set outApkPath=%3
	
	echo. releaseOrDebug=%releaseOrDebug%  studioName=%studioName% outApkPath=%outApkPath%
	
	if exist "..\frameworks\runtime-src\pro.androidstudio\app\assets" (
		rmdir /s /q ..\frameworks\runtime-src\pro.androidstudio\app\assets
	)
	if exist "..\frameworks\runtime-src\pro.androidstudio\app\build" (
		rmdir /s /q ..\frameworks\runtime-src\pro.androidstudio\app\build
	)
	if exist "..\frameworks\runtime-src\pro.androidstudio\app\release" (
		rmdir /s /q ..\frameworks\runtime-src\pro.androidstudio\app\release
	)
	
	set dirPath=..\resAsset\base
	if exist %dirPath% (
		rmdir /s /q %dirPath%
	)
	mkdir %dirPath%\libs

	xcopy /y /e ..\client\ciphercode\base ..\resAsset\base
	if %releaseOrDebug% == release (
		echo. copy release\libs
		xcopy /y /e .\ndk\release\libs ..\resAsset\base\libs
	)
	if %releaseOrDebug% == debug (
		echo. copy debug\libs
		xcopy /y /e .\ndk\debug\libs ..\resAsset\base\libs
	)
	
	copy /y .\gradle.properties ..\frameworks\runtime-src\pro.androidstudio\gradle.properties
	copy /y .\settings.gradle ..\frameworks\runtime-src\pro.androidstudio\settings.gradle
	
	
	PUSHD ..\frameworks\runtime-src\pro.androidstudio
		if %releaseOrDebug% == release (
			echo. *********************studio compile release android studio*********************
			call  gradlew.bat :%studioName%:assembleRelease --stacktrace
		)
		
		if %releaseOrDebug% == debug (
			echo. *********************studio compile debug android studio*********************
			call  gradlew.bat :%studioName%:assembleDebug --stacktrace
		)
	POPD
	if  errorlevel 1 (
		echo. Failed to compile apk %releaseOrDebug% 
		pause
		goto:eof
	)
	
	if %releaseOrDebug% == release (
		echo. copy release apk outApkPath=%outApkPath%.apk
		echo f| xcopy /y  ..\frameworks\runtime-src\pro.androidstudio\app\build\outputs\apk\release\*.apk "%outApkPath%.apk"
	)
	if %releaseOrDebug% == debug (
		echo. copy debug apk outApkPath=%outApkPath%-debug.apk
		echo f| xcopy /y  ..\frameworks\runtime-src\pro.androidstudio\app\build\outputs\apk\debug\*.apk "%outApkPath%-debug.apk"
	)
	
	goto:eof

:copyDirectorySpecifiedDirectory
	echo copyDirectorySpecifiedDirectory------------------------------------------
	set dir1=%1
	set dir2=%2
	echo. copy directory current path=%dir1%  Target path=%dir2%
	call:createDirectorys %dir2%
	xcopy /y /e /exclude:uncopy.txt %dir1% %dir2%
	goto:eof
	
:copyDirectorySingleGame
	echo copyDirectorySingleGame------------------------------------------
	set fName=%1
	set dir1=%2
	set dir2=%3
	set folder=%4
	echo. copy directory fName=%fName% folder=%folder% current path=%dir1%  Target path=%dir2%
	
	xcopy /y /e /exclude:uncopy.txt %dir1% %dir2%
	
	set targetDir=..\client_publish\%folder%
	if not exist "%targetDir%\%fName%" (
	   mkdir %targetDir%\%fName%
	)
	call:createMd5File %dir2%
	xcopy /y /e %dir2% %targetDir%\%fName%
	rem call WinRAR a -k -m1 -ep1 -afzip -r -o+  %targetDir%\%fName%.zip %dir2%
	call:compressedFile %targetDir%\%fName%.zip %dir2%
	goto:eof
	
:copyTheCompiledGameFile
	echo copyTheCompiledGameFile------------------------------------------
	set folder=%1
	echo. folder=%folder%
	
	set targetDir=..\client_publish
	set copyDir=..\client\ciphercode

	if not exist "%targetDir%\%folder%" (
	   mkdir %targetDir%\%folder%
	)
	if not exist "%copyDir%\gamerar" (
		mkdir %copyDir%\gamerar
	)
	for /f "skip=1 tokens=1,2,3,4,5,6,7,8,9,10 delims==," %%a in (.\game_list.txt) do (
		echo. rar game name=%%b rarname=%%h path=%%f
		rem call WinRAR a -k -m1 -ep1 -afzip -r -o+ %copyDir%\gamerar\%%h.zip %copyDir%\%%f
		call:compressedFile %copyDir%\gamerar\%%h.zip %copyDir%\%%f
	)
	xcopy /y /e %copyDir% %targetDir%\%folder%
	goto:eof

:createMd5File
	echo createMd5File------------------------------------------
	set dir1=%1
	echo. dir1=%dir1%
	
	if not exist %dir1% (
		echo. MD5 file generation failed directory=%dir1%
		goto:eof
	)
	
	if exist "%dir1%\filemd5List.json" (
	   del %dir1%\filemd5List.json
	)
	
	MakeMD5List -dst %temp% -src %dir1%
	
	if exist "%dir1%\res\filemd5List.json" (
	   del %dir1%\res\filemd5List.json
	)
	
	copy %temp%\filemd5List.json %dir1%\res\filemd5List.json
	del %temp%\filemd5List.json
	goto:eof

:copyFile
	echo copyFile------------------------------------------
	set copyFile=%1
	set targetDir=%2
	
	echo. copyFile=%copyFile% targetDir=%targetDir%

	copy %copyFile% %targetDir%
	goto:eof

:copySpecifiedDirectory
	echo copySpecifiedDirectory------------------------------------------
	set vCopyDir=%1
	set vTargetDir=%2
	
	echo. copyDir=%vCopyDir% targetDir=%vTargetDir%

	if not exist %vTargetDir% (
	   mkdir %vTargetDir%
	)
	xcopy /y /e %vCopyDir% %vTargetDir%
	goto:eof

:copyFileOrCompressedFile
	echo copyFileOrCompressedFile------------------------------------------
	set copyDir=%1
	set targetDir=%2
	set vType=%3
	
	echo. copyDir=%copyDir% targetDir=%targetDir% vType=%vType%

	call:copySpecifiedDirectory %copyDir% %targetDir%
	
	if %vType% equ 1 (
		call:compressedFile %targetDir%.zip %copyDir%
	)
	goto:eof
	
:compressedFileBCC
	echo compressedFileBCC------------------------------------------
	set m_fileName=%1
	set m_base=%2
	set m_command=%3
	set m_client=%4
	echo. fileName=%m_fileName% base=%m_base% command=%m_command% client=%m_client%
	rem call WinRAR a -k -m1 -ep1 -afzip -r -o+ %m_fileName% %m_base% %m_command% %m_client%
	call:compressedFile %m_fileName% %m_base% %m_command% %m_client%
	goto:eof
	
:compressedFile
	echo compressedFile------------------------------------------
	echo. all args=%*
	call WinRAR a -k -m1 -ep1 -afzip -r -o+ %*
	
	rem set yFileName=%1
	rem set yDirPath=%2
	rem if exist %yDirPath% (
	rem	call WinRAR a -k -m1 -ep1 -afzip -r -o+ %yFileName% %yDirPath%
	rem ) else (
	rem	echo. createMd5File no such directory %dir1%
	rem )
	goto:eof
	
:deleteDirectory
	echo deleteDirectory------------------------------------------
	set dirPath=%1
	echo. dirPath=%dirPath%
	
	if exist %dirPath% (
		rmdir /s /q %dirPath%
		echo. deleteDirectory Directory success %dirPath%
	) else (
		echo. deleteDirectory no such directory %dirPath%
	)
	goto:eof

:deleteFile
	echo deleteFile------------------------------------------
	set filePath=%1
	echo. filePath=%filePath%
	
	if exist %filePath% (
		del /q /s %filePath%
		echo. deleteFile File success %filePath%
	) else (
		echo. deleteFile no such File %filePath%
	)
	goto:eof
	
:cleanDirectory
	echo cleanDirectory------------------------------------------
	set m_dir=%1
	echo. clean Directory m_dir=%m_dir%
	
	if exist %m_dir% (
	   rmdir /s /q %m_dir%
	)
	mkdir %m_dir%
	echo. clean Directory success %m_dir%
	goto:eof
	
:createDirectorys
	echo createDirectorys------------------------------------------
	set m_dir=%1
	echo. created directory m_dir=%m_dir%
	if not exist %m_dir% (
		mkdir %m_dir%
	) else (
		echo. directory exists %m_dir%
	)
	goto:eof
	
:makefileJksKeystore
	echo makefileJksKeystore------------------------------------------
	
	set outPath=%1
	
	set keystore=%2
	set keystoreAlias=%3
	set key_password=%4
	set store_password=%5
	set ket_dname=%6
	
	echo. outPath=%outPath%
	echo. keystore=%keystore%
	echo. keystoreAlias=%keystoreAlias%
	echo. key_password=%key_password%
	echo. store_password=%store_password%
	echo. dname=%ket_dname%
	
	if not exist %outPath% (
		mkdir %outPath%
	)

	if exist %outPath%\%keystore% (
		echo. there is a key file %outPath%\%keystore%
		goto:eof
		rem del %outPath%\%keystore%
	)
	
	set fileName=""
	set fileSuffix=""
	for %%i in (%keystore%) do (
		set fileName=%%~ni
		set fileSuffix=%%~xi
	)

	echo keystore=%keystore%>%outPath%\%fileName%.txt
	echo %ip%    %ip%alias=%keystoreAlias%>>%outPath%\%fileName%.txt
	echo %ip%    %ip%storepass=%store_password%>>%outPath%\%fileName%.txt
	echo %ip%    %ip%keypass=%key_password%>>%outPath%\%fileName%.txt
	echo %ip%    %ip%dname=%ket_dname%>>%outPath%\%fileName%.txt
	
	if %fileSuffix% == .jks (
		echo. create *.jks file
		call keytool -genkey -v -keystore %outPath%\%keystore% -alias %keystoreAlias% -storepass %store_password% -keypass %key_password% -keyalg RSA -keysize 2048 -validity 36500 -dname %ket_dname%
	)
	
	if %fileSuffix% == .keystore (
		echo. create *.keystore file
		call keytool -genkey -v -keystore %outPath%\%keystore% -alias %keystoreAlias% -storepass %store_password% -keypass %key_password% -keyalg RSA -validity 20000 -dname %ket_dname%
	)
	goto:eof

:signApkEclipse
	echo sign apk eclipse------------------------------------------
	set channel=%1
	
	set apkPath=%2
	set outApkName=%3

	set keyName=%4
	set keyAlias=%5
	set keyPassword=%6
	set keyStorePassword=%7
	
	set outPath=%8
	
	echo. channel=%channel%
	echo. apkPath=%apkPath%
	echo. outApkPath=%outApkPath%
	
	echo. keyName=%keyName%
	echo. keyAlias=%keyAlias%
	echo. keyPassword=%keyPassword%
	echo. keyStorePassword=%keyStorePassword%
	
	set zipPath=%outPath%\%channel%\temp
	call:createDirectorys %zipPath%

	call WinRAR x -ibck %apkPath% %zipPath%
	
	echo. edit channel value %channel%
	
	python channel.py "%zipPath%\assets\base\config.json" %channel%
	rmdir /s /q %zipPath%\META-INF
	
	set apkName=%outPath%\%channel%\abc.apk
	call WinRAR a -k -m1 -ep1 -afzip -r -o+ %apkName% %zipPath%\
	
	echo. sign the new package

	jarsigner -tsa http://sha256timestamp.ws.symantec.com/sha256/timestamp -sigalg SHA1withRSA -digestalg SHA1 -keystore %keyName% -keypass %keyPassword% -storepass %keyStorePassword% -signedjar %outPath%\%outApkName% %apkName% %keyAlias%
	
	echo. signed successfully
	del /q /s %apkName%
	
	goto:eof
	