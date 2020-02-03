echo "compiling code with JAVACC"
SET jjFileName=Exp2.jj
echo "arg1 = %1"
IF NOT "%1"=="" (
	SET jjFileName=%1
)
javacc.bat -DEBUG_PARSER -OUTPUT_DIRECTORY:.\src\ .\src\%jjFileName%
