%{
# include "semantics.h"
# include "y.tab.h"				// 由XDYACC根据源程序生成
# include <stdio.h>
unsigned int LineNo;			// 行号
struct Token tokens;			// 记号
%}

%option case-insensitive
%x comment_entry c_comment_entry

name	   [a-z]([_]?[a-z0-9])*
number     [0-9]+ 
ws         [ \t]+
newline    \n

%%
"//"|"--" { BEGIN comment_entry ;}  /* 行注释 开始 */
<comment_entry>.
<comment_entry>"\n"	 { BEGIN 0;  LineNo ++; }

"/*"	{ BEGIN c_comment_entry ;}   /* 块注释 开始 */
<c_comment_entry>"*/"		{ BEGIN 0; }
<c_comment_entry>.
<c_comment_entry>"\n"		{ ++LineNo; }

{ws}				;							// 空白
{newline}			LineNo ++;					// 换行

"origin"|"原点"		return ORIGIN;
"scale"|"横纵比例"	return SCALE;
"rot"|"旋转角度"	return ROT;
"is"|"是"			return IS;
"for"|"令"			return FOR;
"from"|"自"			return FROM;
"to"|"至"			return TO;
"step"|"步长"		return STEP;
"draw"|"绘制"		return DRAW;
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
