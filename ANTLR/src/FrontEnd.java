import java.io.FileInputStream; 
import java.io.InputStream;    

import org.antlr.v4.runtime.*; 
import org.antlr.v4.runtime.tree.ParseTree;
public class FrontEnd {
	protected ParseTree tree = null; // 分析树
  	protected String theFilePath; // 文件路径

  	public FrontEnd(String filePath) {
   		theFilePath = filePath; 
  	}

  	public ParseTree getTree() {
    	return tree; 
    }
    
    // 语法+词法分析，返回输入中的语法错误数量
  	public int  doParse() throws Exception { 
    	java.io.InputStream is = System.in;
    	if ( theFilePath != null ) {
        	is = new FileInputStream(theFilePath);
    	}
			// 1+4 层对象，构造时关联起来
			ANTLRInputStream input = new ANTLRInputStream( is );
			DrawGraphLexer lexer = new DrawGraphLexer(input);
			CommonTokenStream tokens = new CommonTokenStream(lexer);
			DrawGraphParser parser = new DrawGraphParser(tokens);
    	// 这里的调用，意味着 program 是文法的开始符号
    	tree   = parser.program (); 
    	int nErr = parser.getNumberOfSyntaxErrors();
    	return nErr; //返回语法错误数
    }
}