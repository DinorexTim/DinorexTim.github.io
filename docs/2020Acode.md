# code

## Q1

### Q1.py

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint 
'''
heat equation
du/dt=a * d(du/dz)/dz
'''
# 附件温度数据
experiment_data=np.array([])

# 焊锡厚度
solder_thickness=0.15e-3

# 附件数据中各个温区温度
experiment_temperature=np.array(pd.read_csv('附件.csv'))

# 求解实验附件炉内温度(以炉前区域末端为起始坐标点)
def getFurnacetemperature_exp(x):
    furance_len=0.305 # 小温区长度
    interval_len=0.05 # 间隙长度
    if x <= -0.25:
        return 25
    elif x <= 0:
        return 25 + (150)/0.25 * (x+0.25)
    elif x <= 5*furance_len+4*interval_len and x >= 0:
        return 175
    elif x <= 5*(furance_len+interval_len):
        return 175 + (20/interval_len) * (x-(5*furance_len+4*interval_len))
    elif x <= 6*furance_len+5*interval_len:
        return 195
    elif x <= 6*(furance_len+interval_len):
        return  195 + (40/interval_len) * (x-(6*furance_len+5*interval_len))
    elif x <= 7*furance_len + 6*interval_len:
        return 235
    elif x <= 7*(furance_len+interval_len):
        return 235 + (20/interval_len) * (x-(7*furance_len + 6*interval_len))
    elif x <= 9*furance_len+8*interval_len:
        return 255
    elif x <= 9*(furance_len+interval_len):
        return  255 - (230/interval_len) * (x-(9*furance_len+8*interval_len))
    else:
        return 25

# 求解锡膏温度曲线u(z,t)
def heat_equation():
    pass
    
# 绘图
# x=np.linspace(-0.3,4,5000)
# y=np.linspace(0,0,5000)
# for index in range(x.size):
#     y[index]=getFurnacetemperature_exp(x[index])
    
# plt.plot(x,y)
# plt.show()
```

### Q1_pso.py

```python
from Q1_ut import *

def pso():
    N=20 # 种群个数
    d=1 # 维度
    cnt_max=70 # 最大迭代次数
    xlimit_a=[1e-4,1e-3] # a位置界限
    vlimit_a=[-1e-5,1e5] # a速度界限
    
    xlimit_h=[0,10] # h位置界限
    vlimit_h=[-0.3,0.3] # h速度界限
    
    w=0.8 # 惯性系数
    c1=0.5 # 个体学习参数
    c2=0.5 # 全局学习系数

    # 初始化种群
    a_x=np.random.uniform(low=xlimit_a[0], high=xlimit_a[1], size=20)
    h_x=np.random.uniform(low=xlimit_h[0], high=xlimit_h[1], size=20)
    # 初始化个体速度
    a_v=np.random.uniform(low=-vlimit_a[0], high=vlimit_a[1], size=20)
    h_v=np.random.uniform(low=-vlimit_h[0], high=vlimit_h[1], size=20)

    # 个体历史最优
    individual_best=np.zeros(a_x.size)
    for index in range(a_x.size):
        individual_best[index]=np.copy(CN(a_x[index],h_x[index],100,0.15e-3))
    # 个体历史最优位置
    individual_best_a=np.copy(a_x)
    individual_best_h=np.copy(h_x)
    # 全局最优解
    global_best=0
    # 全局历史最优位置
    global_best_a=0
    global_best_h=0

    # 初始化全局最优
    for index in range(a_x.size):
        temp=CN(a_x[index],h_x[index],100,0.15e-3)
        if(global_best > temp):
            global_best_a=a_x[index]
            global_best_h=h_x[index]
            global_best=temp
            
    # 进行迭代
    for cnt in range(cnt_max):
        print("迭代次数: ",cnt)
        r1=np.random.rand(1)
        r2=np.random.rand(1)
        for index in range(a_x.size):
            # 更新a,v速度
            va_temp=w*a_v[index] + c1*r1[0]*(individual_best_a[index]-a_x[index]) + c2*r2[0]*(global_best_a-a_x[index])
            vh_temp=w*h_v[index] + c1*r1[0]*(individual_best_h[index]-h_x[index]) + c2*r2[0]*(global_best_h-h_x[index])
            if va_temp >= vlimit_a[0] and va_temp <= vlimit_a[1]:
                a_v[index]=va_temp
            else:
                if va_temp>vlimit_a[1]:
                    a_v[index]=vlimit_a[1]
                else:
                    a_v[index]=vlimit_a[0]
            if vh_temp >= vlimit_h[0] and vh_temp <= vlimit_h[1]:
                h_v[index]=vh_temp
            else:
                if vh_temp>vlimit_a[1]:
                    h_v[index]=vlimit_h[1]
                else:
                    h_v[index]=vlimit_h[0]
            # 更新a,v位置
            if a_x[index]+a_v[index]>=xlimit_a[0] and a_x[index]+a_v[index]<=xlimit_a[1] and h_x[index]+h_v[index]>=xlimit_h[0] and h_x[index]+h_v[index]<=xlimit_h[1]:
                a_x[index] = a_x[index]+a_v[index]
                h_x[index] = h_x[index]+h_v[index]
                # 更新个体历史最优
                if individual_best[index] > CN(a_x[index],h_x[index],100,0.15e-3):
                    individual_best_a[index] = a_x[index]
                    individual_best_h[index] = h_x[index]
                    individual_best [index] = CN(a_x[index],h_x[index],100,0.15e-3)
                # 更新全局历史最优
                if global_best > CN(a_x[index],h_x[index],100,0.15e-3):
                    global_best_a = a_x[index]
                    global_best_h = h_x[index]
                    global_best = CN(a_x[index],h_x[index],100,0.15e-3)
    
    return np.average(a_x),np.average(h_x),global_best

print(pso())
```

### Q1_ut.py

```python
from Q1 import *
def CN(a, h, m, solder_thickness):
    dt=0.5
    dz=0.15e-3/m
    r=a**2 * dt / (dz)**2
    
    initial_val=np.full((m+1,1),25)
    
    left1=np.zeros((m+1,m+1))
    # left2=np.zeros((m+1,1))
    right1=np.zeros((m+1,m+1))
    right2=np.copy(initial_val)
    right3=np.zeros((m+1,1))
    res=np.zeros((int(np.floor(4.105/(0.7/60)/0.5)),2))
    
    for cnt in range(int(np.floor(4.105/(0.7/60)/dt))):
        for index in range(m+1):
            if index == 0:
                left1[0][0]=1+h*dz
                left1[0][1]=-1
                right3[index][0]=h*dz*getFurnacetemperature_exp(dt*cnt*0.7/60-0.25)
            elif index == m:
                left1[m][m]=1+h*dz
                left1[m][m-1]=-1
                right3[index][0]=h*dz*getFurnacetemperature_exp(dt*cnt*0.7/60-0.25)
            else:
                left1[index][index-1]=-r
                left1[index][index]=2*(1+r)
                left1[index][index+1]=-r
                
                right1[index][index-1]=r
                right1[index][index]=2*(1-r)
                right1[index][index+1]=r
        # 存入
        
        res[cnt][0]=cnt*dt
        res[cnt][1]=right2[int(m/2)][0]
        right2=np.copy(np.linalg.inv(left1) @ (right1 @ right2 + right3)) 
    sum=0
    experiment_temperature=np.array(pd.read_csv('附件.csv'))
    for index in range(int(res.T[0].size/2.2)):
        sum+=(res[index][1]-experiment_temperature[index][1])**2
    return sum



# aa=CN(6.588e-4,1.97,100,0.15e-3)
# pd.DataFrame(aa).to_csv('11.csv',index=False)

# x=np.linspace(-0.3,4,5000)
# y=np.linspace(0,0,5000)
# for index in range(x.size):
#     y[index]=getFurnacetemperature_exp(x[index])
    
# # plt.plot(x,y)
# plt.plot(aa.T[0]*0.7/60-0.25,aa.T[1])
# plt.plot(experiment_temperature.T[0]*0.7/60-0.25,experiment_temperature.T[1])
# plt.grid()
# plt.show()
```
## Q2

## Q3

## Q4