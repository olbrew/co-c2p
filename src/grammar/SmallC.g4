/**
 * 
 */
grammar SmallC;

/*
* Parser Rules
*/
smallc_program : include* (function_definition)*;

function_definition : EXTERN? type_specifier id '(' param_decl_list? ')' (compound_stmt | ';');

id : (AMPERSAND | ASTERISK)? IDENTIFIER (array_definition | array_indexing)?;

array_definition : '[' INTEGER ']';
array_indexing : '[' expr ']';

include : INCLUDE '<' FILENAME '>';

type_specifier : CONST? (INT | CHAR | BOOL | VOID);

param_decl_list : parameter_decl (',' parameter_decl )* (',' parameter_pack)?;
parameter_pack : '...';
parameter_decl : type_specifier id?;

param_list : expr (',' expr )*;

compound_stmt : '{' (var_decl* stmt*)? '}';

var_decl : type_specifier var_decl_list ';';

var_decl_list :  variable_id ( ',' variable_id)*;

variable_id  : id ( '=' expr )?;

stmt : compound_stmt | cond_stmt | while_stmt | for_stmt | BREAK ';' | CONTINUE ';' | RETURN expr ';' | READINT '(' id ')' ';' | WRITEINT '(' expr ')' ';' | assignment ';' | functioncall ';'; //

cond_stmt :  IF '('  expr ')' stmt (ELSE stmt)?;

while_stmt : WHILE '(' expr ')' stmt;

for_stmt : FOR '(' (var_decl | ';') expr? ';' expr? ')' stmt;

expr : assignment | condition | functioncall;

assignment : id '=' expr; //

functioncall : id '(' param_list? ')';

condition : disjunction | disjunction '?' expr ':' condition;

disjunction :  conjunction | disjunction '||' conjunction;

conjunction : comparison | conjunction '&&' comparison;

comparison : relation | relation '==' relation;

relation : sum | sum (LEFTANGLE | RIGHTANGLE) sum;

sum : sum PLUS term | sum MINUS term | term;

term : term ASTERISK factor | term SLASH factor | term PROCENT factor | factor;

factor : EXCLAMATIONMARK factor | MINUS factor | primary;

primary :  INTEGER | CHARCONST | BOOLEAN | id | '(' expr ')' | functioncall;

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

// modifier keywors
CONST : 'const';

// datatypes
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
CHARCONST : '"' (.)*? '"' | '\'' (.)*? '\'';
BOOLEAN : 'true' | 'false';
IDENTIFIER : (UNDERSCORE | CHARACTER) (UNDERSCORE | CHARACTER | DIGIT)*;
FILENAME : (UNDERSCORE | CHARACTER | DIGIT | DOT)+;

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

// text formatting
COMMENT : ('/*' (.)*? '*/' | '//' (.)*? '\n') -> skip;
NEWLINE : ('\r'? '\n')+ -> skip;
WHITESPACE : (' ' | NEWLINE | '\t' | '\u000C') -> skip;