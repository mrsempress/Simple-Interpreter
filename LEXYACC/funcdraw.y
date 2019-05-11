
// -------------------------- funcdraw.y ------------------------------

%{
# define YYSTYPE struct ExprNode *		// �ض��������������Ϊ���ڵ�ָ��
# include "y.tab.h"
# include "semantics.h"
# include <stdarg.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <stdio.h>
extern int yylex (void) ;
unsigned int LineNo;


double	Parameter=0,					// ����T�Ĵ洢�ռ�
		start=0, end=0,	step=0,			// ѭ����ͼ������㡢�յ㡢����
		Origin_x=0, Origin_y=0,			// �ᡢ��ƽ�ƾ���
		Scale_x=1, 	Scale_y=1, 			// �ᡢ�ݱ�������
		Rot_angle=0;					// ��ת�Ƕ�
extern struct Token tokens;				// �Ǻ�
%}

// ------------- �ս������ -------------
%token CONST_ID FUNC FOR FROM DRAW TO STEP ORIGIN SCALE;
%token ROT IS T ERRTOKEN SEMICO COMMA L_BRACKET R_BRACKET;
%left PLUS MINUS;
%left MUL DIV;
%right UNSUB;
%right POWER;
%start Program;

%%
Program :								// ����
	| Program Statement SEMICO
	;
Statement								// ���
	: FOR T FROM Expr TO Expr STEP Expr DRAW L_BRACKET Expr COMMA Expr R_BRACKET
			{  	start = GetExprValue($4);
				end	  = GetExprValue($6);
				step  = GetExprValue($8);
				printf("DRAWLoop start %.2lf to %.2lf, step %.2lf\n", start, end, step);
				DrawLoop(start, end, step, $11, $13) ;
			}
	| ORIGIN IS L_BRACKET Expr COMMA Expr R_BRACKET
			{ 	Origin_x = GetExprValue($4); 
				Origin_y = GetExprValue($6);
				printf("Set Origin (%.2lf, %.2lf)\n", Origin_x, Origin_y);
			}
	| SCALE IS L_BRACKET Expr COMMA Expr R_BRACKET
	        {	Scale_x = GetExprValue($4); 
				Scale_y = GetExprValue($6);
				printf("Set Scale (%.2lf, %.2lf)\n", Scale_x, Scale_y);
			}
	| ROT IS Expr
	        {	Rot_angle = GetExprValue($3);
	            printf("Set ROT (%.2lf)\n", Rot_angle);
			}
	;
Expr									// ���ʽ
    : T							{ $$ = MakeExprNode(T); }
	| CONST_ID					{ $$ = MakeExprNode(CONST_ID,  tokens.value); }
	| Expr PLUS Expr			{ $$ = MakeExprNode(PLUS,  $1, $3); }
	| Expr MINUS Expr			{ $$ = MakeExprNode(MINUS, $1, $3); }
	| Expr MUL Expr				{ $$ = MakeExprNode(MUL,   $1, $3); }
	| Expr DIV Expr				{ $$ = MakeExprNode(DIV,   $1, $3); }
	| Expr POWER Expr			{ $$ = MakeExprNode(POWER, $1, $3); }
	| L_BRACKET Expr R_BRACKET	{ $$ = $2; }
	| PLUS Expr %prec UNSUB		{ $$ = $2; }
	| MINUS Expr %prec UNSUB	
				{ $$ = MakeExprNode(MINUS, MakeExprNode(CONST_ID, 0.0), $2); }
	| FUNC L_BRACKET Expr R_BRACKET	{ $$ = MakeExprNode(FUNC, tokens.FuncPtr, $3);}
	| ERRTOKEN						{ yyerror("error token in the input");}
	;

%%
/*
// ----------------------- ������
void yyerror (const char *Msg) 
{	char errmsg[200];
	memset(errmsg,0,200);
	sprintf(errmsg, "Line %5d : %s", LineNo, yytext);
	printf("%s:%s\n", Msg, errmsg);
}
*/

// ----------------------- �����﷨���е�һ���ڵ�
struct ExprNode * MakeExprNode(enum yytokentype opcode,...)
{	va_list ArgPtr ;
	struct ExprNode *ExprPtr = malloc(sizeof(struct ExprNode));
	ExprPtr->OpCode = opcode;
	va_start (ArgPtr,opcode) ;                  //ʹ��ָ��,������ջ���еĲ����б�,�ӵ͵�ַ���ߵ�ַһ��һ���ذѲ������ݶ�����
	switch(opcode)
	{	case CONST_ID:
			ExprPtr->Content.CaseConst = (double)va_arg(ArgPtr, double);
			break;
		case T:
			ExprPtr->Content.CaseParmPtr = &Parameter;
			break;
		case FUNC:
			ExprPtr->Content.CaseFunc.MathFuncPtr = (FuncPtr)va_arg(ArgPtr, FuncPtr);
			ExprPtr->Content.CaseFunc.Child 
					= (struct ExprNode *) va_arg (ArgPtr,struct ExprNode *);
			break;
		default:    //PLUS MINUS MUL DIV POWER
			ExprPtr->Content.CaseOperator.Left
					= (struct ExprNode *)va_arg (ArgPtr,struct ExprNode *);
			ExprPtr->Content.CaseOperator.Right
					= (struct ExprNode *)va_arg (ArgPtr,struct ExprNode *);
			break;
	}
	va_end(ArgPtr); //���ȡ�����в������Ӻ�������֮ǰ���������va_end()���ɴ�ȷ����ջ����ȷ�ָ���
	return ExprPtr;
}

char SrcFilePath[300];              //���ڴ�������ļ�·��
extern FILE *yyin;
int InitScanner(char* filename) {
    yyin = fopen(filename, "r");
    if(yyin == NULL){
        printf("Error to open the source file %s!\n", filename);
        return 0;
    }
    return 1;
}

int CloseScanner() {
    fclose(yyin);
    return 0;
}

int main(int argc, char* argv[]){
    if(argc < 2) {
        printf("Usage: %s file\n", argv[0]);
        return 1;
    }
    strcpy(SrcFilePath, argv[1]);

    if(1 != InitScanner(SrcFilePath)) return 1;
     yyparse();

     /*
     FILE* fp = NULL;
     char cmd[512];
     sprintf(cmd, "python Draw.py");
     printf("Use command: %s\n",cmd);
     if ((fp = popen(cmd, "r")) == NULL) {
         printf("Failed python\n");
         return 1;
     }
     */

/*
    FILE* fp = NULL;
    char cmd[512];
    sprintf(cmd, "python");
    printf("%s\n",cmd);
    if ((fp = popen(cmd, "r")) == NULL) {
       printf("Failed python\n");
       return 1;
    }
    sprintf(cmd, "import matplotlib.pyplot as plt");
    printf("%s\n",cmd);
    if ((fp = popen(cmd, "r")) == NULL) {
          printf("Failed import\n");

          sprintf(cmd, "exit()");
          popen(cmd, "r");
          return 1;
    }
*/

/*
    //��ʼ��Python����
    Py_Initialize();
    if (!Py_IsInitialized()){
        printf("Initialize Error!\n");
        return 0;
    }

    PyRun_SimpleString("import sys");
    //���Insertģ��·��
    PyRun_SimpleString("sys.path.append('./')");

    //����ģ��
    PyObject* pModule = PyImport_ImportModule("Draw");

    if (!pModule) {
       printf("Python get module failed.\n");
       return 0;
    }

     //��ȡInsertģ����_add����
     PyObject* pFunc = PyObject_GetAttrString(pModule, "draw");
     if (!pFunc || !PyCallable_Check(pFunc)) {
        printf("Can't find function (draw)\n");
        return 0;
     }

     //��ʼ��Ҫ����Ĳ�����args���óɴ�������������ģʽ
     PyObject* args = PyTuple_New(2);
     //��Long������ת����Python�ɽ��յ�����
     PyObject* arg1 = PyLong_FromLong(4);
     PyObject* arg2 = PyLong_FromLong(3);

     yyparse();

     PyObject * pv = PyObject_GetAttrString(pModule, "show");
     if(!pv) {
        printf("Can't find function (show)\n");
        return 0;
     }

     PyEval_CallObject(pv, NULL);

     Py_Finalize();
*/

/*
    yyparse();
    sprintf(cmd, "exit()");
    popen(cmd, "r");
    pclose(fp);

*/
    CloseScanner();
    return 0;
}