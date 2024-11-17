
You will need the following:

RaspberryPi Pico or Pico W.
USB C Port - https://amzn.eu/d/fpsSOgz image is included in this folder.
Toggle Switch - Only if you want to manual power switch or a power switch to isolate the Pico from the LEDs if you're wanting to play around with the Pico software.
LED Rings - These are 241 LEDs in total over 9 rings, the smallest having 1 LED the largest having 60.  You will need to manually resolder all the connections because they're just too big and bulky - although you could expand the CPU Holder part to accommodate them it would make the back fairly chunky.
USB C 5volt 5amp Power Supply - These are readily available as power supplies for RaspberryPi 5 computers.  
Wires - Keep in mind they could be carrying up to 5amps, so make sure they're suitably specified for the task.

At maximum brightness these LEDs could be pulling up to 9amps.  For this reason the software defaults to limiting the brightness and will typically keeps its power use under 3amps using the default settings.  You can dial up the brightness, but be aware that you may find the higher power demand causes the power supply to cut out or the Pico to crash or reboot due to unstable power.  Some effects are significantly more power hungry than others so the reboots might only happen when certain effects run.  You can optionally ignore the USB C port and install something else to supply power at significantly more amps.  During tests turning all LEDs up to a value of 150 out of 255 caused power consumption to hit 5amps, while 100 out of 255 saw around 3.5amps.  The maxbrightness value in the script defaults to 0.5 which is about 128, pulling a max of about 3amps.



