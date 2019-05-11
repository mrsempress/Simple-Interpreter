// -------------------------- semantics.c ------------------------------
#include "semantics.h"
//#define PY_SSIZE_T_CLEAN
//#include "include/python3.6m/Python.h"
# include <stdarg.h>
# include <stdlib.h>
# include <string.h>
# include <stdio.h>

extern double
		Parameter,
		start, end,	step,
		Origin_x, Origin_y,
		Scale_x, Scale_y,
		Rot_angle;
extern unsigned int LineNo;
extern unsigned char *yytext;
//extern PyObject * pFunc;

void DrawPixel(unsigned long x, unsigned long y);
void DrawLoop(double Start,
			  double End,
			  double Step,
			  struct ExprNode * HorPtr,
			  struct ExprNode * VerPtr);
double GetExprValue(struct ExprNode * root);

static void Errmsg (char *string);
static void CalcCoord(struct ExprNode * Hor_Exp,
					  struct ExprNode * Ver_Exp,
					  double * Hor_x,
					  double * Ver_y);


void Errmsg (char *string) { exit (1); }


static void CalcCoord(struct ExprNode * Hor_Exp,
					  struct ExprNode * Ver_Exp,
					  double * Hor_x,
					  double * Ver_y)
{
	double HorCord, VerCord, Hor_tmp;


	HorCord = GetExprValue(Hor_Exp);
	VerCord = GetExprValue(Ver_Exp);


	HorCord *= Scale_x ;
	VerCord *= Scale_y ;


	Hor_tmp = HorCord * cos(Rot_angle) + VerCord * sin(Rot_angle);
	VerCord = VerCord * cos(Rot_angle) - HorCord * sin(Rot_angle);
	HorCord = Hor_tmp;


	HorCord += Origin_x;
	VerCord += Origin_y;


	* Hor_x = HorCord;
	* Ver_y = VerCord;
}


void DrawLoop(double Start,
			  double End,
			  double Step,
			  struct ExprNode * HorPtr,
			  struct ExprNode * VerPtr)
{
    double x, y;
	for(Parameter = Start; Parameter <= End; Parameter += Step)
	{	CalcCoord(HorPtr, VerPtr, &x, &y);
		DrawPixel((unsigned long)x, (unsigned long)y);
	}
    //printf("-------------------------------temp end---------------------------------\n");
}

// -------------------------- ?????????
void DrawPixel(unsigned long x, unsigned long y)
{
//    FILE* fp = fopen("output.txt", "a+");
//    if(fp == NULL) {
//        printf("File output error");
//        exit(0);
//    }
//    fprintf(fp, "%lu %lu\n", x, y);
//    fclose(fp);

	//printf("now the dot is at x: %lu, y: %lu\n", x, y);
/*
    PyObject *args = NULL;
    args = PyTuple_New(2);

    PyTuple_SetItem(args, 0, x);

    PyTuple_SetItem(args, 1, y);


    PyObject_CallObject(pFunc, args);
*/

/*
	FILE* fp = NULL;
	char cmd[512] = "plt.scatter(";
	char i[50]; sprintf(i, "%lu", x);
	//itoa(x,i);
	char j[50]; sprintf(i, "%lu", x);
	//itoa(y,i);
	strcat(i, j);
	strcat(cmd, i);
	char z[20] = ", s=1)";
	strcat(cmd, z);
	printf("%s\n",cmd);
	if ((fp = popen(cmd, "r")) == NULL) {
		printf("Failed draw\n");
	}
 */
}


double GetExprValue(struct ExprNode * root)
{	if (root == NULL) return 0.0;
	switch (root -> OpCode)
	{	case PLUS  :
			return GetExprValue(root->Content.CaseOperator.Left ) +
					GetExprValue(root->Content.CaseOperator.Right) ;
		case MINUS :
			return GetExprValue(root->Content.CaseOperator.Left ) -
					GetExprValue(root->Content.CaseOperator.Right) ;
		case MUL   :
			return GetExprValue(root->Content.CaseOperator.Left ) *
					GetExprValue(root->Content.CaseOperator.Right) ;
		case DIV   :
			return GetExprValue(root->Content.CaseOperator.Left ) /
					GetExprValue(root->Content.CaseOperator.Right) ;
		case POWER :
			return pow(GetExprValue(root->Content.CaseOperator.Left ),
					GetExprValue(root->Content.CaseOperator.Right) );
		case FUNC  :
			return (* root->Content.CaseFunc.MathFuncPtr)
					(GetExprValue(root->Content.CaseFunc.Child) );
		case CONST_ID :
			return root->Content.CaseConst ;
		case T  :
			return *(root->Content.CaseParmPtr);
		default    :
			return 0.0 ;
	}
}


void yyerror (const char *Msg)
{	char errmsg[200];
	memset(errmsg,0,200);
	sprintf(errmsg, "Line %d", LineNo);
	printf("%s:%s\n", Msg, errmsg);
}