Ageing Playfully Raspberry Pi3 music box

Hook up external hardware: 
- Each LED needs a resistor, then cpnnect to GPIO pins of Raspberry PI. Pinout here: https://www.raspberrypi.org/learning/python-quick-reaction-game/worksheet/
- Hookup picade (flash with latest firmware to save volume level) and makey makey by USB for button-keyboard input.
- Hookup dreamer nano (leonardo clone) over usb and flash with firmware. Connect to flex and force sensors via potential divider circuit on analogue inputs

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


