%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
void yyerror(const char *s);

int vars[26]; // For storing variable values

int temp_count = 0;
char* new_temp() {
    char buf[10];
    sprintf(buf, "t%d", temp_count++);
    return strdup(buf);
}

char* concat(const char* s1, const char* s2, const char* s3) {
    char* result = malloc(strlen(s1) + strlen(s2) + strlen(s3) + 3);
    sprintf(result, "%s%s%s\n", s1, s2, s3);
    return result;
}
%}

%union {
    int num;
    char* str;
    struct {
        char* code;
        char* place;
        int num;
    } expr;
}

%token <num> NUM
%token <str> VAR
%token IF ELSE PRINT
%token <str> STRING

%type <expr> expr

%left '+' '-'
%left '*' '/'
%start program

%%

program:
    program stmt
    | /* empty */
    ;

stmt:
    expr ';' {
        printf("Intermediate Code:\n%sResult stored in: %s\n", $1.code, $1.place);
    }
    | PRINT '(' expr ')' ';' {
        printf("Output: %d\n", $3.num);
    }
    | PRINT '(' STRING ')' ';' {
        printf("Output: %s\n", $3); free($3);
    }
    | VAR '=' expr ';' {
        vars[$1[0] - 'a'] = $3.num;
        printf("Assigned %d to variable %c\n", $3.num, $1[0]);
        free($1);
    }
    | IF '(' expr ')' block ELSE block {
        if ($3.num)
            printf("IF Branch\n");
        else
            printf("ELSE Branch\n");
    }
    ;

block:
    '{' program '}'
    ;

expr:
    NUM {
        char buf[20];
        sprintf(buf, "%d", $1);
        $$.place = strdup(buf);
        $$.code = strdup("");
        $$.num = $1;
    }
    | VAR {
        $$.place = $1;
        $$.code = strdup("");
        $$.num = vars[$1[0] - 'a']; // Fetch the stored value
    }
    | expr '+' expr {
        $$.place = new_temp();
        char line[100];
        sprintf(line, "%s = %s + %s", $$.place, $1.place, $3.place);
        $$.code = concat($1.code, $3.code, line);
        $$.num = $1.num + $3.num;
    }
    | expr '-' expr {
        $$.place = new_temp();
        char line[100];
        sprintf(line, "%s = %s - %s", $$.place, $1.place, $3.place);
        $$.code = concat($1.code, $3.code, line);
        $$.num = $1.num - $3.num;
    }
    | expr '*' expr {
        $$.place = new_temp();
        char line[100];
        sprintf(line, "%s = %s * %s", $$.place, $1.place, $3.place);
        $$.code = concat($1.code, $3.code, line);
        $$.num = $1.num * $3.num;
    }
    | expr '/' expr {
        $$.place = new_temp();
        char line[100];
        sprintf(line, "%s = %s / %s", $$.place, $1.place, $3.place);
        $$.code = concat($1.code, $3.code, line);
        $$.num = $3.num != 0 ? $1.num / $3.num : 0;
    }
    | '(' expr ')' {
        $$ = $2;
    }
    ;

%%

void yyerror(const char *s) {
    printf("syntax error\n");
}
