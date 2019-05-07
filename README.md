# Simple-Interpreter
1. Python 2. c, Lex and yacc; 2. Java, ANTLR

This interpreter implements basic drawing functions.
Through lexical analysis, parsing, semantic analysis, and the ability to add graphics.

Supported statements:
ORIGIN IS(expr, expr);
ROT IS expr;
SCALE IS (expr, expr);
FOR T FROM expr TO expr STEP expr DRAW (expr, expr);
COLOR IS (RED | GREEN | BLUE) | (expr, expr, expr)

Three notes:
1. --
2. //
3. /**/

Divided into three phases:
The first stage, after compiling the principle course, hand-written, using python tools
The second stage, using the lex and yacc tools, but no implementation interface, MACOS system does not support
The third stage, using the ANTLR tool, implements the interface.
