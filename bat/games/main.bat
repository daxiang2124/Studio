@echo off

set outPath=%~dp0out

rem 打包[大厅,子游戏](package lobby or sub game)
rem call:packageLobby
rem call:packageSubGame
rem call:platformPackageSubGame
rem call:platformCopyProjectPackageSubGame
rem call:gamesMd5


rem 同步文件(svn)
rem call:svnCommand
rem call:syncContent

pause
exit

:packageLobby
	rem 打包项目-大厅
	echo package lobby
	call:deletePathContent %outPath%

	rem 打包的平台或项目名字
	set platform=all
	set platform_all=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh;nation_customer
	set platform_c=nation_customer
	
	set platform_i=nation_india
	
	rem 印度
	set platform_rb=n_rummybest
	set p_joyrummy=n_joyrummy;n_teenpatiiparty;india_google_3PattiDiamond
	set p_pattifun=n_teen_patti_fun;n_teen_patti_rich;India_google_TeenpattiWind
	set p_teenpattilive=n_teenpattilive;n_teenpattionline;n_rummytour;india_google_TeenpattiGuru
	set p_teenpattigo=n_teen_patti_go;india_google_TeenpattiHappy
	set p_teenpatticlub=n_teen_patti_club;india_google_a_TeenpattiKing
	set p_rummyclub=n_rummy_club;n_teen_patti_royal;n_teen_patti_palace;india_google_teenpattipartyS
	set p_rummygo=n_rummyGo;n_teen_patti_winner;n_hello_rummy_a;india_google_TeenpattiSunny
	set p_india_other=india_google_RummySilver;india_google_UpDownWinner;india_google_UpDownStar;india_google_RummyNoble_qmdl;india_google_UpDownCrazy
	set platform_ii=%platform_rb%;%p_joyrummy%;%p_pattifun%;%p_teenpattilive%;%p_teenpattigo%;%p_teenpatticlub%;%p_rummyclub%;%p_rummygo%;%p_india_other%
		
	set platform_tr=n_teen_patti_rich
	set platform_rummyGo=n_rummyGo;n_teen_patti_winner;n_hello_rummy_a;india_google_TeenpattiSunny;india_google_LudoWind
	set platform_teenpattiClub=n_teen_patti_club;india_google_a_TeenpattiKing;india_google_LudoStar;india_google_LudoRoom
	set platform_gc=%platform_rummyGo%;%platform_teenpattiClub%
	
	set platform_e=india_666Entertainment;india_RummyLoot;india_RummyStar;india_RummyGlee;india_RummySatta;india_TeenpattiBaaz
	
	rem 巴基斯坦
	set platform_p=pakistan;pakistan_google_goldteenpatti;pakistan_google_CardRummy_qmdl;pakistan_google_3PattiLucky_qmdl;pakistan_google_3PattiGame_qmdl;pakistan_google_RummyCrash_qmdl;pakistan_google_3pattiBlue_qmdl
	
	
	PUSHD ..\
		call python command.py --packageLobby lobby --platform %platform_rb% --targetPath %outPath%
	POPD
	goto:eof
	
:packageSubGame
	rem 打包项目-子游戏
	echo package sub game	
	call:deletePathContent %outPath%

	rem 子游戏路径
	set vSubgamePath=client/game/yule/rummy
	set vSubgamePath_a="client/game/yule/andarbahar|client/game/yule/bestoffives|client/game/yule/baccaratnew|client/game/yule/carroulette|client/game/yule/teenpatti20|client/game/yule/zooroulette"
	
	rem 打包的平台或项目名字
	set platform=all
	set platform_all=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh;nation_customer
	set platform_rb=n_rummybest
	
	echo. projectName=%vProjectName%
	echo. subgamePath=%vSubgamePath%

	PUSHD ..\
		call python command.py --projectName %platform_rb% --subgamePath %vSubgamePath% --targetPath %outPath%
	POPD
	goto:eof
	
:platformPackageSubGame
	rem 打包平台-子游戏
	echo designated platform sub-game package
	call:deletePathContent %outPath%

	rem 子游戏路径
	set vSubgamePath=client/game/yule/ballsports
	set vSubgamePath_a="client/game/yule/andarbahar|client/game/yule/bestoffives|client/game/yule/baccaratnew|client/game/yule/carroulette|client/game/yule/teenpatti20|client/game/yule/zooroulette"
	
	rem 打包的平台或项目名字
	set platform=all
	set platform_all=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh;nation_customer
	
	set platform_tr=n_teen_patti_rich
	set platform_rummyGo=n_rummyGo;n_teen_patti_winner;n_hello_rummy_a;india_google_TeenpattiSunny;india_google_LudoWind
	set platform_teenpattiClub=n_teen_patti_club;india_google_a_TeenpattiKing;india_google_LudoStar;india_google_LudoRoom
	set platform_c=%platform_rummyGo%;%platform_teenpattiClub%

	echo. gamePath=%vSubgamePath%
	echo. platform=%platform_c%

	PUSHD ..\
		call python command.py --subgamePath %vSubgamePath% --platform %platform_c% --targetPath %outPath%
	POPD
	goto:eof
	
:platformCopyProjectPackageSubGame
	rem 打包平台-子游戏(拷贝目录下子游戏)
	echo designated platform sub-game package
	call:deletePathContent %outPath%
	
	rem 子游戏路径
	set vSubgamePath=client/game/yule/rummy
	set vSubgamePath_a="client/game/yule/andarbahar|client/game/yule/bestoffives|client/game/yule/baccaratnew|client/game/yule/carroulette|client/game/yule/teenpatti20|client/game/yule/zooroulette"
	
	rem 拷贝的项目
	set	vCopyProject=n_rummybest
	
	rem 打包的平台或项目名字
	set platform=all
	set platform_all=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh;nation_customer
	
	rem 印度
	set platform_yb=n_rummybest
	set p_joyrummy=n_joyrummy;n_teenpatiiparty
	set p_pattifun=n_teen_patti_fun;n_teen_patti_rich
	set p_teenpattilive=n_teenpattilive;n_teenpattionline;n_rummytour
	set p_teenpattigo=n_teen_patti_go
	set p_teenpatticlub=n_teen_patti_club
	set p_rummyclub=n_rummy_club;n_teen_patti_royal;n_teen_patti_palace
	set p_rummygo=n_rummyGo;n_teen_patti_winner;n_hello_rummy_a
	set platform_i=%p_joyrummy%;%p_pattifun%;%p_teenpattilive%;%p_teenpattigo%;%p_teenpatticlub%;%p_rummyclub%;%p_rummygo%
	
	set platform_c=india_777wealth;
	
	echo. copyProject=%vCopyProject%
	echo. gamePath=%vSubgamePath%
	echo. platform=%platform%

	PUSHD ..\
		call python command.py --subgamePath %vSubgamePath% --copyProject %vCopyProject% --platform %platform_i% --targetPath %outPath%
	POPD
	goto:eof

:gamesMd5
	echo Sync game md5
	call:deletePathContent %outPath%
	set contentFile=D:\git\SvnLocal\client-dabao\india_666Entertainment\client\ciphercode\client
	
	PUSHD ..\
		call python command.py --dirMd5 %contentFile% --targetPath %outPath%
	POPD
	goto:eof

rem rem svn
:svnCommand
	rem 执行svn命令
	rem  注意:1同步文件时本工程svn处理干净,命令上传不能区分目录,2安装svn命令(检查svn命令是否能用)
	echo execute the svm command
	
	rem set vSvnCommand="svn add *|svn commit -m "delete client/base 33""
	set vSvnCommand="svn update"
	
	rem 打包的平台或项目名字
	set platform=all
	set platform_all=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh;nation_customer
	
	set platform_i=nation_india
	set platform_o=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh;nation_customer
	
	PUSHD ..\
		call python command.py --svnCommand %vSvnCommand% --platform %platform_i%
		
		rem call python command.py --svnCommand %vSvnCommand% --platform %platform_o%
	POPD
	goto:eof

:syncContent
	rem 同步内容
	rem  注意:1同步文件时本工程svn处理干净,命令上传不能区分目录,2安装svn命令(检查svn命令是否能用)
	echo Sync content
	
	rem syncContent 同步的内容|;分隔(单个| 多个;)
	rem 例如同步单个文件:info/PythonCommand.py|info 把文件nfo/PythonCommand.py 复制目标info目录下
	set vContentFile="info/PythonCommand.py|info"
	set vContentDir="info/abc123|info/abc123"
	set vContentDir_a="info/abc123|info/abc123;info/testx|info/testx"
	set vContentDir_b="info/aaabbbcccc.bat|info;info/aaabbbccccdd.bat|info"
	
	set vContentFile_d="info/PythonCommand.py|info"
	
	rem copyProject 拷贝的项目
	set vCopyProject=n_rummybest
	set vCopyProject_c=india_777wealth
	
	rem platform 打包的平台或项目名字
	set vPlatform=all
	set vPlatform_all=nation_india;nation_indonesia;nation_thailand;nation_mexico;nation_brazil;nation_pakistan;nation_bangladesh
	set vPlatform_i=nation_india
	set vPlatform_c=nation_customer
	set vPlatform_p=nation_pakistan
	
	rem platform 特殊客户平台
	set vPlatform_cother=india_google_AndarBaharGame;india_google_UpDownLucky
	
	PUSHD ..\
		rem 客户
		call python command.py --syncContent %vContentFile_d% --copyProject %vCopyProject% --platform %vPlatform_c%
		
		rem 特殊客户
		rem call python command.py --syncContent %vContentFile_d% --copyProject %vCopyProject% --platform %vPlatform_cother%
		
		rem 印度
		rem call python command.py --syncContent %vContentFile_d% --copyProject %vCopyProject% --platform %vPlatform_i%
	POPD
	goto:eof

:createProjectConfiguration
	rem 创建项目配置
	set vContentFile="info/PythonCommand.py|info"
	set vProjectName=n_rummybest
	PUSHD ..\
		call python command.py --syncContent %vContentFile% --projectName %vProjectName%
	POPD
	goto:eof

:deletePathContent
	set dpc=%1
	echo delete path content
	if exist %dpc% (
	   rmdir /s /q %dpc%
	)
	mkdir %dpc%
	goto:eof

:PdsdseAAAAA
	setlocal enabledelayedexpansion
		set cdccd=%~dp0
		set tOutPath=%cdccd%ouacb
		rem if exist %tOutPath% (
		rem     rmdir /s /q %tOutPath%
		rem )
		rem mkdir %tOutPath%
		for /f "skip=1 tokens=1,2,3,4,5,6,7,8,9,10,11,12,13,14 delims==," %%a in (.\info.txt) do (
			rem echo lck=%%l lcv=%%n
			echo subGameName=%%b pathOffset=%%j copyDirectory=%%d targetPath=%%h targetName=%%f outPaht=%tOutPath% lckey=%%l lcvalue=%%n
			rem call:runBatCopyDir %%b %%j %%d %%h %%f %tOutPath% %%l %%n

			echo outname=%tOutPath%\%%f
			if not exist %tOutPath%\%%f (
				mkdir %tOutPath%\%%f
			)
			rem call %%h\%%f\info\Project.bat
			echo target name=%%f luacompile_key=%%l luacompile_value=%%n
			echo  
			call %%d\info\sendDirectory.bat %%d\%%j\%%b %tOutPath%\%%f %%l %%n
		)
	endlocal
	goto:eof

:india
	echo india table
	setlocal enabledelayedexpansion
		set cdccd=%~dp0
		set tOutPath=%cdccd%ouacb
		rem if exist %tOutPath% (
		rem     rmdir /s /q %tOutPath%
		rem )
		rem mkdir %tOutPath%
		for /f "skip=1 tokens=1,2,3,4,5,6,7,8,9,10 delims==," %%a in (.\india.txt) do (
			echo targetName=%%f dbname=%%b pathOff=%%j cpyeDir=%%d mbdir=%%h outPaht=%tOutPath%
			call:runBatCopyDir %%b %%j %%d %%h %%f %tOutPath%
		)
	endlocal
	goto:eof
	
:indonesia
	echo indonesia table
	setlocal enabledelayedexpansion
		set cdccd=%~dp0
		set tOutPath=%cdccd%ouacb
		rem if exist %tOutPath% (
		rem     rmdir /s /q %tOutPath%
		rem )
		rem mkdir %tOutPath%
		for /f "skip=1 tokens=1,2,3,4,5,6,7,8,9,10 delims==," %%a in (.\indonesia.txt) do (
			echo targetName=%%f dbname=%%b pathOff=%%j cpyeDir=%%d mbdir=%%h outPaht=%tOutPath%
			call:runBatCopyDir %%b %%j %%d %%h %%f %tOutPath%
		)
	endlocal
	goto:eof

:customer
	echo customer table
	setlocal enabledelayedexpansion
		set cdccd=%~dp0
		set tOutPath=%cdccd%ouacb
		rem if exist %tOutPath% (
		rem     rmdir /s /q %tOutPath%
		rem )
		rem mkdir %tOutPath%
		for /f "skip=1 tokens=1,2,3,4,5,6,7,8,9,10 delims==," %%a in (.\customer.txt) do (
			echo targetName=%%f dbname=%%b pathOff=%%j cpyeDir=%%d mbdir=%%h outPaht=%tOutPath%
			call:runBatCopyDir %%b %%j %%d %%h %%f %tOutPath%
		)
	endlocal
	goto:eof

:runBatCopyDir
	echo package subgame - read target path item
	rem 打包子游戏-读取目标路径项目

	rem 子游戏名称
	set subGameName=%1
	rem 路径偏移量
	set pathOffset=%2
	rem 拷贝目录
	set copyDirectory=%3
	rem 目标路径
	set targetPath=%4
	rem 目标名字
	set targetName=%5
	rem 输出路径
	set outPaht=%6
	
	echo .... subGameName=%subGameName% pathOffset=%pathOffset% copyDirectory=%copyDirectory% targetPath=%targetPath% targetName=%targetName% outPaht=%outPaht%
	
	set copyDir=%copyDirectory%\%pathOffset%\%subGameName%
	set mbdir=%targetPath%\%targetName%\%pathOffset%\%subGameName%
	rem if exist %mbdir% (
	rem    rmdir /s /q %mbdir%
	rem )
	rem echo d| xcopy /y /e %copyDir% %mbdir%
	
	set outPath=%outPaht%\%targetName%
	if not exist %outPath% (
		mkdir %outPath%
	)

	echo  .... copy the contents of the path %targetPath%\%targetName%
	call %targetPath%\%targetName%\info\Project.bat
	echo  .... target name=%targetName% luacompilekey=%luacompile_key% luacompilevalue=%luacompile_value%
	call %copyDirectory%\info\sendDirectory.bat %copyDir% %outPath% %luacompile_key% %luacompile_value%
	
	rem  .... echo content under the target path %targetPath%\%targetName%
	rem call %targetPath%\%targetName%\info\Project.bat
	rem  .... echo target name=%targetName% luacompile_key=%luacompile_key% luacompile_value=%luacompile_value% mbdir=%mbdir%
	rem call %targetPath%\%targetName%\info\sendDirectory.bat %mbdir% %outPath% %luacompile_key% %luacompile_value%

	echo  .... delete cache directory %outPath%\%subGameName%
	if exist %outPath%\%subGameName% (
		rmdir /s /q %outPath%\%subGameName% 
	)
	
	goto:eof