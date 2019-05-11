# 编译原理——解释器编写

## 规则

解释器可以实现以下语句：

* 循环绘图（FOR-DRAW）
  * `FOR T FROM 起点 TO 终点 STEP 步长 DRAW(横坐标, 纵坐标)`
  * 令T从起点到终点、每次改变一个步长，绘制出由(横坐标，纵坐标)所规定的点的轨迹
* 比例设置（SCALE）
  * `SCALE IS (横坐标比例因子，纵坐标比例因子)`
  * 设置横坐标和纵坐标的比例，并分别按照比例因子进行缩放
* 角度旋转（ROT）
  * `ROT  IS 角度`
  * 逆时针旋转角度所规定的弧度值。具体计算公式：
    * 旋转后X=旋转前X*COS(角度)+旋转前Y*SIN(角度) 
    * 旋转后Y=旋转前Y*COS(角度)-旋转前X*SIN(角度)
* 坐标平移（ORIGIN）
  * `ORIGIN IS (横坐标，纵坐标)`
  * 将坐标系的原点平移到横坐标和纵坐标规定的点处
* 注释        （-- 或 //）
  * // 或 -- 之后，直到行尾，均是注释



坐标系（画图）规则：

* 左上角为原点
* x方向从左向右增长
* y方向**从上到下增长**(与一般的坐标系方向相反)



其他规则：

* 语言对大小写不敏感，例如for、For、FOR等，均被认为是同一个保留字。
* 语句中表达式的值均为双精度类型，旋转角度单位为弧度且为逆时针旋转，平移单位为点。  



## 词法分析

记号数据结构

``` python
class Token:
    """
    This class stores the information for token
    token - 'TokenType' type
    lexeme - original string of input
    value - corresponding value if it is 'CONST_ID'
    func_ptr - function pointer if it is 'FUNC'
    """

    def __init__(self, token, lexeme="", value=0, func_ptr=None):
        self.token_type = token
        self.string = lexeme
        self.value = value
        self.func_ptr = func_ptr

```



记号的分类与表示

``` python
class TokenType(Enum):
    """
    This class stores all the key words
    """
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    FOR = "FOR"
    FROM = "FROM"
    T = "T"
    SEMICO = ';'
    L_BRACKET = '('
    R_BRACKET = ')'
    COMMA = ','
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    POWER = '**'
    FUNC = "FUNCTION"
    CONST_ID = 21
    NONTOKEN = 22
    ERRTOKEN = 23
    
```



## 语法分析

根据规定语句进行匹配，同时对Expression进行处理，并将结果预先处理，记录结果



## 语义分析





## 画图

在画图中，需要用到`python`的库`matplotlib.pyplot`

### Matplotlib.pyplot

`matplotlib.pyplot`是有状态的，即它会保存当前图片和作图区域的状态，新的作图函数会作用在当前图片的状态基础之上

``` python
import matplotlib.pyplot as plt

# 设置坐标轴的取值范围
plt.xlim((from,to))
plt.ylim((from,to))

# X轴从from到to，取number个点，也就是修改了坐标轴的刻度
plt.xticks(np.linspace(from, to, number))

# 设置横纵坐标的单位长度一致
ax.set_aspect("equal")

# 颜色，线宽度，线的风格
plt.plot(x, y, color = 'red', linewidth = 1.0, linestyle = '--')

# 获取当前的坐标轴, gca = get current axis
ax = plt.gca()

# 设置右边框和上边框
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 设置x坐标轴为下边框
ax.xaxis.set_ticks_position('bottom')
# 设置y坐标轴为左边框
ax.yaxis.set_ticks_position('left')

# 翻转y轴
ax.invert_yaxis()

# 设置x轴, y轴在(0, 0)的位置
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

# 绘制散点图
plt.scatter(x, y, s = 75, c = color, alpha = 0.5)

# 显示图形，在显示图形前可以对图形进行属性更改
plt.show()
```

