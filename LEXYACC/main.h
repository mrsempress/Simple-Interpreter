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
	char * lexeme;				// �Ǻŵ��ַ���
	int    type;				// �Ǻŵ��ֱ�
	double value;				// ����ǳ�����������ֵ
	double (* FuncPtr)(double);	// ����Ǻ�����������ָ��
};
struct ExprNode					// �﷨���ڵ����͵Ķ���
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

extern yyparse();									// �﷨������

											
/*
extern struct ExprNode * MakeExprNode(enum Token_Type opcode,...);
extern double Origin_X, Origin_Y;					// ����ƽ�ƾ���
extern double Rot_ang ;								// ��ת�Ƕ�
extern double Scale_x, Scale_y;						// ��������
extern double Parameter;							// ���� 
unsigned int LineNo;								// �к�

extern void DrawLoop(double Start,					// ����ͼ��
					 double End,
					 double Step,
					 struct ExprNode * HorPtr,
					 struct ExprNode * VerPtr);
extern void SetRotAngle(double angle);				// ������ת�Ƕ�
extern void SetScale(double x,double y);			// ���ñ�������
extern void SetOrigin(double x,double y);			// ����ƽ�ƾ���
extern void DrawPixel(unsigned long x,				// ����һ����
					  unsigned long y);
extern void DelExprTree(struct ExprNode * root);	// ɾ��һ�﷨��
extern double GetExprValue(struct ExprNode * root);	// ��ñ��ʽ��ֵ
*/

#endif