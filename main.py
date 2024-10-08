# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def parse_elo_graph(file):
    elo_list = []
    for line in file:
        found = line.find('New Elo: ')
        if found >= 0:
            elo_str = line[found + 9: found + 13]
            elo_int = int(elo_str)
            elo_list.append(elo_int)
    return elo_list

def smooth_elo(base_elo, sharpness):
    if sharpness > 1:
        sharpness = 0.85
    #temp = base_elo.reverse()
    temp = base_elo[:]
    temp.reverse()
    smooth = []
    #smooth = []
    smooth.append(temp[0])
    for i in range(len(temp) - 1):
        smooth.append(smooth[i] * sharpness + temp[i + 1] * (1-sharpness))
    #smooth.append(base_elo[len(base_elo) - 1])
    smooth.append(2000)
    smooth.reverse()
    return smooth

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = open(str(Path.home() / "Downloads/history_S3.txt"), "rt", encoding='UTF-8')
    s3_elo = parse_elo_graph(file)
    s3_elo.insert(0, 2000)
    file.close()
    file = open(str(Path.home() / "Downloads/history_S4.txt"), "rt", encoding='UTF-8')
    s4_elo = parse_elo_graph(file)
    s4_elo.append(2000)
    s4_elo.reverse()
    file.close()
    file = open(str(Path.home() / "Downloads/history_alt.txt"), "rt", encoding='UTF-8')
    alt_elo = parse_elo_graph(file)
    alt_elo.append(2000)
    alt_elo.reverse()
    file.close()

    damping = 0.8
    smooth_s3 = smooth_elo(s3_elo, damping)
    smooth_s4 = smooth_elo(s4_elo, damping)
    smooth_alt = smooth_elo(alt_elo, damping)

    plt.subplot(2, 1, 1); plt.title('True elo')
    plt.plot(s3_elo)
    plt.plot(s4_elo)
    plt.plot(alt_elo)
    plt.legend(['season 3', 'season 4', 'alt account'])
    #plt.show()

    plt.subplot(2, 1, 2); plt.title('Smoothed curve')
    plt.plot(smooth_s3)
    plt.plot(smooth_s4)
    plt.plot(smooth_alt)
    plt.legend(['season 3', 'season 4', 'alt account'])
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
