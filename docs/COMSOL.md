[COMSOL快速教程](https://cn.comsol.com/video/basics-comsol-multiphysics-18-minutes)

[COMSOL使用教程(PDF)](https://cdn.comsol.com/translated-documentation/cn/5.3/COMSOLMultiphysics%E7%AE%80%E4%BB%8B.pdf)

## COMSOL多物理场的工作流程

|定义问题|初始化问题|几何|材料属性|边界条件|网格|求解|后处理|优化|
|-|-|-|-|-|-|-|-|-|
|定义需要<br>求解的问题|初始化模型|绘制或导入CAD|定义求解域|设定边界条件|网格划分|求解|后处理和报告|优化修改|

## 1 定义问题

### 例：热微执行器

- 问题描述：
    - 在执行器一段施加电压
    - 电流生成热
    - 结构发生膨胀
    - 最终求解温度、变形、应力

> 多物理场：电+热+结构力学
>
> 建模难点在于如何反向简化模型

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol1.png?raw=true){width=200}

### 定义问题逻辑

|定义分析目标|几何维度|确定所需物理场|确定多物理场耦合|
|-|-|-|-|
|获得执行器通电后的热变形情况|三维|电流<br>固体传热<br>固体力学|电磁热<br>热膨胀|

## 2 几何建模

### 几何体素

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol2.png?raw=true){width=200 align=right}

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol3.png?raw=true){width=150}

每个对象包含“域”、“边界”、“边”、“点”属性，对任意一个几何体素进行变换操作时，都要选中对应的域/边界/边/点进行操作，同时要注意操作的结果是否符合逻辑

### 几何操作

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol4.png?raw=true){width=200}

#### 阵列

用于在x,y,z方向上生成相同的几何体素，快速构建零部件

<figure markdown>
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol5.png?raw=true){width=500}
<figcaption>变换前几何体素</figcaption>
</figure>

<figure markdown>
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol6.png?raw=true){width=400}
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol7.png?raw=true){width=400}
<figcaption>阵列操作选项</figcaption>
</figure>

<figure markdown>
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol8.png?raw=true){width=400}
<figcaption>阵列变换效果</figcaption>
</figure>

#### 移动

<figure markdown>
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol9.png?raw=true){width=400}
<figcaption>移动特定几何体素选项</figcaption>
</figure>

#### 布尔操作

- 并集
- 交集
- 差集

<figure markdown>
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol10.png?raw=true){width=400}
<figcaption>圆柱与长方体进行差集运算后几何图像</figcaption>
</figure>

#### 工作平面

可以选取平面绘制二维图像，方便进行变换操作（拉伸，旋转等）

<figure markdown>
![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol11.png?raw=true){width=400}
</figure>

### 几何模型定义的逻辑

**几何体素的定义>>变换操作>>逻辑操作**

## 3 CFD接口

### 单相流

#### 使用雷诺数确定流型

$$Re_L=\frac{\rho UL}{\mu}=\frac{惯性力}{粘性力}$$

- 低雷诺数(<<1)：蠕动流
    - 粘性力阻碍了所有流体脉动的产生
    - 可逆的平滑流型
- 中等雷诺数(~1-2000)：层流
    - 惯性力重要性增加
    - 粘性力被限制在边界层、剪切层、尾迹内部
    - 规则、平滑流型
- 高雷诺数(>4000)：湍流

#### 雷诺数计算

- 平板流 $Re_x=\frac{Ux}{\nu}$
- 圆球扰流 $Re_L=\frac{UL}{\nu}$
- 管流 $Re_{Dh}=\frac{UD_h}{\nu}\quad D_h=\frac{4A(横截面积)}{P(周长)}$
- 圆管流 $Re_D=\frac{UD}{\nu}$

#### 马赫数

$$Ma=\frac{|u|}{a}=\frac{流速}{音速}$$

- $Ma=0$:正规的不可压缩流动
    - 音速无限大（假设），扰动瞬时传播
    - 抛物型Navier-Stokes方程
- $0<Ma<0.3$:“弱”可压缩流动
    - 小和中等梯度亚音速流
    - 密度变化不超过5%

### 层流

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol12.png?raw=true){width=400 align=right}

- 求解NS方程
    - 针对低雷诺数情况
    - 瞬态或稳态求解器
    - 不可压缩或可压缩（$Ma<0.3$）
- 可以切换到湍流模型
- 可以切换至蠕动流
    - 忽略惯性项
- 定义参考压力水平（默认为:$1[atm]$）

