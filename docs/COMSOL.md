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

定义问题逻辑：

|定义分析目标|几何维度|确定所需物理场|确定多物理场耦合|
|-|-|-|-|
|获得执行器通电后的热变形情况|三维|电流<br>固体传热<br>固体力学|电磁热<br>热膨胀|
