## 什么是Machine learning

Machine learning $\approx$ Looking for function

**“机器学习”实质就是帮助人类寻找人类无法写出的函数**

如果机器学习的任务是寻找一个函数，那么深度学习的意思是使用类神经网络寻找一个函数

这个类神经网络可以包含各种各样的输入：比如向量、矩阵、一段序列（文字、语音等等）；输出可以是：数值(regression)、做出选择(classification)等等

实际上机器学习领域中还有Structured Learning的任务，让机器去“创造”一个有结构的事物

## 如何让机器去寻找函数？

**需要先寻找样本（数据），每获得一份数据就给它做上标记(label)，用于训练模型**

但是实际上的标记工作量十分巨大，假如要做一套分类模型的训练（比如识别猫和狗、识别轿车和自行车...），为每个任务寻找对应的数据集是十分耗时的

*那么如何解决？*

## 自监督学习(Self Supervise Learning)

**在模型训练之前，让模型练成基本功**

在训练前进行预训练(Pre-train)，这样在进行特定目的的训练时，可以更加高效地学习

*那么如何进行预训练？*

只需要准备大量**未标注数据**，让机器去学习基本的“知识”

比如：仅仅是将一张图像和它的一张镜像翻转后的图像投喂给机器，让其明白这两张图像实质是一样的

### 一个类比：OS 与 App

当下的应用开发门槛降低了许多，软件开发工程师并不需要从头开发，去和硬件打交道，因为真正复杂的工作已经交给操作系统去完成了。

一个好的Pre-train model就好比一个优秀的操作系统，当要开发新的训练任务时，其难度会大大降低。在众多预训练模型中，比较知名的有`BERT`模型(340M参数)

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-1.png?raw=true){width=450}
<figcaption>贝尔托特是你吗（</figcaption>
</figure>

## 生成式对抗网络(Generative adversarial network)

对于一个自监督学习，假如你要收集大量的**成对的**数据（输入和对应的输出），但是Gan允许你只需有收集到大量的输入数据和大量的输出数据而**无需配对**

<details>
    <summary>Gan相关论文</summary>

<a href="https://arxiv.org/abs/1804.00316">https://arxiv.org/abs/1804.00316</a><br>

<a href="https://arxiv.org/abs/1812.09323">https://arxiv.org/abs/1812.09323</a><br>

<a href="https://arxiv.org/abs/1904.04100">https://arxiv.org/abs/1904.04100</a><br>

<a href="https://arxiv.org/abs/2105.11084">https://arxiv.org/abs/2105.11084</a><br>

</details>

## 强化学习(Reinforcement learning)

**解决不知道如何标注数据的情况**

假如想让机器学会下围棋，但是问题在于人类自己也不清楚在目前棋子排列的情况下，下一步到底要怎么走。

但是，人类可以定义“好”与“坏”，即赢得比赛为“good”，输了比赛判定为"bad"，那么就可以使用强化学习的方法

## 异常检测

假如真的训练了一个可以进行分类猫狗的模型，在实际运用过程中，当输入了一个完全不同于训练数据种类的生物（比如老鼠），模型需要具备回答“我不知道”的能力

## 可解释性AI

当模型实现了分类的能力后，还需要它具备解释这样**分类的原因**

## 模型攻击

假设现在有一个图像识别的模型，对于一张正常的猫的图片，它能够正确地识别，但是在这张图片里面加入一些特定的噪点后，会导致模型识别出来的生物与猫大相径庭

![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-2.png?raw=true){width=450}

## 领域自适应(Domain Adaption)

假设对于一个手写识别模型，假设训练数据全是黑白的手写字体，那么在实际运用中即使输入的是“彩色手写字”，模型也应该理解这份手写字体

## 实例：预测Youtube频道观看人数

假如现在频道主想根据过往的播放信息，去预测未来某一天特定的观看人数，那么如何去找到想要的函数？

分为三个步骤

### 1.猜测含未知参数的函数

令第二天待预测的观看人数为$y$，$x$为今天的观看人数

在没有任何知识储备的情况下，可以**假设**一个函数为$y=b+wx_1\quad 其中w和b都是未知参数，需要从数据中学习$

我们将这个带有未知参数的函数叫做“**模型**”(`model`)，$x_1$称为`feature`，$w$叫做`weight`，$b$称为`bias`

### 2.定义损失函数Loss

`Loss`是一个自定义的函数$L(b,w)$，这个函数内的参数是`model`的参数b,w

`Loss`输出的值表示“预测值与实际的偏差”

实际的正确值称为`label`

当计算出了一系列的weight和bias后，可以得到一个**误差曲面**`Error Surface`

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-3.png?raw=true){width=450}
</figure>

### 3.优化(Optimization)

寻找一组$w$与$b$，使得$Loss$值最小，即

$$w^*,b^*=arg\min_{w,b} L$$

目前可以使用**梯度下降法**(Gradient Descent)进行优化

为了简化起见，假设未知参数仅有w，当w取值不同时，对应的Loss值也不一样

随机选择一个初始点$w^0$，计算$\frac{\partial L}{\partial w}|_{w=w^0}$，当计算出的偏导数为负数，那么增加w的值，否则减小w的值，使用$w^1\leftarrow w^0-步幅$反复进行计算，当w的取值越靠近Loss最小值对应的$w^*$，“步幅”会变得越来越小

增加或减少的“步幅”可以用$\eta\frac{\partial L}{\partial w}|_{w=w^0}$表示，其中$\eta$表示**学习速率**(learning rate)，该参数是自定义的。

> 在机器学习里面，像$\eta$这样手动设置的参数称为**超参数**`hyperparameter`

梯度下降法存在一个非常明显的问题：随机取得的初始点在经过迭代后，很有可能会陷入**局部最低点**无法跳出，导致无法求得真正的**全局最低点**。但是在实际的深度学习中，梯度下降法的“局部最低点”问题实际上并非其真正的“痛点”

#### 小结

优化步骤

- 随机取样$w^0,b^0$
- 进行迭代，达到设定的迭代次数上限后结束

$$\begin{align*}
    &w^1\leftarrow w^0-\eta\frac{\partial L}{\partial w}|_{w=w^0}\\
    &b^1\leftarrow b^0-\eta\frac{\partial L}{\partial b}|_{b=b^0}
\end{align*}$$

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-4.png?raw=true){width=450}
</figure>

### 4.预测效果分析和模型修改

在学习了2017年-2020年的观看数据后，模型预测了2021年每天的观看人数，将模型预测值和实际的值进行对比得到下图

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-5.png?raw=true){width=450}
</figure>

从上面的图像可以看出的是，观看次数呈现出一定的“周期性”，大概是7天为一个周期，在周末时间段观看人数会明显降低（~~谁周末还看深度学习~~），所以之前的一次函数模型还有可以修改的空间

> **对模型的修改一般都基于对问题理解的改变**。在一开始的时候，对问题完全没有理解，所以会胡乱猜测一个一次函数作为预测模型，而这样胡乱猜测的模型一般的预测效果也不会很好

新模型可以基于周期性规律，考虑前7天对于未来一天观看数量的影响，修改为

$$y=b+\sum_{j=1}^{7}w_jx_j$$

经实验证实增加考虑的天数确实有助于降低损失函数的数值，但是随着考虑天数的增加模型的进步会愈发不明显

## 线性模型局限与改进

上述实例中的模型可以统称为**线性模型**，但是对于大部分要预测的对象来说，这个模型限制过大，因为无论怎样调整模型的$w$和$b$都只能得到一条“直线”，这种模型本身的限制称为`Model Bias`

*如何突破线性模型的限制？*

**写出一个更复杂、更具弹性的模型**

从分段线性函数开始：

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-6.png?raw=true){width=450}
</figure>

对于单一的线性函数，永远不可能得到图中红色的函数图像，经过观察，红色的折线其实可以拆分为一个常数值与“蓝色函数”的和

![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-8.png?raw=true){width=200 align=right}

![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-7.png?raw=true){width=200 align=right}

不管对于什么样的分段线性函数折线，都可以用一个常数值与“蓝色函数”的和组成。即使考虑函数图像的不是分段线性函数（比如指数函数），也可以先在曲线上去若干点然后讲这些点相连近似处理为分段线性函数，也就是说：只要有足够的“蓝色函数”求和相加，或许就可以得到任何的连续曲线

*那么如何写出“蓝色函数”的表达式呢？*

使用**S型函数**(Sigmoid Function)逼近“蓝色函数”，其表达式为

$$y=c\cdot sigmoid(b+wx_1)=c\frac{1}{1+e^{-(b+wx_1)}}$$

修改$w,b,c$可以调整S型函数图像，c调整高度，b左右平移，w调整倾斜程度

再回头看红色的分段线性函数，可以得到表达式

$$\begin{align}
    y=b+\sum_i c_i\cdot sigmoid(b_i+w_ix_1)
    \\=b+\sum_i c_i\cdot sigmoid(b_i+\sum_j w_{ij}x_j)
\end{align}$$

这样我们就可以写出非常有“弹性”的函数

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-9.png?raw=true){width=400}
</figure>

上面的式子还可以进一步变形，修改为矩阵相乘的形式

$$y=b+\mathbf{c}^T\sigma(\mathbf{b}+\mathbf{W}\mathbf{x})$$

其中x为`feature`,$\vec{W},\vec{b},\vec{c}^T,b$都是未知参数

将未知参数“拉伸”，可以得到一个长的向量$\mathbf{\theta}=\left[\begin{matrix}\theta1\\\theta2\\theta3\\\dots\end{matrix}\right]$，其中$\theta_i$表示一个数值

当参数越来越多时，为了简化表达，将损失函数定义为$L(\theta)$

那么对应的优化步骤也目标也成了$\theta^*=arg\min_{\theta} L$

在优化开始时，随机挑选一个初始值$\theta_0$

根据下式进行迭代

$$\theta^{i+1}=\theta_i-\left[\begin{matrix}
\eta\frac{\partial L}{\partial \theta_1}|_{\theta=\theta^i}\\
\eta\frac{\partial L}{\partial \theta_2}|_{\theta=\theta^i}\\
\dots
\end{matrix}\right]$$

简写为$\theta^{i+1}=\theta^0-\eta\nabla L(\theta^i)=\theta^0-\eta \mathbf{g}$

### 更常见的优化操作（批处理）

比起使用所有参数进行损失函数的计算，使用批处理更为常见

将$\theta$随机分为一个一个一个`batch`，只拿其中的第一份batch进行损失函数的计算，在这里将计算出的结果命名为$L^1$，根据这个$L^1$来计算$\theta$的梯度，进而更新参数，再拿出第二份batch重复上述操作，以此类推，使用了所有的batch进行了一次优化，叫做一个`epoch`，更新一次的操作叫做`update`

> 一次epoch的训练，实际的更新次数不确定的，因为batch的大小是手动设定的

## 更多模型的变形

“蓝色函数”实际上可以由两个**线性整流函数**`Rectified Linear Unit`(ReLU)构成

ReLU的表达式为$c\cdot max(0,b+wx_1)$

<figure markdown>
![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/ml0-10.png?raw=true){width=400}
</figure>