import sys, os
import numpy as np 
from matplotlib import pyplot as plt

if len(sys.argv) != 2:
    print('Usage: python drawRSSI.py rssi_path')
    exit()
rssi_path = sys.argv[1]
distances = []
rssis = []
distances_single = []
rssi_mean = []
rssi_median = []
rssi_time = []
filelist = os.listdir(rssi_path)
filelist.sort()
for file_name in filelist:
    with open(rssi_path + file_name) as f:
        lines = f.readlines()
        distance = float(lines[0])
        cost = float(lines[1])
        temp_rssi = []
        for i in range(2, len(lines)):
            rssi = float(lines[i])
            distances.append(distance)
            temp_rssi.append(rssi)
            rssis.append(rssi)
        distances_single.append(distance)
        rssi_time.append(cost)
        rssi_mean.append(np.mean(temp_rssi))
        rssi_median.append(np.median(temp_rssi))

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.set_xlabel('distance[m]')
ax1.set_ylabel('rssi[dB]')
ax2.set_ylabel('timecost[s]')
plt.title('distance-rssi')
ax1.scatter(distances, rssis, marker='.', color='blue')
ax1.plot(distances_single, rssi_mean, label='mean')
ax1.plot(distances_single, rssi_median, label='median', color='r')
ax2.plot(distances_single, rssi_time, label='timecost', color='g')
ax1.legend(loc='upper left')
ax2.legend()
plt.grid()

plt.show()
