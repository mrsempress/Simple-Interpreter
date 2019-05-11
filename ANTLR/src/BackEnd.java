import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class BackEnd {
  protected ParseTree tree = null; // 分析树
  protected BaseUI theUI = null;// UI类型自定义

  public BackEnd(ParseTree t, BaseUI ui){ 
    tree=t;  theUI = ui; 
  }

  //执行应用层的计算逻辑
  public void run() {
	  ParseTreeWalker walker = new ParseTreeWalker();
    DrawerListener eval = new DrawerListener();
   	eval.setUI( theUI ); // 关联 UI 对象
   	walker.walk( eval , tree ); // 监听器模式
  }
}