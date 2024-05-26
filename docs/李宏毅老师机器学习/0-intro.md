## 什么是Machine learning

Machine learning $\approx$ Looking for function

**“机器学习”实质就是帮助人类寻找人类无法写出的函数**

如果机器学习的任务是寻找一个函数，那么深度学习的意思是使用类神经网络寻找一个函数

这个类神经网络可以包含各种各样的输入：比如向量、矩阵、一段序列（文字、语音等等）；输出可以是：数值(regression)、做出选择(classification)等等

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
