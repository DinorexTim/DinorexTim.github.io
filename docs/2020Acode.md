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
        experiment_temperature=np.array(pd.read_csv('附件.csv'))
        for index in range(experiment_temperature.T[1].size):
            while np.array([t,u])[0][tmp]<19:
                tmp+=1
            sum+=(np.array([t, u])[1][tmp+index]-experiment_temperature[index][1])**2
        return sum

def pso():
    num_to_optimize=5
    N=20 # 种群个数
    cnt_max=40 # 最大迭代次数
    xlimit_a=[0.0001,0.001] # a位置界限
    vlimit_a=[-0.0002,0.0002] # a速度界限
    
    xlimit_h=[3000,12000] # h位置界限
    vlimit_h=[-1300,1300] # h速度界限

    # 初始化种群
    x_a=np.array([
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=N),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=N),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=N),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=N),
        np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=N)
    ])
    x_h=np.array([
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=N),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=N),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=N),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=N),
        np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=N)
    ])
    v_a=np.array([
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=N),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=N),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=N),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=N),
        np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=N)
    ])
    v_h=np.array([
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=N),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=N),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=N),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=N),
        np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=N)
    ])

    w=np.linspace(1.1,0.3,cnt_max) # 惯性系数
    w=np.append(w,np.linspace(0.6,0.6,20))
    cnt_max+=20
    c1=0.6 # 个体学习参数
    c2=0.6 # 全局学习系数
    
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
        temp=CN(100,x_a.T[index],x_h.T[index],70/60)
        if(global_best > temp):
            global_best_a=np.copy(x_a.T[index])
            global_best_h=np.copy(x_h.T[index])
            global_best=temp
            
    # 进行迭代
    for cnt in range(cnt_max):
        print("*******")
        print("迭代次数: ",cnt+1)
        print("*******")
        r1=np.array(np.random.rand(num_to_optimize))
        r2=np.array(np.random.rand(num_to_optimize))
        for index in range(x_a[0].size):
            # 更新a,v速度
            va_temp=np.copy(w[cnt]*v_a.T[index] + c1*r1*(individual_best_a.T[index]-x_a.T[index]) + c2*r2*(global_best_a-x_a.T[index]))
            vh_temp=np.copy(w[cnt]*v_h.T[index] + c1*r1*(individual_best_h.T[index]-x_h.T[index]) + c2*r2*(global_best_h-x_h.T[index]))
            if not ((va_temp >= vlimit_a[0]).all() and (va_temp <= vlimit_a[1]).all()):
                for pos in range(va_temp.size):
                    if va_temp[pos]>vlimit_a[1]:
                        va_temp[pos]=vlimit_a[1]
                    elif va_temp[pos]<vlimit_a[0]:
                        va_temp[pos]=vlimit_a[0]
            v_a.T[index]=np.copy(va_temp)
            if not ((vh_temp >= vlimit_h[0]).all() and (vh_temp <= vlimit_h[1]).all()):
                for pos in range(vh_temp.size):
                    if vh_temp[pos]>vlimit_h[1]:
                        vh_temp[pos]=vlimit_h[1]
                    elif vh_temp[pos]<vlimit_h[0]:
                        vh_temp[pos]=vlimit_h[0]
            v_h.T[index]=np.copy(vh_temp)
            # 更新a,v位置
            if (x_a.T[index]+v_a.T[index]>=xlimit_a[0]).any() and (x_a.T[index]+v_a.T[index]<=xlimit_a[1]).any() and (x_h.T[index]+v_h.T[index]>=xlimit_h[0]).any() and (x_h.T[index]+v_h.T[index]<=xlimit_h[1]).any():
                # 更新个体历史最优
                x_a.T[index] = np.copy(x_a.T[index]+v_a.T[index])
                x_h.T[index] = np.copy(x_h.T[index]+v_h.T[index])
                tmp = CN(100,x_a.T[index],x_h.T[index],70/60)
                if individual_best[index] > tmp: # 只有优于个体历史最佳时才进行更新
                    individual_best_a.T[index] = np.copy(x_a.T[index])
                    individual_best_h.T[index] = np.copy(x_h.T[index])
                    individual_best[index] = tmp
                # 更新全局历史最优
                if global_best > tmp:
                    print("*******")
                    print("发现全局更优解:",tmp)
                    print("*******")
                    global_best_a = np.copy(x_a.T[index])
                    global_best_h = np.copy(x_h.T[index])
                    global_best = tmp
         
            print("a:",global_best_a)
            print("h:",global_best_h)
            print(global_best)   
    return global_best_a,global_best_h,global_best

if __name__ == "__main__":
    a,h,globalbest=pso()
    test = CN(100, a, h, 70/60, 1)
    test = test.T
    u = pd.read_csv('附件.csv')
    u = np.array(u)

    plt.figure(figsize=(14, 6))
    plt.subplots_adjust(wspace=0.5)
    plt.subplot(121)
    plt.plot(test[38:-2, 0], test[38:-2, 1], label='模型温度')
    plt.plot(u[:, 0],u[:, 1], label='实验温度')
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

### Q2.py
```python
from Q2peakTemperature import *
from Q2slope import *
from Q2temperature150To190 import *
from Q2temperature217 import *

v_result=np.zeros(4)

# 最大斜率
max_slope=3
# 传送带速度范围
v_range=[65/60,100/60]

# 当前速度
mid=(v_range[0]+v_range[1])/2
high=v_range[1]
low=v_range[0]
# 最大迭代次数
cnt_max=15

# 已知a,h
a= np.array([0.00068095, 0.00080617 ,0.00091174 ,0.00069781, 0.00050876])
h= np.array([9983.39272247, 4681.68896512, 9237.15138045, 8110.32864819 ,5665.62009518])

def dichotomy_slope(mid):
    cnt=0
    while cnt<cnt_max:
        print("迭代次数:",cnt+1)
        if max_slope == Maxslope(mid):
            return mid
        if max_slope > Maxslope(mid):# 加判断条件
            mid=(mid+high)/2
        else:
            mid=(mid+low)/2
        cnt+=1
    return mid

def dichotomy_peak(mid):
    cnt=0
    while cnt<cnt_max:
        print("迭代次数:",cnt+1)
        if PeakTemperature(mid):# 加判断条件
            mid=(mid+high)/2
        else:
            mid=(mid+low)/2
        cnt+=1
    return mid

def dichotomy_217(mid):
    cnt=0
    while cnt<cnt_max:
        print("迭代次数:",cnt+1)
        if Temperature217(mid):# 加判断条件
            mid=(mid+high)/2
        else:
            mid=(mid+low)/2
        cnt+=1
    return mid

def dichotomy_150to190(mid):
    cnt=0
    while cnt<cnt_max:
        print("迭代次数:",cnt+1)
        if Temperature150To190(mid):# 加判断条件
            mid=(mid+high)/2
        else:
            mid=(mid+low)/2
        cnt+=1
    return mid

v_result[0]=dichotomy_slope(mid)
v_result[1]=dichotomy_peak(mid)
v_result[2]=dichotomy_217(mid)
v_result[3]=dichotomy_150to190(mid)

print(v_result)
```

### Q2slope.py

```python
from Q1 import *

def Maxslope(speed):
    maxslope=0
    a= np.array([0.00068095, 0.00080617 ,0.00091174 ,0.00069781, 0.00050876])
    h= np.array([9983.39272247, 4681.68896512, 9237.15138045, 8110.32864819 ,5665.62009518])
    ut=CN(100,a,h,speed,1)
    ut=ut.T
    for index in range(ut.T[0].size-1):
        if maxslope < np.abs(ut[index+1][1]-ut[index][1])/0.5:
            maxslope = np.abs(ut[index+1][1]-ut[index][1])/0.5
    return maxslope
```

### Q2peakTemperature.py

```python
from Q1 import *

def PeakTemperature(speed):
    a= np.array([0.00068095, 0.00080617 ,0.00091174 ,0.00069781, 0.00050876])
    h= np.array([9983.39272247, 4681.68896512, 9237.15138045, 8110.32864819 ,5665.62009518])
    ut=CN(100,a,h,speed,1)
    u = ut[1]
    if np.max(u) >= 240:
        return 1
    else:
        return 0

if __name__ == "__main__":
    a = PeakTemperature(np.array([1, 245, 3]))
    print(a)
```

### Q2temperature217.py

```python
from Q1 import *

def Temperature217(speed):
    a= np.array([0.00068095, 0.00080617 ,0.00091174 ,0.00069781, 0.00050876])
    h= np.array([9983.39272247, 4681.68896512, 9237.15138045, 8110.32864819 ,5665.62009518])
    ut=CN(100,a,h,speed,1)
    u = ut[1]
    a = u[u > 217]
    b = len(a)
    if b*0.5 >= 40:
        return 1
    else:
        return 0

if __name__ == "__main__":
    a = Temperature217(np.array([1, 245, 3, 255]))
    print(a)
```

### Q2temperature150To190.py

```python
from Q1 import *

def Temperature150To190(speed):
    a= np.array([0.00068095, 0.00080617 ,0.00091174 ,0.00069781, 0.00050876])
    h= np.array([9983.39272247, 4681.68896512, 9237.15138045, 8110.32864819 ,5665.62009518])
    ut=CN(100,a,h,speed,1)
    u = ut[1]
    diff_u = np.diff(u)
    a = u[1:][diff_u > 0]
    a = a[(a > 150) & (a < 190)]
    b = len(a)
    if b * 0.5 >= 60:
        return 1
    else:
        return 0


if __name__ == "__main__":
    a = Temperature150To190(np.array([[1,1,1,1,1,1],[1, 45,155, 160, 3, 255]]))
    print(a)
```
## Q3

## Q4