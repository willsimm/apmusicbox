Ageing Playfully Raspberry Pi3 music box

Hook up external hardware: 
- Each LED needs a resistor, then connect to GPIO pins of Raspberry PI. Pinout here: https://www.raspberrypi.org/learning/python-quick-reaction-game/worksheet/
- Hookup picade (flash with latest firmware to save volume level) and makey makey by USB for button-keyboard input.
    - The picade and makey makey map to keyboard buttons. Check the keyboard and light map in the code.
- Hookup dreamer nano (leonardo clone) over usb and flash with firmware. Connect to flex and force sensors via potential divider circuit on analogue inputs. 
    - This device sends inputs over serial - check serial port is correct in the code.

Config Pi:
- Make sound come out of headphone jack: amixer cset numid=3 1
- Make code run at boot: Crontab -e then add @reboot sudo python /home/pi/ap/ap.py &

Config network stuff:
- Set Pi up as a Wifi access point: https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software
- Optional - Change Hostname (change to ageing playfully): http://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname/
- Install Apache and php:https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md
- Change www folder (change to /home/pi/ap/www): http://stackoverflow.com/a/23175981

Connect to hotspot and head to http://raspberrypi/ in a browser. You can also ssh pi@raspberrypi.

In the browser you can edit and upload playback files, and download usage recordings.

TODO:
- Fix threading so during playback buttons can be pressed
- on playback take into account length of sample in delay as sometimes plays back too quick but timing gap is correct.
- map force sensor to tones
- add mic recording input to create user samples, map to new buttons?
- other inputs
- Make web interface display look nicer
- Web interface config and mapping of buttons / lights and upload / selection of sound samples.
