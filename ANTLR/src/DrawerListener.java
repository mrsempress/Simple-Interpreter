/**
 * 本文定义解释器后端中的监听器类。
 * 当 BackEnd 采用 Listener 模式访问分析树时，
 * 将使用这个文件中的类 DrawerListener，
 * 以便在遍历树时回调这里定义的操作。
*/
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

@SuppressWarnings({"deprecation"})
public class DrawerListener extends DrawGraphBaseListener {
    BaseUI theUI =null;
    public DrawerListener(){}
    public void setUI(BaseUI ui){
        theUI = ui;        
    }

    private ParseTreeProperty<Double> values = new ParseTreeProperty<Double>();
    public void setValue(ParseTree node, double value) { values.put(node, value); }
    public double getValue(ParseTree node) { return values.get(node); }
    
    // 跨产生式使用的语义变量
    private double valueOfT =0; // for 语句中，循环变量 T 的当前值
    private double originX =0; // 坐标平移参数
    private double originY =0; 
    private double scaleX =1;  // 横向缩放因子
    private double scaleY =1;  // 纵向缩放因子
    private double rotate =0;  // 旋转角度
    private uiPixelAttrib  pixelAttrib = new uiPixelAttrib();

// 下面是重置了父类的方法
	@Override public void exitStatOrigin(DrawGraphParser.StatOriginContext ctx){
	    originX = getValue( ctx.expr(0) );
	    originY = getValue( ctx.expr(1) );
	    theUI.showMessage("OriginX=" + originX + " originY=" + originY );
	}

	@Override public void exitStatScale(DrawGraphParser.StatScaleContext ctx){
	    scaleX = getValue( ctx.expr(0) );
	    scaleY = getValue( ctx.expr(1) );
   		theUI.showMessage("scaleX=" + scaleX + " scaleY=" + scaleY );
	}

	@Override public void exitStatRot(DrawGraphParser.StatRotContext ctx){
	    rotate = getValue( ctx.expr() );
   		theUI.showMessage("rotate=" + rotate );
	}

	@Override public void exitStatFor(DrawGraphParser.StatForContext ctx){
	    if(pixelAttrib == null) pixelAttrib = new uiPixelAttrib();
	    double Tbegin = getValue( ctx.expr(0));
	    double Tend   = getValue( ctx.expr(1));
	    double Tstep  = getValue( ctx.expr(2));

        ParseTreeWalker walker = new ParseTreeWalker(); //用于多次遍历子树
	    for(valueOfT = Tbegin; valueOfT <Tend; valueOfT += Tstep){	        
            walker.walk(this , ctx.expr(3));      // 遍历子树，获得当前的逻辑坐标
			double x = getValue( ctx.expr(3) );
            walker.walk(this , ctx.expr(4));
			double y = getValue( ctx.expr(4) );

			x *= scaleX; y *= scaleY;           // 先比例变换
			double tmp;
			tmp = x*Math.cos(rotate) + y*Math.sin(rotate); // 再旋转变换
			y = y*Math.cos(rotate)-x*Math.sin(rotate);
			x = tmp;
			x+=originX; y+=originY;              // 最后平移变换
			theUI.drawPixel(x, y, pixelAttrib);
			// System.out.println(x);
			// System.out.println(y);
			// System.out.println(pixelAttrib.size());
			// System.out.println(pixelAttrib.red());
			// System.out.println(pixelAttrib.green());
			// System.out.println(pixelAttrib.blue());
         	// theUI.showMessage("*** PIXEL at (" + x + ", " + y + ")");
	    }
	}

	@Override public void exitStatColor(DrawGraphParser.StatColorContext ctx){
	    TerminalNode node = ctx.RED();
	    if(node != null) {
	        pixelAttrib = new uiPixelAttrib(255, 0, 0);
	        return;
	    }
	    
	    node = ctx.GREEN();
	    if(node != null) {
	        pixelAttrib = new uiPixelAttrib(0, 255, 0);
	        return;
	    }
	    node = ctx.BLUE();
	    if(node != null) {
	        pixelAttrib = new uiPixelAttrib(0, 0, 255);
	        return;
	    }

	    node = ctx.BLACK();
	    if(node != null) {
	        pixelAttrib = new uiPixelAttrib(0, 0, 0);
	        return;
	    }
	    
	    double r = getValue( ctx.expr(0) );
	    double g = getValue( ctx.expr(1) );
	    double b = getValue( ctx.expr(2) );
    	    
  	    pixelAttrib = new uiPixelAttrib(r, g, b);
	}

	@Override public void exitPowerExpr(DrawGraphParser.PowerExprContext ctx){
	    double left = getValue( ctx.expr(0) ); // 左操作数的值
	    double right = getValue( ctx.expr(1) ); // 右操作数的值
	    double value = Math.pow(left, right);
	    setValue(ctx, value);
	}

	@Override public void exitMulDivExpr(DrawGraphParser.MulDivExprContext ctx){
	    double left = getValue( ctx.expr(0) ); // 左操作数的值
	    double right = getValue( ctx.expr(1) ); // 右操作数的值
	    double value = 0;
	    if( ctx.MUL() != null ) value = left * right;
	    else if(right != 0)value = left / right;  // 这里应检查除数是否为0!
	    setValue(ctx, value);
	}

    
	@Override public void exitVarT(DrawGraphParser.VarTContext ctx){
	    setValue(ctx, valueOfT);
	}

	@Override public void exitConst(DrawGraphParser.ConstContext ctx){
	    Token tk = ctx.CONST_ID().getSymbol();    // 获得记号对象
	    String vName = tk.getText().toLowerCase();// 获得记号对象的文本并转换为小写字母
	    double value = 0;
	    
	    if(vName.equals("pi")) value = Math.PI; //3.1415926
	    else if(vName.equals("e")) value = Math.E; //2.7182818284
	    else {
	        try {
	           value = Double.valueOf(vName);
	        } catch(Exception e) {
	            theUI.showMessage("error " + tk.getLine() + ":" 
	               + tk.getCharPositionInLine()
	               + "  不支持的常量名 '" + vName  +"'" );
	            value = 0;
	        }
	    }

	    setValue(ctx, value);
	}

	@Override public void exitPlusMinusExpr(DrawGraphParser.PlusMinusExprContext ctx){
	    double left = getValue( ctx.expr(0) ); // 左操作数的值
	    double right = getValue( ctx.expr(1) ); // 右操作数的值
	    double value = 0;
	    if( ctx.PLUS() != null ) value = left + right;
	    else value = left - right;
	    setValue(ctx, value);
	}

	@Override public void exitNestedExpr(DrawGraphParser.NestedExprContext ctx){
	    setValue(ctx, getValue(ctx.expr()));
    }

	@Override public void exitUnaryExpr(DrawGraphParser.UnaryExprContext ctx){
	    double value = getValue( ctx.expr() ); // 操作数的值
	    if( ctx.PLUS() == null ) value = -1 * value;
	    setValue(ctx, value);
    }

	@Override public void exitFuncExpr(DrawGraphParser.FuncExprContext ctx){
	    Token id = ctx.ID().getSymbol();
	    String funcName = id.getText().toLowerCase();
	    double value = 0;
	    double param = getValue(ctx.expr());  // 函数调用的参数值
	    if(funcName.equals("sin")) value = Math.sin(param);
	    else if(funcName.equals("cos")) value = Math.cos(param);
	    else if(funcName.equals("tan")) value = Math.tan(param);
	    else {
	        theUI.showMessage("error " + id.getLine() + ":" 
	               + id.getCharPositionInLine()
	               + "  不支持的函数名 '" + funcName  +"'" );
	    }
	    setValue(ctx, value);	    
	}


	@Override public void visitErrorNode(ErrorNode node) { }    
}
