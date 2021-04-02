import sys, time
import numpy as np
from bluepy.btle import Scanner, DefaultDelegate, Peripheral

discoveredDevices = []
namedDevices = []
rssi = []
dev_mac_addr = '49:61:52:74:34:54'
COUNTS = 10
TIMECOST = 1.0
DATANEED = 10
DATACOLLECTED = 0

class Device:  
    def __init__(self, devi, number):
        self.devi = devi  
        self.number = number  
        self.name = "default"

    def setname(self, name):
        self.name = name
        
    def setnewnumber(self, number):
        self.number = number


def getdevice(addr):
    for device in namedDevices:
        if device.devi.addr == addr:
            return device


class ScanDelegate(DefaultDelegate): 
    i = 1

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            flag = False
            if not namedDevices:
                print"%d) New device detected" % ScanDelegate.i, dev.addr
                discoveredDevices.append(Device(dev, ScanDelegate.i))
            else:
                for device in namedDevices:
                    if device.devi.addr == dev.addr:
                        flag = True

                if flag:
                    print"%d) %s" % (ScanDelegate.i, getdevice(dev.addr).name)
                    getdevice(dev.addr).setnewnumber(ScanDelegate.i)
                    discoveredDevices.append(getdevice(dev.addr))
                else:
                    print"%d) New device detected" % ScanDelegate.i, dev.addr
                    discoveredDevices.append(Device(dev, ScanDelegate.i))

            ScanDelegate.i += 1


class ScanDelegateTracking(DefaultDelegate): 
    def __init__(self, addr):
        DefaultDelegate.__init__(self)
        self.addr = addr

    def handleDiscovery(self, dev, isNewDev, isNewData): 
        if dev.addr == self.addr:
            rssi.append(dev.rssi)
            print("RSSI=%d dB, Distance=%f m" % (dev.rssi, getdistance(dev.rssi)))
            global DATACOLLECTED
            DATACOLLECTED += 1


def getdistance(rssi):
    txpower = -75   #one meter away RSSI
    if rssi == 0:
        return -1
    else:
        ratio = rssi*1.0 / txpower
        if ratio < 1:
            return ratio ** 10
        else:
            return 0.89976 * ratio**7.7095 + 0.111


scanner = Scanner().withDelegate(ScanDelegate())
scannerTracking = Scanner().withDelegate(ScanDelegateTracking(dev_mac_addr))


def ricorsiva(distance):
    print"Scans are starting..."
    stop = False
    start = time.time()
    while DATACOLLECTED < DATANEED:
        scannerTracking.scan(TIMECOST) 

    print('mean rssi %f' % np.mean(rssi)) 

    end = time.time()
    cost = end - start
    print('scan cost: ', cost, 's')

    f = open(str(distance) + "_rssi.csv", "w+")
    f.write(str(distance) + '\n')
    f.write(str(cost) + '\n')
    for item in rssi:
        f.write(str(item) + '\n')
    f.close()

if len(sys.argv) != 2:
    print('Usage: python GettingRSSI.py distance[m]')
    exit()
ricorsiva(sys.argv[1])
