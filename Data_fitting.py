import numpy  as np 
import solver
import math as m
import scipy.stats as stats
from datetime import datetime
def heartrate_preprocessor(heartrate, time):
    heartrate = heartrate.astype(float)
    month = np.zeros(len(heartrate))
    day = np.zeros(len(heartrate))
    hour = np.zeros(len(heartrate))
    minute = np.zeros(len(heartrate))
    for i in range(len(month)-1):

        dt = datetime.strptime(time[i], "%Y-%m-%d %H:%M:%S")
        
        month[i] = dt.month
        day[i] = dt.day
        hour[i] = dt.hour
        minute[i] = dt.minute

    averaged = np.zeros((4, 0))
    end = -1
    for i in range(100000):
        if(end < len(heartrate)-1):
            hour0, averagee, end = average(hour, heartrate, end+1)
            averaged =np.append(averaged, [[month[end]], [day[end]], [hour0], [averagee]], axis=1)
        else: break
    return averaged
def air_preprocessor(heartrate, time):
    heartrate = heartrate.astype(float)
    month = np.zeros(len(heartrate))
    day = np.zeros(len(heartrate))
    hour = np.zeros(len(heartrate))
    minute = np.zeros(len(heartrate))
    for i in range(len(month)-1):
        dt = datetime.strptime(time[i], "%Y-%m-%d %H:%M")
        month[i] = dt.month
        day[i] = dt.day
        hour[i] = dt.hour
        minute[i] = dt.minute

    averaged = np.zeros((4, 0))
    for i in range(len(heartrate)):
        averaged = np.append(averaged, [[month[i]],[day[i]],  [hour[i]],[heartrate[i]]],axis = 1)

    return averaged
def average(hour, heartrate, start):
    num = 0
    temp = 0
    i = start
    while(True):

        if(i > len(hour)):
            break
        
        if (hour[i] == hour[start]):
            if(heartrate[i] != 0):
                temp += heartrate[i]
                num += 1

        else: break
        if(i+1 <= len(heartrate)):
            i = i+1
        else: break
    if(num == 0):num = 1

    return hour[start], temp/num, i
def matrix_processor(heartrate, air):
    data_mat = np.zeros((2,0))
    j = 0
    for i in range(len(heartrate[0])):
        if(  heartrate[2][i] >= 2 and heartrate[2][i] <= 6):
            while(True):
                
                    if(j <= len(air[0])-1):
                        #print(i, j)
                        if(air[0][j] == heartrate[0][i] and air[1][j] == heartrate[1][i] and air[2][j] == heartrate[2][i]-1):
                            #print("HELLO")
                            if(heartrate[3][i] != 0):
                                data_mat = np.append(data_mat, [[heartrate[3][i]], [air[3][j]]], axis=1)
                            break
                        else: j += 1
                    if(j >= len(air[0])-1): break
                
    return data_mat

def fitter(hdatapath, airdatapath):
    data = np.genfromtxt(hdatapath, dtype=str, delimiter = ',', skip_header=1)
    heartrate = data[:,1]
    time = data[1:,0]   
    averaage = heartrate_preprocessor(heartrate, time)
    
    airdata = np.genfromtxt(airdatapath,dtype=str, encoding = 'utf-8' , delimiter = ',', skip_header=1)
    pm = airdata[:,4]
    #pm = pm.astype(float)
    time = airdata[:,1]
    averaair = air_preprocessor(pm, time)
    data_mat = matrix_processor(averaage, averaair)
    
    a,b = solver.Linear_LS_Regression(data_mat[1], data_mat[0], len(data_mat[0]))
            
    #print(a,b)
    cor = np.corrcoef(data_mat[1], data_mat[0])
    cor = cor[0][1]
    _, p = stats.pearsonr(data_mat[1], data_mat[0])
    return a, b, cor, p

data_air_path = './air_quality/combined.txt'
data_h_path = './watch_data/merged_and_sorted_with_filled_timestamps.csv'
m, b, cor, p = fitter(data_h_path, data_air_path)
print(m, b, cor, p)