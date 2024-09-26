## SLR分析基本思想

对项目集$I$有

$$\begin{cases}
    A_1\to \alpha_1\cdot a_1\beta_1\\
    A_2\to \alpha_2\cdot a_2\beta_2\\
    \dots\\
    A_m\to \alpha_m\cdot a_m\beta_m\\
    B_1\to \gamma_1\\
    B_2\to \gamma_2\\
    \dots\\
    B_n\to \gamma_n
\end{cases}$$

如果集合$\{a_1, a_2, …, a_m\}$和$FOLLOW(B_1), FOLLOW(B_2),…,FOLLOW(B_n)$两两不相交，则项目集I中的冲突可以按以下原则解决： 

设$a$是下一个输入符号

1. 若$a\in \{a_1,a_2,\dots,a_m\}$，则移进a
2. 若$a\in FOLLOW(B_i)$，则用产生式$B_i\to\gamma_i$归约
3. 否则报错

构造G'的规范LR(0)项集族C = { I0, I1, … , In}。

根据$I_i$构造得到状态$i$。状态$i$的句法分析动作按照下面的方法决定：

```
if A→α·aβ∈Ii and GOTO( Ii , a )=Ij then ACTION[ i, a ]=sj
if A→α.Bβ∈Ii and GOTO( Ii , B )=Ij then GOTO[ i, B ]=j 
if A→α·∈Ii且A ≠ S' then for \forall a∈FOLLOW(A) do 
    ACTION[ i, a ]=rj （j是产生式A→α的编号）
if S'→S·∈Ii then ACTION [ i , $ ]=acc;
```

没有定义的所有条目都设置为“error”。
