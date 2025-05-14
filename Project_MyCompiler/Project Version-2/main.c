#include <stdio.h>

extern FILE *yyin;
int yyparse();

int main() {
    yyin = fopen("test2.txt", "r");
    if (!yyin) {
        perror("test2.txt");
        return 1;
    }

    yyparse();
    fclose(yyin);
    return 0;
}
