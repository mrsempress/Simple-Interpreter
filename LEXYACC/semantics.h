// -------------------------- semantics.h ------------------------------
#ifndef SEMANTICS_H
#define SEMANTICS_H
//#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "y.tab.h"

#define MAX_CHARS 200
#define black RGB(0,0,0)
#define red RGB(255,0,0)

typedef double (*MathFuncPtr) (double);
typedef double (* FuncPtr) (double);
struct Token {
	//char * lexeme;
	//int    type;
    enum yytokentype type;
	double value;
	double (* FuncPtr)(double);
};
struct ExprNode	{
    enum yytokentype OpCode;	// PLUS, MINUS, MUL, DIV, POWER, FUNC, CONST_ID
	union
	{	struct  {struct ExprNode *Left, *Right;} CaseOperator;
		struct  {struct ExprNode *Child; FuncPtr MathFuncPtr;} CaseFunc;
		double  CaseConst;
		double  * CaseParmPtr;
	} Content;
};

extern struct ExprNode * MakeExprNode(enum yytokentype opcode,...);

extern void DrawLoop(double Start,
					 double End,
					 double Step,
					 struct ExprNode * HorPtr,
					 struct ExprNode * VerPtr);
extern void DrawPixel(unsigned long x,
					  unsigned long y);
extern double GetExprValue(struct ExprNode * root);

extern int yyparse();

extern void yyerror (const char *Msg);
#endif
