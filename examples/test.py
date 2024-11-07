from time import sleep
from datetime import datetime
import os, sys
sys.path.append(r'C:\Users\1219-Measurement\Documents\rigol-ds1000z')
from rigol_ds1000z import Rigol_DS1000Z
from rigol_ds1000z import process_display, process_waveform
import numpy as np

visa_string = "USB0::0x1AB1::0x04CE::DS1ZC231701915::INSTR"
visa_backend = "@ivi"
userPath = r"C:\Users\1219-Measurement\Desktop\1219 Experiment data"
filename = "Accelerometer"

## Save the data in a dated file 
dateToday = datetime.today().strftime('%y%m%d')
path = userPath+"\\"+dateToday
if not os.path.exists(path):
    os.makedirs(path)
tag = 0
while os.path.exists(path+'\\'+dateToday+'_'+filename+'_{:04}.txt'.format(tag)):
    tag += 1
filepath = path+'\\'+dateToday+'_'+filename+'_{:04}.txt'.format(tag)

with Rigol_DS1000Z(visa_name=visa_string, backend=visa_backend) as oscope:
    # reset to defaults and print the IEEE 488.2 instrument identifier
    ieee = oscope.ieee(rst=False)
    print(ieee.idn)

    # configure channels 1 and 2, the timebase, and the trigger
    channel1 = oscope.channel(1, probe=1, coupling="DC", scale=1)
    timebase = oscope.timebase(main_scale=200e-3)
    trigger = oscope.trigger(mode="EDGE", source=2, coupling="DC", level=0)

    # send an SCPI commands to setup the math channel
    # oscope.write(":MATH:DISPlay ON")

    oscope.run()

    # capture the display image
    display = oscope.display()
    process_display(display, show=True)

    # plot the channel 1 waveform data 
    waveform = oscope.waveform(source=1)
    xdata, ydata = process_waveform(
        waveform, show=True, filename=filepath
    )
    
    oscope.close()