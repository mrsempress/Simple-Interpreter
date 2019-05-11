grammar DrawGraph;  // 文法名必须和文件名相同
options { 
    language=Java;  
}

// 为生成的语法分析增加自己定义的成员
@parser::members {
  String  auth = "HCX";
  public String getAuth() { return auth; }
}

// 为生成的词法分析增加自己定义的成员
@lexer::members {
  // 目标语言 Java 书写的类成员定义
  String  auth = "HCX";
  public String getAuth() { return auth; }
}

// 语法规则开始
program :  ( statement SEMICO )* EOF   ;
statement :
          statOrigin
        | statScale
        | statRot
        | statFor
        | statColor
        ;

statOrigin : ORIGIN IS  L_BRACKET
          expr COMMA expr R_BRACKET
        ;

statScale :  SCALE IS L_BRACKET
          expr COMMA expr R_BRACKET
        ;

statRot : ROT IS expr 
        ;

statFor : FOR  T1 FROM expr 
          TO   expr STEP expr 
          DRAW L_BRACKET
          expr COMMA expr R_BRACKET
        ;

statColor : COLOR  IS
	    ( RED | BLACK | BLUE | GREEN
	    | L_BRACKET 
	      expr COMMA expr COMMA expr R_BRACKET
	    )
        ;

expr :
         <assoc=right>   expr POWER expr   #PowerExpr  //乘方，最高优先级，右结合
      |  (PLUS | MINUS)  expr              #UnaryExpr  //一元加减运算, 右结合
      |  expr (MUL  | DIV)   expr          #MulDivExpr // 乘除，左结合
      |  expr (PLUS | MINUS) expr          #PlusMinusExpr // 加减，最低优先级，左结合
                                 // 下面这些结构的优先级低于上半部分，不影响分析
      |  CONST_ID    #Const   // pi, e, 0.12, 1, 2.23e-12 
      |  T1          #VarT
      |  ID   L_BRACKET  expr  R_BRACKET  #FuncExpr //  需要判断 ID 是否为支持的函数名，将这个判断放在语义分析阶段了
      |  L_BRACKET       expr  R_BRACKET  #NestedExpr
      ;

// 下面是词法规则
WS  :  [ \t\r\n]+    -> skip  // skip all blank
    ;

COMMENT:	
		(  '//' ~[\r\n]* 
		|  '--' ~[\r\n]* 
		|  '/*' .*? '*/'    /* '?' for non-greedy mode */ 
		)
		-> skip  // skip all comments
		;

PLUS   :	'+'  ;
MINUS  :	'-'  ;
DIV    :	'/'  ;
MUL    :	'*'  ;
POWER  :	'**' ;

SEMICO   :	';' ;
L_BRACKET:	'(' ;
R_BRACKET:	')' ;
COMMA    :	',' ;

CONST_ID :
          IntegerConstant     // 整数字面量，解释器统一看作浮点数
      |   FloatingConstant    // 浮点数字面量
      |   NamedConstant       // 命名的常量，包括 pi 和 e
      ;

// 关键词 fragment 表示这里是正规式的"辅助定义"
fragment
NamedConstant
    :  
      P I    /* pi */
    | E      /* e */
    ;

fragment
IntegerConstant  :   DigitSequence  ;

fragment
FloatingConstant
    :   FractionalConstant ExponentPart?
    |   DigitSequence ExponentPart       // 123E2
    ;

fragment
FractionalConstant
    :   DigitSequence? '.' DigitSequence  // 1.23,  .9(OK)
    |   DigitSequence  '.'                // 3. is OK
    ;

fragment
ExponentPart
    :   E Sign? DigitSequence
    ;

fragment
Sign
    :   '+' | '-'
    ;

fragment
DigitSequence  :  [0-9]+   ;

ORIGIN:	 O R I G I N ;
SCALE :  S C A L E   ;
ROT   :  R O T ;
IS    :  I S   ;
TO    :  T O   ;
STEP  :  S T E P ;
DRAW  :  D R A W ;
FOR   :  F O R   ;
FROM  :  F R O M ;

T1    :  T;

COLOR :  C O L O R;
RED   :  R E D;
BLACK :  B L A C K;
BLUE  :  B L U E  ;
GREEN :  G R E E N;

ID : [a-zA-Z_][a-zA-Z_0-9]*
   ;

ErrText : . ;

fragment A : [aA]; // match either an 'a' or 'A'
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];