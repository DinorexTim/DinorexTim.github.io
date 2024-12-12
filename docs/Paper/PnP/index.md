## SCI问题数学形式

考虑B帧的视频$X\in R^{n_x\times n_y\times B}$，根据掩码$C\in R^{n_x\times n_y\times B}$被调制为$Y\in R^{n_x\times n_y}$

可以被表示为

$$Y=\sum_{b=1}^B C_b \odot X_b + Z$$

其中C位掩码，X为B帧视频，z为噪声，亦可表达为

$$y=Hx+z$$

其中$y=\text{Vec}(Y)\in R^{n_xn_y}$，$z=\text{Vec}(Z)\in R^{n_xn_y}$

$$x=\text{Vec}(X)=[\text{Vec}(X_1)^T,\text{Vec}(X_2)^T,\cdots,\text{Vec}(X_B)^T]^T$$

H为稀疏传感矩阵，$H\in R^{n_xn_y\times n_xn_yB}$，是对角矩阵的串联

$$H=[D_1\cdots, D_B]$$

其中$D_b = \text{diag}(\text{Vec}(C_b))\in R^{n_xn_y\times n_xn_y}$

> 对于彩色视频，常用的拜耳模式传感器捕获数据具有RGGB通道，首先需要分别恢复4个通道，然后在重建的视频中demosaic

## PnP-ADMM

SCI反演问题可以建模为

$$\hat{x}=\argmin_{x} f(x)+\lambda g(x)$$

> f(x)为损失函数，即$||y-Hx||^2_2$，g(x)为正则项，即$||x||_1\leq 1$

### 回顾PnP-ADMM

使用ADMM框架，引入辅助参数v，将无约束优化转化为

$$(\hat{x},\hat{v})=\argmin_{x,v} f(x)+\lambda g(v)\quad x=v$$

最小化问题可以通过求解如下子问题解决

$$\begin{align}
    x^{(k+1)}=\argmin_{x} f(x)+ \frac{\rho}{2}||x-(v^{(k)}-\frac{1}{\rho}u^{(k)})||^2_2\\
    v^{(k+1)}=\argmin_{v} \lambda g(v)+\frac{\rho}{2}||v-(x^{(k)}+\frac{1}{\rho}u^{(k)})||^2_2\\
    u^{(k+1)} = u^{(k)} + ρ(x^{(k+1)} − v^{(k+1)}),
\end{align}$$

> f(x)通常为二次形式，式1会有多解，在PnP-ADMM中，式2会被现成的去噪算法替代，得到:$v^{(k+1)}=D_\sigma (x^{(k)}+\frac{1}{\rho}u^{(k)})$
>
> $D_\sigma$表示降噪器，$\sigma$表示假设的高斯白噪声标准偏差
>
> 在[Plugand-play ADMM for image restoration: Fixed-point convergence and applications](https://arxiv.org/abs/1605.01710)中作者提出，使用$\rho_{k+1}=\gamma_k\rho_k$更新迭代$\rho$，并且为降噪器设置$\sigma_k=\sqrt{\lambda/\rho_k}$。这样可定义一个有界去噪器，并且可证明PnP-ADMM不动点收敛

#### 有界去噪器

令有界去噪器$D_\sigma$是一个函数，对于任何输入$x\in R^n$，有

$$\frac{1}{n}||D_\sigma(x)-x||^2_2\leq \sigma^2 C$$

> C为某一常数

###  PnP-ADMM for SCI

PnP-ADMM算法的目标函数f(x)为

$$f(x)=\frac{1}{2} ||y-H x||^2_2$$

> 所有像素都被正则化至[0,1]区间

#### 引理1

SCI中，损失函数f(x)具有有界梯度，即$||\nabla f(x)||_2\leq B||x||_2$

