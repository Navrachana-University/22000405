all: compiler.exe

compiler.exe: lex.yy.c parser.tab.c
	gcc -o compiler.exe lex.yy.c parser.tab.c

parser.tab.c parser.tab.h: parser.y
	bison -d parser.y

lex.yy.c: lexer.l parser.tab.h
	flex lexer.l

clean:
	del lex.yy.c parser.tab.c parser.tab.h compiler.exe
