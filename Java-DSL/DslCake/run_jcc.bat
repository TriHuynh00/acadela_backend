SET fileName=.\execCmd.txt

IF NOT "%1" == "" (
  SET fileName=%1
)
java -cp "E:\TUM\Thesis\DSL-Connecare\dsl-connecare\Java-DSL\DslCake\class\" Parser %fileName%