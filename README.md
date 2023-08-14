# TwitchSniffer

- Uses decapi.me for searching streams online
- Automates browser to open and close stream
- Can be used with browser Twitch collecting extension
- Works on RPi4

## Dependencies

- Python 3.11
- Requests
- BeautifulSoup4
- Keyboard
- Psutil

## RPi4

- Works on RPi4 running 64-bit RpiOS with chromium-browser
- Can start on boot (after user login) automatically with Autostart [forums.raspberrypi.os](https://forums.raspberrypi.com/viewtopic.php?t=294014)

#### Autostart file for RPi4
Create autostart file in following path
```bash
sudo nano  /home/USER_NAME/.config/lxsession/LXDE-pi/autostart
```
Recommended autostart contents:
```bash
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@lxterminal --working-direcotry=PATH_TO_TWITCHSNIFFER_DIR -e python3 PATH_TO_TWITCHSNIFFER_DIR/main.py
```
