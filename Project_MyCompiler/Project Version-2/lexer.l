%{
#include "parser.tab.h"
#include <string.h>
#include <stdlib.h>
%}

%%

"agar"              { return IF; }
"warna"             { return ELSE; }
"chhapo"            { return PRINT; }
[0-9]+              { yylval.num = atoi(yytext); return NUM; }
\"[^\"]*\" {
    // Remove the quotes and return the string
    yylval.str = strdup(yytext + 1);
    yylval.str[strlen(yylval.str) - 1] = '\0';
    return STRING;
}
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return VAR; }
[ \t\n]+            { /* skip whitespace */ }
.                   { return yytext[0]; }

%%

int yywrap() { return 1; }
