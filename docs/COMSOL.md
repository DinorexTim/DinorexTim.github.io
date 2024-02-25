[COMSOL快速教程](https://cn.comsol.com/video/basics-comsol-multiphysics-18-minutes)

[COMSOL使用教程(PDF)](https://cdn.comsol.com/translated-documentation/cn/5.3/COMSOLMultiphysics%E7%AE%80%E4%BB%8B.pdf)

## COMSOL多物理场的工作流程

|定义问题|初始化问题|几何|材料属性|边界条件|网格|求解|后处理|优化|
|-|-|-|-|-|-|-|-|-|
|定义需要<br>求解的问题|初始化模型|绘制或导入CAD|定义求解域|设定边界条件|网格划分|求解|后处理和报告|优化修改|

## 定义问题：热微执行器

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

## 几何建模

### 几何体素

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol2.png?raw=true){width=200 align=right}

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol3.png?raw=true){width=150}

每个对象包含“域”、“边界”、“边”、“点”属性

### 几何操作

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol4.png?raw=true){width=200}

#### 阵列

用于在x,y,z方向上生成相同的几何体素

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol5.png?raw=true){width=400}

- 阵列操作选项

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol6.png?raw=true){width=400}

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol7.png?raw=true){width=400}

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/comsol8.png?raw=true){width=400}

### 几何模型定义的逻辑

**几何体素的定义>>变换操作>>逻辑操作**
