@echo off

set outPath=%~dp0out

call:createProguardFile

pause
exit

:createProguardFile
	call:createPathContent %outPath%

	@REM 混淆文件
	set fileName=proguard.txt
	
	@REM 混淆数量(多少条数据,默认12000(0就会默认值))
	set obfuscationsCount=30000

	@REM 混淆字符
	set chars_00="ހށ;ނ;ރ;ބ;ޅ;ކ;އ;ވ;މ;ފ;ދ;ތ;ލ;ގ;ޏ;ސ;ޑ;ޒ;ޓ;ޔ;ޕ;ޖ;ޗ;ޘ;ޙ;ޚ;ޛ;ޜ;ޝ;ޞ;ޟ;ޠ;ޡ;ޢ;ޣ;ޤ;ޥ"
	set chars_01="Ф;Ə;ϧ;ʘ;Ӿ;߿;ԯ;$;֎;Ԩ"
	set chars_02="֍;֎;֏;߽;߾;߿;$;ԯ;Ф;Ԩ;Ӿ;ϧ;ʘ;$;Ə;߿"
	set chars_03="Ԩ;ԩ;Ԫ;ԫ;Ԭ;ԭ;Ԯ;ԯ;ϧ;߽"
	set chars_04="ϧ;ʘ;Ӿ;߿;$;އ;ވ;މ;ފ;ދ;ތ;ލ;ގ;ޏ;ސ;ޑ;ԫ;Ԭ;ԭ;Ԯ;ԯ;֎;Ф;Ə"
	set chars_05=%chars_00%;%chars_01%;%chars_02%;%chars_03%;%chars_04%

	
	PUSHD ..\
		call python command.py --proguard true --fileName %fileName% --numberOfObfuscations %obfuscationsCount% --chars %chars_00% --targetPath %outPath%
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

:createPathContent
	set dpc=%1
	echo delete path content
	if not exist %dpc% (
		mkdir %dpc%
	)
	goto:eof