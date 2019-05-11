flex -i funcdraw.l	
bison -d -o y.tab.c funcdraw.y 
gcc -o fdgl y.tab.c lex.yy.c semantics.c
./fdgl test1
