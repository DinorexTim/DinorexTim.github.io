$\epsilon-NFA$：对NFA进行扩展，在不输入任何字符的情况下（空串$\epsilon$），可以**自发地**发生状态转移

- 可简化NFA构造
- $\epsilon-NFA$明确定义了至少一个空转移的NFA
- 在状态表里面多了对应于$\epsilon$的一列

## 定义

带空转移非确定有穷自动机($\epsilon-NFA$)A为五元组$A=(Q,\Sigma,\delta,q_0,F)$

1. $Q$: 有穷状态集；
2. $\Sigma$: 有穷输入符号集或字母表；
3. $\delta$: $Q\times (\Sigma\cup\epsilon)\to2^Q$ 状态转移函数；
4. $q_0\subseteq Q$: 初始状态
5. $F\subseteq Q$: 终结状态集或接受状态集

例：$L=\{w\in\{0,1\}^*|w倒数3个字符至少有一个是1\}$的$\epsilon-NFA$

![img](https://github.com/DINOREXNB/DINOREXNB.github.io/blob/main/docs/images/xsyy5-1.png?raw=true){width=400}