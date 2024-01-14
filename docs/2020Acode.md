# code

## Q1

### Q1.py

```python
import pandas as pd
from getFurnacetemperature import *

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

solder_thickness = 0.015
delta_t = 0.5

def Matrix_A(m, r, h): # 计算左侧的方形矩阵
    delta_z = solder_thickness / m
    A = np.diag([2 * (1 + r)] * (m + 1)) + np.diag([-r] * m, k=1) + np.diag([-r] * m, k=-1)
    A[0][0] = 1 + h * delta_z
    A[0][1] = -1
    A[-1][-2] = -1
    A[-1][-1] = 1 + h * delta_z
    return A

def Matrix_B(m, r): # 计算右侧的方形矩阵
    B = np.diag([2 * (1 - r)] * (m + 1)) + np.diag([r] * m, k=1) + np.diag([r] * m, k=-1)
    B[0][:] = 0
    B[-1][:] = 0
    return B

def CN(m = 100, # 焊接区域厚度的切割份数
       a = np.array([6.683e-4, 8.076e-4, 9.744e-4, 8.493e-4, 5.287e-4]), # 各阶段的a
       h = np.array([24987, 1432, 827.9, 654.8, 1338]), # 各阶段的h
       v = 70/60,# 速度
       draw = 0):# 是否绘图
    delta_z = solder_thickness / m
    r = a * a * delta_t / (delta_z * delta_z)
    # 初值
    right_u = np.array([25] * (m+1))
    time = 0
    t = np.array([0])
    u = np.array([25])
    # 小温区1-5
    while (time * v) < (front_len + 5*furance_len + 4.5*interval_len):
        # 计算右侧的单列矩阵
        right_b = np.array([.0] * (m + 1))
        right_b[0] = h[0] * getFurnacetemperature((time + delta_t) * v) * delta_z
        right_b[-1] = h[0] * getFurnacetemperature((time + delta_t) * v) * delta_z
        left_u = np.linalg.inv(Matrix_A(m, r[0], h[0])) @ (Matrix_B(m, r[0],) @ right_u + right_b)
        time = time + delta_t
        t = np.append(t, time)
        u = np.append(u, left_u[int(m / 2)])
        right_u = left_u
    # 小温区6
    while (time * v) < (front_len + 6*furance_len + 5.5*interval_len):
        # 计算右侧的单列矩阵
        right_b = np.array([.0] * (m + 1))
        right_b[0] = h[1] * getFurnacetemperature((time + delta_t) * v) * delta_z
        right_b[-1] = h[1] * getFurnacetemperature((time + delta_t) * v) * delta_z
        left_u = np.linalg.inv(Matrix_A(m, r[1], h[1])) @ (Matrix_B(m, r[1],) @ right_u + right_b)
        time = time + delta_t
        t = np.append(t, time)
        u = np.append(u, left_u[int(m / 2)])
        right_u = left_u
    # 小温区7
    while (time * v) < (front_len + 7*furance_len + 6.5*interval_len):
        # 计算右侧的单列矩阵
        right_b = np.array([.0] * (m + 1))
        right_b[0] = h[2] * getFurnacetemperature((time + delta_t) * v) * delta_z
        right_b[-1] = h[2] * getFurnacetemperature((time + delta_t) * v) * delta_z
        left_u = np.linalg.inv(Matrix_A(m, r[2], h[2])) @ (Matrix_B(m, r[2],) @ right_u + right_b)
        time = time + delta_t
        t = np.append(t, time)
        u = np.append(u, left_u[int(m / 2)])
        right_u = left_u
    # 小温区8-9
    while (time * v) < (front_len + 9*furance_len + 8.5*interval_len):
        # 计算右侧的单列矩阵
        right_b = np.array([.0] * (m + 1))
        right_b[0] = h[3] * getFurnacetemperature((time + delta_t) * v) * delta_z
        right_b[-1] = h[3] * getFurnacetemperature((time + delta_t) * v) * delta_z
        left_u = np.linalg.inv(Matrix_A(m, r[3], h[3])) @ (Matrix_B(m, r[3],) @ right_u + right_b)
        time = time + delta_t
        t = np.append(t, time)
        u = np.append(u, left_u[int(m / 2)])
        right_u = left_u
    # 小温区10-11
    while (time * v) <= (2*front_len + 11*furance_len + 10*interval_len):
        # 计算右侧的单列矩阵
        right_b = np.array([.0] * (m + 1))
        right_b[0] = h[4] * getFurnacetemperature((time + delta_t) * v) * delta_z
        right_b[-1] = h[4] * getFurnacetemperature((time + delta_t) * v) * delta_z
        left_u = np.linalg.inv(Matrix_A(m, r[4], h[4])) @ (Matrix_B(m, r[4],) @ right_u + right_b)
        time = time + delta_t
        t = np.append(t, time)
        u = np.append(u, left_u[int(m / 2)])
        right_u = left_u
    if(draw):
        return np.array([t, u])
    else:
        sum=0
        tmp=0
        experiment_temperature=np.array(pd.read_csv('fujian.csv'))
        for index in range(experiment_temperature.T[1].size):
            while np.array([t,u])[0][tmp]<19:
                tmp+=1
            sum+=np.abs((np.array([t, u])[1][tmp+index]-experiment_temperature[index][1]))
        return sum

def pso():
    num_to_optimize=5
    N=20 # 种群个数
    d=1 # 维度
    cnt_max=20 # 最大迭代次数
    xlimit_a=[0.0001,0.001] # a位置界限
    vlimit_a=[-0.00002,0.00002] # a速度界限
    
    xlimit_h=[0,10000] # h位置界限
    vlimit_h=[-800,800] # h速度界限
    
    w=0.8 # 惯性系数
    c1=0.5 # 个体学习参数
    c2=0.5 # 全局学习系数

    # 初始化种群
    x_a=np.array([
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20)
    ])
    x_h=np.array([
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20)
    ])
    v_a=np.array([
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20)
    ])
    v_h=np.array([
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20)
    ])
    # x_a=np.full((num_to_optimize,len(np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20))),np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20))
    # x_h=np.full((num_to_optimize,len(np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20))),np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20))
    # # 初始化个体速度
    # v_a=np.full((num_to_optimize,len(np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20))),np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20))
    # v_h=np.full((num_to_optimize,len(np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20))),np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20))

    # 个体历史最优
    individual_best=np.zeros(x_a[0].size)
    for index in range(individual_best.shape[0]):
        individual_best[index]=np.copy(CN(100,x_a.T[index],x_h.T[index],70/60))
    # 个体历史最优位置
    individual_best_a=np.copy(x_a)
    individual_best_h=np.copy(x_h)
    # 全局最优解
    global_best=1000000
    # 全局历史最优位置
    global_best_a=np.zeros(num_to_optimize)
    global_best_h=np.zeros(num_to_optimize)

    # 初始化全局最优
    for index in range(x_a[0].size):
        temp=CN(100,x_a.T[index][:],x_h.T[index][:],70/60)
        if(global_best > temp):
            global_best_a=x_a.T[index][:]
            global_best_h=x_h.T[index][:]
            global_best=temp
            
    # 进行迭代
    for cnt in range(cnt_max):
        print("*******")
        print("迭代次数: ",cnt+1)
        print("*******")
        r1=np.full(num_to_optimize,np.random.rand(1))
        r2=np.full(num_to_optimize,np.random.rand(1))
        for index in range(x_a[0].size):
            # 更新a,v速度
            va_temp=w*v_a.T[index] + c1*r1*(individual_best_a.T[index]-x_a.T[index]) + c2*r2*(global_best_a-x_a.T[index])
            vh_temp=w*v_h.T[index] + c1*r1*(individual_best_h.T[index]-x_h.T[index]) + c2*r2*(global_best_h-x_h.T[index])
            if not ((va_temp >= vlimit_a[0]).all() and (va_temp <= vlimit_a[1]).all()):
                for pos in range(va_temp.size):
                    if va_temp[pos]>vlimit_a[1]:
                        va_temp[pos]=vlimit_a[1]
                    else:
                        va_temp[pos]=vlimit_a[0]
            v_a.T[index]=va_temp
            if not ((vh_temp >= vlimit_h[0]).all() and (vh_temp <= vlimit_h[1]).all()):
                for pos in range(vh_temp.size):
                    if vh_temp[pos]>vlimit_a[1]:
                        vh_temp[pos]=vlimit_h[1]
                    else:
                        vh_temp[pos]=vlimit_h[0]
            v_h.T[index]=vh_temp
            # 更新a,v位置
            if (x_a.T[index]+v_a.T[index]>=xlimit_a[0]).any() and (x_a.T[index]+v_a.T[index]<=xlimit_a[1]).any() and (x_h.T[index]+v_h.T[index]>=xlimit_h[0]).any() and (x_h.T[index]+v_h.T[index]<=xlimit_h[1]).any():
                x_a.T[index] = x_a.T[index]+v_a.T[index]
                x_h.T[index] = x_h.T[index]+v_h.T[index]
                # 更新个体历史最优
                tmp = CN(100,x_a.T[index][:],x_h.T[index][:],70/60)
                if individual_best[index] > tmp:
                    individual_best_a.T[index] = x_a.T[index]
                    individual_best_h.T[index] = x_h.T[index]
                    individual_best[index] = tmp
                # 更新全局历史最优
                if global_best > tmp:
                    global_best_a = x_a.T[index]
                    global_best_h = x_h.T[index]
                    global_best = tmp
            print("a:",global_best_a)
            print("h",global_best_h)
            print(global_best)
            
    return global_best_a,global_best_h,global_best

if __name__ == "__main__":
    a,h,globalbest=pso()
    test = CN(150, a, h, 70/60, 1)
    test = test.T
    u = pd.read_csv('fujian.csv')
    u = np.array(u)

    plt.figure(figsize=(14, 6))
    plt.subplots_adjust(wspace=0.5)
    plt.subplot(121)
    plt.plot(test[38:-2, 0], test[38:-2, 1], label='实验温度')
    plt.plot(u[:, 0],u[:, 1], label='模型温度')
    plt.legend()
    plt.subplot(122)
    delta = test[38:-1, 1] - u[:, 1]
    F = sum(delta*delta)
    plt.plot(u[:, 0], delta, label='F={}'.format(F))
    plt.legend()
    plt.show()
```

### getFurnacetemperature.py

```python
import pylab as plt
import numpy as np

furance_len = 30.5  # 小温区长度
interval_len = 5  # 间隙长度
front_len = 25  # 炉前区域

def getFurnacetemperature(x, temp=[175, 195, 235, 255]):
    # 炉外区域
    if x <= 0:
        return 25
    # 炉前区域
    elif x <= front_len:
        return 25 + (temp[0]-25)/25 * x
    # 小温区1-5
    elif x <= front_len + 5*furance_len+4*interval_len:
        return temp[0]
    # 过度区域
    elif x <= front_len + 5*(furance_len+interval_len):
        return temp[0] + ((temp[1] - temp[0])/interval_len) * (x-(25 + 5*furance_len+4*interval_len))
    # 小温区6
    elif x <= front_len + 6*furance_len+5*interval_len:
        return temp[1]
    # 过度区域
    elif x <= front_len + 6*(furance_len+interval_len):
        return temp[1] + ((temp[2] - temp[1])/interval_len) * (x-(25 + 6*furance_len+5*interval_len))
    # 小温区7
    elif x <= front_len + 7*furance_len + 6*interval_len:
        return temp[2]
    # 过度区域
    elif x <= front_len + 7*(furance_len+interval_len):
        return temp[2] + ((temp[3] - temp[2])/interval_len) * (x-(25 + 7*furance_len + 6*interval_len))
    # 小温区8-9
    elif x <= front_len + 9*furance_len+8*interval_len:
        return temp[3]
    # 小温区10-11
    elif x <= front_len + 9*(furance_len+interval_len):
        return temp[3] + ((25 - temp[3])/interval_len) * (x-(25 + 9*furance_len+8*interval_len))
    # 炉外区域
    else:
        return 25

if __name__ == "__main__":
    x = np.arange(0, 2*front_len + 11*furance_len + 10*interval_len, 0.1)
    y = np.array([])
    for v in x:
        y = np.append(y, getFurnacetemperature(v))
    plt.plot(x, y, label='炉内温度')
    plt.show()

```

## Q2

## Q3

## Q4