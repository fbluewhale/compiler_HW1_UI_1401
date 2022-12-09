simple lexer for below grammars

    stmt -> compound-stmt | if-stmt | while-stmt | assign-stmt;
    compound-stmt -> { stmt-list }
    if-stmt -> if expr stmt | if expr stmt else stmt
    while-stmt -> while expr do stmt
    assign-stmt -> id= expr
    expr -> expr + expr | expr – expr | expr * expr | expr / expr | expr < expr | expr <= expr | expr > expr |
    expr >= expr | expr != expr | expr == expr | (expr) | id | num
    stmt-list -> stmt stmt-list | stmt

### usage

execute python script from main directory:

```
$ python3.10 main.py
```

read p.txt then tokenized it

#TODO
[]sweeping :)
