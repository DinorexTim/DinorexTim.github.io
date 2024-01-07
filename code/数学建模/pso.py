import numpy as np

N=20 # 种群个数
d=1 # 维度
cnt_max=2000 # 最大迭代次数
limit=[0,50] #位置界限
vlimit=[-3,3] # 速度界限
w=0.8 # 惯性系数
c1=0.5 # 个体学习参数
c2=0.5 # 全局学习系数

#目标函数
def func(x):
    return x*np.sin(x)*np.cos(2*x)-2*x*np.sin(3*x)+3*x*np.sin(4*x)

# 初始化种群
x=np.random.uniform(low=0, high=50, size=20)
# 初始化个体速度
v=np.random.uniform(low=-3, high=3, size=20)

# 个体历史最优
individual_best=np.copy(func(x))
# 个体历史最优位置
individual_bestx=np.copy(x)
#全局最优解
global_best=100
#全局历史最优位置
global_bestx=0

# 初始化全局最优
for index in range(x.size):
    if global_best>func(x[index]):
        global_best=func(x[index])
        global_bestx=x[index]

# 进行迭代
for cnt in range(cnt_max):
    r1=np.random.rand(1)
    r2=np.random.rand(1)
    for index in range(x.size):
        # 判断v是否在边界内
        v_temp=w*v[index] + c1*r1[0]*(individual_bestx[index]-x[index]) + c2*r2[0]*(global_bestx-x[index])
        if v_temp>=vlimit[0] and v_temp<=vlimit[1]:
            # 判断x是否在边界内
            v[index]=v_temp
        else:
            # 若超出界限，则取边界值
            if v_temp>vlimit[1]:
                v[index]=vlimit[1]
            else:
                v[index]=vlimit[0]
        if x[index]+v[index]>=limit[0] and x[index]+v[index]<=limit[1]:
            x[index]=x[index]+v[index]
            # 更新个体历史最优最优
            if individual_best[index]>func(x[index]):
                individual_best[index]=func(x[index])
                individual_bestx[index]=x[index]
            # 更新全局最优
            if global_best>func(x[index]):
                global_best=func(x[index])
                global_bestx=x[index]
        
# 输出最优解
print("最小值为:",global_best)
        