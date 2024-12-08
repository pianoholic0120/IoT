import numpy  as np 
import solver
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
    for i in range(len(averaage[0])):
        if(averaage[2][i] >= 20 or averaage[2][i] <= 8):
            while(True):
                if(averaage[2][i] %2 == 0):
                    if(j <= len(averaair[0])-1):
                        #print(i, j)
                        if(averaair[0][j] == averaage[0][i] and averaair[1][j] == averaage[1][i] and averaair[2][j] == averaage[2][i]):
                            if(averaage[3][i] != 0):
                                data_mat = np.append(data_mat, [[averaage[3][i]], [averaair[3][j]]], axis=1)
                            break
                        else: j += 1
                    if(j >= len(averaair[0])-1): break
                else: break
    return data_mat


data = np.genfromtxt('./watch_data/merged_and_sorted_with_filled_timestamps.csv',dtype=str, delimiter = ',', skip_header=1)
heartrate = data[:,1]
time = data[1:,0]   
averaage = heartrate_preprocessor(heartrate, time)

airdata = np.genfromtxt('./air_quality/combined.txt',dtype=str, encoding = 'utf-8' , delimiter = ',', skip_header=1)
pm = airdata[:,5]
#pm = pm.astype(float)
time = airdata[:,1]
averaair = air_preprocessor(pm, time)
data_mat = matrix_processor(averaage, averaair)

a,b = solver.Linear_LS_Regression(data_mat[1], data_mat[0], len(data_mat[0]))
        
print(a,b)