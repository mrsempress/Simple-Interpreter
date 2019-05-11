// -------------------------- main.c ------------------------------
#include "../../LEXYACC/LEXYACC/semantics.h"
#include "../../LEXYACC/LEXYACC/lex.yy.c"
#include "../../LEXYACC/LEXYACC/y.tab.c"

char SrcFilePath[MAX_CHARS];				// 用于存放源程序文件路径

static FILE *InFile;
static char Name[] = "Compiler";			// 窗口名
static int PrepareWindow(HINSTANCE,			// 初始化窗口函数声明
                         HINSTANCE,
                         int);
static int CheckSrcFile(LPSTR);				// 检查源程序文件是否合法函数声明
static void CloseFile();					// 关闭分析的源文件
static LRESULT CALLBACK WndProc(HWND,
        UINT,
        WPARAM,
        LPARAM);	// 窗口消息处理函数声明
extern int yyparse();
extern FILE *yyin;
//----------------------   window程序主函数
int APIENTRY WinMain(HINSTANCE hInstance,
                    HINSTANCE hPrevInstance,
                    LPSTR     lpCmdLine,
                    int       nCmdShow)
{   MSG Msg;
    strcpy(SrcFilePath,lpCmdLine);	//保存源文件路径
    if ( PrepareWindow(hInstance,hPrevInstance,nCmdShow) != 1)	// 初始化窗口
    {	MessageBox(NULL,"窗口初始化失败 !", "错误", MB_OK);
        return 1;
    }
    if ( !CheckSrcFile(lpCmdLine))	return 1;	//检查要分析的源程序文件
    yyparse();		// 调用语法分析器
    CloseFile();	// 关闭文件

    while(GetMessage(&Msg,NULL,0,0))	//进入window消息循环
    {	TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }
    return Msg.wParam;
}

//----------------------   初始化窗口
int PrepareWindow(HINSTANCE hInst, HINSTANCE hPrevInstance, int nCmdShow)
{	HWND hWnd;
    WNDCLASS W;

    memset(&W,0,sizeof(WNDCLASS));
    W.style = CS_HREDRAW | CS_VREDRAW;
    W.lpfnWndProc = WndProc;
    W.hInstance = hInst;
    W.hCursor = LoadCursor(NULL,IDC_ARROW);
    W.hbrBackground = (HBRUSH) (COLOR_WINDOW + 1);
    W.lpszClassName = Name;
    RegisterClass(&W);

    hWnd = CreateWindow(Name,Name,WS_OVERLAPPEDWINDOW,
                    10,10,740,490,NULL,NULL,hInst,NULL);
    if(hWnd == NULL) return 0;

    ShowWindow(hWnd,nCmdShow);
    UpdateWindow(hWnd);
    SetCursor(LoadCursor(hInst,IDC_ARROW));

    hDC = GetDC(hWnd);
    return 1;
}

//----------------------   检查源程序文件是否合法
int CheckSrcFile(LPSTR lpszCmdParam)
{   InFile = NULL;
    if(strlen(lpszCmdParam) == 0)
    {   MessageBox(NULL,"未指定源程序文件 !","错误",MB_OK);
        return 0;
    }
    if((InFile = fopen(lpszCmdParam,"r")) == NULL){
        MessageBox(NULL,"打开源程序文件出错 !","错误",MB_OK);
        MessageBox(NULL,lpszCmdParam,"文件名",MB_OK);
        return 0;
    }
    yyin = InFile;
    return 1;
}

//----------------------   关闭源文件
static void CloseFile()
{
    if(InFile != NULL) fclose(InFile);
}

//----------------------   窗口处理
LRESULT CALLBACK WndProc(HWND hWnd,
                         UINT Message,
                         WPARAM wParam,
                         LPARAM lParam)
{   switch(Message)
    {	case WM_DESTROY:
            ReleaseDC(hWnd,hDC);
            PostQuitMessage(0);
            return 0;
            break;
        case WM_PAINT:
        {	PAINTSTRUCT pt;
            BeginPaint(hWnd,&pt);
            EndPaint(hWnd,&pt);
        }
        default:
            return DefWindowProc(hWnd,Message,wParam,lParam);
    }
}
