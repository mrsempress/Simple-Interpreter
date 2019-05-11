public class DrawLangMain {
	public static void main(String[] args) {
   		if( args.length < 1){
     		System.err.println("应提供源文件！\n");
     		System.exit(1);
		}
   		try {
      		BaseUI theUI = new MyWin();
      		DrawLangMain.doFile(args[0], theUI);
   		} catch(Exception e) {
			System.err.println("Exception in main: "+e);
			e.printStackTrace(); 	
			System.exit(1);
   		}
   	}

   	public static void  doFile(String file, BaseUI theUI) throws Exception { // 调用前端对象 完成对输入的语法分析
		FrontEnd fe = new FrontEnd(file);
		int nErr = fe.doParse();

  		if(nErr > 0){
     		theUI.showMessage ("语法分析发现错误了!");
     		System.gc();  
     		return; 
     	}
		theUI.setVisible(true); 
  		// 调用后端对象 完成对应用层的计算
  		BackEnd be =new BackEnd(fe.getTree(), theUI);
		be.run(); 
	}
}