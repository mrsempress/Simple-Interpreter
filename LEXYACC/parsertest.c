#include <stdio.h>

extern void Parser(char * SrcFilePtr);

void main(int argc, char *argv[])
{
	if (argc < 2)
	{	printf("please input Source File !\n" );	return;
	}
	Parser("test.txt");
}
