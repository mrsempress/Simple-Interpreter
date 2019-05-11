
#include "..\\funcdraw\\scanner.h"

void main(int argc, char *argv[])
{
	Token token;
	if (argc < 2)
	{	printf("please input Source File !\n" );	return;
	}
	if(!InitScanner(argv[1]))            //��ʼ���ʷ�������
	{	printf("Open Source File Error ! \n");		return;
	}
	printf("�Ǻ����    �ַ���      ����ֵ      ����ָ��\n");
    printf("____________________________________________\n");
	while(1)
	{	token = GetToken();				//��üǺ�
		if(token.type != NONTOKEN)		//��ӡ�Ǻŵ�����
				printf("%4d,%12s,%12f,%12x\n",
					token.type, token.lexeme, token.value, token.FuncPtr); 
		else	break;
	};
    printf("____________________________________________\n");
	CloseScanner();
}
