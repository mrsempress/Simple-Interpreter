%{
# include "semantics.h"
# include "y.tab.h"				// ��XDYACC����Դ��������
# include <stdio.h>
unsigned int LineNo;			// �к�
struct Token tokens;			// �Ǻ�
%}

%option case-insensitive
%x comment_entry c_comment_entry

name	   [a-z]([_]?[a-z0-9])*
number     [0-9]+ 
ws         [ \t]+
newline    \n

%%
"//"|"--" { BEGIN comment_entry ;}  /* ��ע�� ��ʼ */
<comment_entry>.
<comment_entry>"\n"	 { BEGIN 0;  LineNo ++; }

"/*"	{ BEGIN c_comment_entry ;}   /* ��ע�� ��ʼ */
<c_comment_entry>"*/"		{ BEGIN 0; }
<c_comment_entry>.
<c_comment_entry>"\n"		{ ++LineNo; }

{ws}				;							// �հ�
{newline}			LineNo ++;					// ����

"origin"|"ԭ��"		return ORIGIN;
"scale"|"���ݱ���"	return SCALE;
"rot"|"��ת�Ƕ�"	return ROT;
"is"|"��"			return IS;
"for"|"��"			return FOR;
"from"|"��"			return FROM;
"to"|"��"			return TO;
"step"|"����"		return STEP;
"draw"|"����"		return DRAW;
"t"					return T;

"pi"	tokens.type = CONST_ID; tokens.value   = 3.14159;	return CONST_ID;
"e"		tokens.type = CONST_ID; tokens.value   = 2.71828;	return CONST_ID;
"sin"	tokens.type = FUNC;     tokens.FuncPtr = sin;		return FUNC;
"cos"	tokens.type = FUNC;     tokens.FuncPtr = cos;		return FUNC;
"tan"	tokens.type = FUNC;     tokens.FuncPtr = tan;		return FUNC;
"exp"	tokens.type = FUNC;     tokens.FuncPtr = exp;		return FUNC;
"ln"	tokens.type = FUNC;     tokens.FuncPtr = log;		return FUNC;
"sqrt"	tokens.type = FUNC;     tokens.FuncPtr = sqrt;		return FUNC;
"-"		return MINUS;
"+"		return PLUS;
"*"		return MUL;
"/"		return DIV;   
","		return COMMA;
";"		return SEMICO;
"("		return L_BRACKET;
")"		return R_BRACKET;
"**"	return POWER;

{number}(\.{number}+)?	{	tokens.value = atof(yytext) ;
							tokens.type = CONST_ID;
							return CONST_ID ;
						}
{name}	return ERRTOKEN;
.		return ERRTOKEN;

%%
int yywrap() { return   1; }