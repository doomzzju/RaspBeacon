import sys, time
from bluepy.btle import Scanner, DefaultDelegate

discoveredDevices = []
namedDevices = []

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

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData): pass


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
scannerTracking = Scanner().withDelegate(ScanDelegateTracking())


def ricorsiva(distance):
    #devices = scanner.scan(5.0)
    #named = False
    #selectednumber = input("Select device by digiting its number occurence: ")
    #selecteddevice = None

    #for device in discoveredDevices:
    #    if device.number == selectednumber:
    #        selecteddevice = device 

    #for device in namedDevices:
    #    if selecteddevice.devi.addr == device.devi.addr:
    #        print"You choose %s" % device.name
    #        named = True

    #if not named:
    #    print"Selezionato dispositivo con indirizzo: %s" % selecteddevice.devi.addr
    #    devname = raw_input("Name the chosen device: ")
    #    selecteddevice.setname(devname)
    #    namedDevices.append(selecteddevice)
    #    print"Given name: %s" % devname

    dev_mac_addr = '49:61:52:74:34:54'
    COUNTS = 10
    TIMECOST = 1.0
    DATANEED = 10
    DATACOLLECTED = 0

    print"Scans are starting..."
    stop = False
    rssi = []
    start = time.time()
    while DATACOLLECTED < DATANEED:
        for n in range(COUNTS):  # change this value if you want more or less scans each while loop
            devices = scannerTracking.scan(TIMECOST)  
            for dev in devices:
                if dev.addr == dev_mac_addr: 
                    print("RSSI=%d dB, Distance=%f m" % (dev.rssi, getdistance(dev.rssi)))
                    rssi.append(dev.rssi)
                    DATACOLLECTED += 1
                    break

        #a = raw_input("Keep tracking this device? Yes/No: ")
        #if a == "No":
        #    stop = True
        #if a == "Yes":
        #    pass
    end = time.time()
    cost = end - start
    print('scan cost: ', cost, 's')

    #b = raw_input("Tracking new device?: Yes/No: ")
    #if b == "Yes":
    #    ricorsiva()
    #else:
    #    return
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
