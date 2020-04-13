SET jjFileName=Cake.jj
IF NOT "%1"=="" (
  SET jjFileName=%1
)
.\jcc_compile.bat %jjFileName% && .\java_compile.bat