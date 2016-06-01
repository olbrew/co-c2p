grammar SmallC;

/*
 * Parser Rules
 */
smallc_program : include* (var_decl | function_definition)*;

function_definition : EXTERN? type_specifier identifier '(' param_decl_list? ')' (compound_stmt | ';');

identifier : (AMPERSAND | ASTERISK)? IDENTIFIER (array_definition | array_indexing)?;

array_definition : '[' INTEGER ']';
array_indexing : '[' expr ']';

//include : INCLUDE '<' FILENAME '>';
include : INCLUDE '<' STDIO '>';

type_specifier : CONST? (FLOAT | INT | CHAR | BOOL | VOID);

param_decl_list : parameter_decl (',' parameter_decl )* (',' parameter_pack)?;
parameter_pack : '...';
parameter_decl : type_specifier identifier?;

param_list : expr (',' expr )*;

compound_stmt : '{' (var_decl | stmt)* '}';

var_decl : type_specifier var_decl_list;

var_decl_list :  variable_id ( ',' variable_id)* ';';

variable_id  : identifier ( '=' expr )?;

stmt : compound_stmt | cond_stmt | while_stmt | for_stmt | BREAK ';' | CONTINUE ';' | RETURN expr ';' | READINT '(' identifier ')' ';' | WRITEINT '(' expr ')' ';' | assignment ';' | functioncall ';'; //

cond_stmt :  IF '('  expr ')' stmt (ELSE stmt)?;

while_stmt : WHILE '(' expr ')' stmt;

for_stmt : FOR '(' (var_decl | var_decl_list) expr? ';' expr? ')' stmt;

expr : assignment | condition | functioncall;

assignment : identifier '=' expr; //

functioncall : identifier '(' param_list? ')';

condition : disjunction | disjunction '?' expr ':' condition;

disjunction :  conjunction | disjunction '||' conjunction;

conjunction : comparison | conjunction '&&' comparison;

comparison : relation | relation EQUALITY relation | relation NEQUALITY relation;

relation : equation | equation (LEFTANGLE | RIGHTANGLE) equation;

equation : equation PLUS term | equation MINUS term | term;

term : term ASTERISK factor | term SLASH factor | term PROCENT factor | factor;

factor : EXCLAMATIONMARK factor | MINUS factor | primary;

primary :  INTEGER | REAL | CHARCONST | BOOLEAN | identifier | '(' expr ')' | functioncall;

/*
 * Lexer Rules
 */
// keywords
BREAK : 'break';
CONTINUE : 'continue';
ELSE : 'else';
IF : 'if';
RETURN : 'return';
WHILE : 'while';
FOR : 'for';
INCLUDE: '#include';
EXTERN: 'extern';

// idioms
READINT : 'readint';
WRITEINT : 'writeint';

// modifier keywords
CONST : 'const';

// datatypes
FLOAT : 'float';
INT : 'int';
CHAR : 'char';
BOOL : 'bool';
VOID : 'void';

// fragments
fragment DIGIT: [0-9];
fragment NUMBER : DIGIT+;
fragment CHARACTER : [a-zA-Z];
fragment SIGN : PLUS | MINUS;

// elements
INTEGER : NUMBER;
REAL : NUMBER'.'NUMBER'f';
CHARCONST : '"' (.)*? '"' | '\'' (.)*? '\'';
BOOLEAN : 'true' | 'false';
IDENTIFIER : (UNDERSCORE | CHARACTER) (UNDERSCORE | CHARACTER | DIGIT)*;
//FILENAME : (UNDERSCORE | CHARACTER | DIGIT | DOT)+;
STDIO: 'stdio.h';

// special characters
PLUS : '+';
MINUS : '-';
ASTERISK : '*';
SLASH : '/';
AMPERSAND : '&';
PROCENT : '%';
UNDERSCORE: '_';
EXCLAMATIONMARK : '!';
QUESTIONMARK : '?';
DOT : '.';
COLON : ':';
SEMICOLON : ';';
ASSIGN : '=';
COMMA : ',';
LEFTANGLE : '<';
RIGHTANGLE : '>';
LEFTPARENTHESIS : '(';
RIGHTPARENTHESIS : ')';
LEFTCURLY : '{';
RIGHTCURLY : '}';
OR : '||';
AND : '&&';
EQUALITY : '==';
NEQUALITY : '!=';

// text formatting
COMMENT : ('/*' (.)*? '*/' | '//' (.)*? '\n') -> skip;
NEWLINE : ('\r'? '\n')+ -> skip;
WHITESPACE : (' ' | NEWLINE | '\t' | '\u000C') -> skip;
