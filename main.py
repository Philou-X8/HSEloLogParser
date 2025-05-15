
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def parse_elo_logs(file_in):
    elo_list = [2000]
    for line in file_in:
        found = line.find('New Elo: ')
        if found >= 0:
            elo_str = line[found + 9: found + 13]
            elo_int = int(elo_str)
            elo_list.append(elo_int)
    return elo_list

## smooth the graph using a rolling average
def smooth_elo(base_elo, sharpness):
    if sharpness > 1:
        sharpness = 0.85
    #temp = base_elo.reverse()
    temp = base_elo[:]
    temp.reverse()
    smooth = []
    smooth.append(temp[0])
    for i in range(len(temp) - 1):
        smooth.append(smooth[i] * sharpness + temp[i + 1] * (1-sharpness))
    #smooth.append(base_elo[len(base_elo) - 1])
    smooth.append(2000)
    smooth.reverse()
    return smooth

def DeriveGraph(arr):
    ret = []
    for ii in range(len(arr) - 1):
        ret.append(arr[ii+1] - arr[ii])
    return ret

def IntegrateGraph(arr, start_val):
    ret = [start_val]
    for ii in range(len(arr)):
        ret.append(ret[ii] + arr[ii])
    return ret

def TryGetDelta(arr, index, delta):
    if (index + delta) < 0:
        return arr[0]
    elif (index + delta) >= len(arr):
        return arr[len(arr) - 1]
    return arr[index + delta]

def ClampedSmooth(arr, count):
    lower_bound = 0 - int(count/2)
    upper_bound = int( count/2 + 0.5)
    smooth_arr = []
    for ii in range(len(arr)):
        avg_sum = 0
        for jj in range(lower_bound, upper_bound):
            avg_sum += TryGetDelta(arr, ii, jj)
        smooth_arr.append(avg_sum / count)
    return smooth_arr

def SmoothIncline(arr):
    dt_arr = ClampedSmooth(DeriveGraph(arr), 5)
    dt_arr = ClampedSmooth(dt_arr, 5)
    dt_arr = ClampedSmooth(dt_arr, 10)
    return IntegrateGraph(dt_arr, 2000 - dt_arr[0])

def SmoothPeeks(arr):
    dt_arr = ClampedSmooth(DeriveGraph(arr), 5)
    dt_arr = ClampedSmooth(dt_arr, 5)
    dt_arr = ClampedSmooth(dt_arr, 10)
    ddt_arr = ClampedSmooth(DeriveGraph(dt_arr), 5)
    ddt_arr = ClampedSmooth(ddt_arr, 10)
    dddt_arr = ClampedSmooth(DeriveGraph(ddt_arr), 10)

    peeks_x = [0]
    peeks_y = [2001]
    for ii in range(len(dddt_arr) - 1):
        if (dddt_arr[ii] * dddt_arr[ii+1]) < 0:
            peeks_x.append(ii)
            peeks_y.append(arr[ii])
        elif (dt_arr[ii] * dt_arr[ii+1]) < 0:
            peeks_x.append(ii)
            peeks_y.append(arr[ii])
    peeks_x.append(int(len(arr)-1))
    peeks_y.append(arr[-1])

    return peeks_x, peeks_y


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    file3 = open("history_S3.txt", "rt", encoding='UTF-8')
    s3_elo = parse_elo_logs(file3)
    file3.close()

    file4 = open("history_S4.txt", "rt", encoding='UTF-8')
    s4_elo = parse_elo_logs(file4)
    file4.close()

    file5 = open("history_S5.txt", "rt", encoding='UTF-8')
    s5_elo = parse_elo_logs(file5)
    s5_elo.pop(0)
    s5_elo.reverse()
    file5.close()

    file4a = open("history_S4_Alts.txt", "rt", encoding='UTF-8')
    s4_elo_Alts = parse_elo_logs(file4a)
    file4a.close()
    file4s = open("history_S4_suffering.txt", "rt", encoding='UTF-8')
    s4_elo_suffering = parse_elo_logs(file4s)
    file4s.close()

    s3_x, s3_y = SmoothPeeks(s3_elo)
    s4_x, s4_y = SmoothPeeks(s4_elo)
    s4_a_x, s4_a_y = SmoothPeeks(s4_elo_Alts)
    s4_s_x, s4_s_y = SmoothPeeks(s4_elo_suffering)
    s5_x, s5_y = SmoothPeeks(s5_elo)

    plt.subplot(2, 1, 1); plt.title('All seasons')
    plt.plot(s3_x, s3_y)
    plt.plot(s4_x, s4_y)
    plt.plot(s5_x, s5_y)
    plt.legend(['S3', 'S4', 'S5'])
    plt.subplot(2, 1, 2); plt.title('Season 3')
    plt.plot(s4_x, s4_y)
    plt.plot(s4_a_x, s4_a_y)
    plt.plot(s4_s_x, s4_s_y)
    plt.legend(['Phil', 'Alts Are Cringe', 'suffering'])
    plt.show()
