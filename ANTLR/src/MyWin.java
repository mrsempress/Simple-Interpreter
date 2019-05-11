import java.awt.AlphaComposite;
import java.awt.*;
import javax.swing.*;

import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

interface BaseUI {  // 声明后端所需 UI 操作
	public void reportError(String msg);
	public void showMessage(String msg);
	public void drawPixel(double x, double y, uiPixelAttrib pa);
	public void setTree(org.antlr.v4.runtime.tree.ParseTree tree, String[] ruleNames);
	public void setVisible(Boolean flag);
	public void endPaint(boolean noError);
}

public class MyWin extends JFrame implements BaseUI{
	private   JPanel contentPane;
	protected JComponent jPanel = null; 

	/** 显示图像的设备。缺省为图像显示面板。*/
	protected Graphics2D theDevice ; 
	/**
	 * 将图像保存在缓冲区中
	 * 仅一次生成屏幕大小的图像，每次刷屏时仅显示，可避免闪烁
	 */
	protected Image theOnceImage = null; 
	private int myWidth;
	private int myHeight;
	private int originx;
	private int originy;
	/**
	 * Create the frame.
	 */
	public MyWin() {
		setFont(new Font("宋体", Font.BOLD, 24));
		setTitle("函数绘图语言解释器（ANTLR/Java) from HCX");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		myWidth = screenSize.width / 2;    
		myHeight = screenSize.height * 3 / 4;
		originx = (screenSize.width - myWidth) / 2;
		originy = (screenSize.height - myHeight) / 2;
		setBounds(originx, originy, myWidth, myHeight);

		contentPane = new JPanel();
		contentPane.setBackground(Color.WHITE);
		setContentPane(contentPane);
		jPanel = contentPane;
		jPanel.setFont(getFont());
		contentPane.setLayout(new BorderLayout(0, 0));
		theDevice= (Graphics2D)jPanel.getGraphics();
	}

	public void dispose() {
		super.dispose();
    }

	public void paint(Graphics g) {
		if(!getClass().equals(BaseUI.class))
			super.paint(g);
		else {
			if(theOnceImage != null){
				// 当先调用 super.paint的话，会先清除背景，从而
				// 造成界面闪烁
				g.drawImage(theOnceImage, 0, 0, null);
			}
		}
	}
	public void setVisible(Boolean flag) {
		if(flag) {
			contentPane.setVisible(true);
			jPanel.setVisible(true); 
			this.setVisible(true);
		}
	}
	/** 
	 * 显示出错信息。
	 * 主要用于词法、语法、树分析过程中进行错误提示。
	 * @param msg 信息文本
	 */
	public void reportError(String msg) {
		System.err.print( msg );
		if(msg.length()>0 && msg.charAt(msg.length()-1) != '\n')
    		System.err.print( "\n" );

		if(theDevice == null)
			theDevice = (Graphics2D)jPanel.getGraphics();
        if(theDevice == null) return;
		theDevice.setBackground(Color.WHITE);
		theDevice.clearRect(0, 0, getWidth(), 100);
        ((Graphics)theDevice).setFont(new Font("微软雅黑",Font.BOLD,28));
		theDevice.drawString(msg, 20, 60);
	}
	
	public void showMessage(String msg) {
		System.out.println( msg );
	}
	

	/**
	 * 在 绘图区 绘制一个像素点。
	 * @param x 横坐标
	 * @param y 纵坐标
	 * @param R 颜色之红色分量
	 * @param G 颜色之绿色分量
	 * @param B 颜色之蓝色分量
	 * @param pixelSize 点的大小，有效范围是 2~60
	 */
	public void drawPixel(double x, double y, uiPixelAttrib pa) {
		if( theDevice == null )
			theDevice = (Graphics2D)getGraphics();
		if( theDevice == null )
		    return;
		theDevice.setColor(new Color((int)pa.red(), (int)pa.green(), (int)pa.blue()));
		// 实心圆 绘制一个像素点
		if(Math.abs(x - originx) > myWidth || Math.abs(y - originy) > myHeight) {
			// System.out.println(x+" "+originx+" "+y+" "+originy+" "+myHeight+" "+myWidth);
			showMessage("x: " + x + " y: " + y + "超出边界了");
		}
		theDevice.fillArc((int)x, (int)y, (int)pa.size(), (int)pa.size(), 0, 360);
	}

    public void setTree(org.antlr.v4.runtime.tree.ParseTree tree, String[] ruleNames) {}

    public void beginPaint() {
		setVisible(true);
		//Step 1: 准备空的内存图像，尺寸同全屏幕
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		int imgWidth = screenSize.width; 
		int imgHeight = screenSize.height; 
		theOnceImage = createImage(imgWidth, imgHeight);
		theDevice = (Graphics2D)theOnceImage.getGraphics();
		
		//Step 2: 将内存图像先设置为白色背景
		theDevice.setBackground(Color.WHITE);
		theDevice.clearRect(0, 0, imgWidth, imgHeight);
    }

    public void endPaint(boolean noError) {
		drawWaterMarker(theDevice, 10,100);
        if(theDevice != null) { theDevice.dispose(); }        
        repaint();
    }

	protected void drawWaterMarker(Graphics g, int x, int y){
		String waterMarker = "黄晨晰制作, ANTLR4/Java, 2019";
		AlphaComposite ac = AlphaComposite.getInstance(AlphaComposite.SRC_OVER, (float)0.4);
		Composite oldac = ((Graphics2D)g).getComposite();
		((Graphics2D)g).setComposite(ac);
		g.setColor(Color.BLACK);
		g.setFont(new Font("微软雅黑",Font.BOLD,28));
		g.drawString(waterMarker, (int)x, (int)y);
		((Graphics2D)g).setComposite(oldac);
	}

}
