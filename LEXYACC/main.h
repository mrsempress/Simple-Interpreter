#ifndef MAIN_H
#define MAIN_H

#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

typedef double (*MathFuncPtr) (double) ;
typedef double (* FuncPtr) (double);

struct Token
{
	char * lexeme;				// 记号的字符串
	int    type;				// 记号的种别
	double value;				// 如果是常数，常数的值
	double (* FuncPtr)(double);	// 如果是函数，函数的指针
};
struct ExprNode					// 语法树节点类型的定义
{
	enum Token_Type OpCode;		// PLUS, MINUS, MUL, DIV, POWER, FUNC, CONST_ID
	union
	{
		struct  {struct ExprNode *Left, *Right;} CaseOperator;
		struct  {struct ExprNode *Child; FuncPtr MathFuncPtr;} CaseFunc;
		double  CaseConst;
		double  * CaseParmPtr;
	}Content;
};

extern yyparse();									// 语法分析器

											
/*
extern struct ExprNode * MakeExprNode(enum Token_Type opcode,...);
extern double Origin_X, Origin_Y;					// 坐标平移距离
extern double Rot_ang ;								// 旋转角度
extern double Scale_x, Scale_y;						// 比例因子
extern double Parameter;							// 参数 
unsigned int LineNo;								// 行号

extern void DrawLoop(double Start,					// 绘制图形
					 double End,
					 double Step,
					 struct ExprNode * HorPtr,
					 struct ExprNode * VerPtr);
extern void SetRotAngle(double angle);				// 设置旋转角度
extern void SetScale(double x,double y);			// 设置比例因子
extern void SetOrigin(double x,double y);			// 设置平移距离
extern void DrawPixel(unsigned long x,				// 绘制一个点
					  unsigned long y);
extern void DelExprTree(struct ExprNode * root);	// 删除一语法树
extern double GetExprValue(struct ExprNode * root);	// 获得表达式的值
*/

#endif