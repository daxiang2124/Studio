@echo off

rem 资源文件都放到res里面

rem apk包的名字(.apk 不用输入)
set apkName=indonesia_DominoRich

rem key的信息(没有这个key就创建一个,有就不创建了)
set keystore=dominoRich.jks
set keystoreAlias=dominoRich
set key_password=dominoRich123456dominoRich
set store_password=dominoRich123456dominoRich

set resPath=%~dp0res
set apk=res\%apkName%.apk

set outPath=%~dp0out
set outaab=%outPath%\%apkName%.aab
if not exist %outPath% (
	mkdir %outPath%
)
if not exist "%resPath%\%keystore%" (
	PUSHD ..\
		echo Create jks
		echo. keyName=%keystore%
		echo. alias=%keystoreAlias%
		echo. keystorePassword=%key_password%
		echo. keystoreAliasPassword=%store_password%
		
		call python command.py --keystoreName %keystore% --keystoreAlias %keystoreAlias% --keystorePassword %key_password% --keystoreAliasPassword %store_password% --targetPath %resPath%
	POPD
)

echo package aab file

call python3 bundletool.py -i %apk% -o %outaab% --keystore %resPath%\%keystore% --key_alias %keystoreAlias% --key_password %key_password% --store_password %store_password%

pause