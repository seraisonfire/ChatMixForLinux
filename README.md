# ChatMixForLinux
Adds **ChatMix functionality** which was originally only available through SteelSeries' GG app to Linux. It works on some SteelSeries headsets using [HeadsetControl](https://github.com/Sapd/HeadsetControl), and allows the user to quickly adjust the volume of game and communication applications so the user can focus on one of them if needed.

---

## Features

- Real-time monitoring of ChatMix slider value from some SteelSeries headsets (check which ones are supported in the [HeadsedControl repo](https://github.com/Sapd/HeadsetControl).)
- Dynamic volume balancing between game and communication apps. 
- Runs as a background user service with systemd, but can be used with other service managers as well. 
- In the python file applications can be added as exceptions, which then will not be regulated by the ChatMix feature.

---
## Dependencies
- Python 3.5+
- [HeadsetControl](https://github.com/Sapd/HeadsetControl)
- PipeWire with WirePlumber

---
### Usage

Run the script directly:

python chatmix.py

Or install and enable the systemd user service:
```
cp service-files/chatmix.service ~/.config/systemd/user/chatmix.service
systemctl --user daemon-reload
systemctl --user enable --now chatmix.service
```
This will start the script automatically in the background on login. 


---

Configuration

By default, the script adjusts volumes for the following applications:

Communication (e.g., Discord)

Everything else (with exceptions being able to be added in the corresponding array.

> By default, only Discord is added as a communication app, with exceptions for everything else.
> A tutorial on how to add more is in the python file.

There is also an option for the ChatMix feature only to work while you are in a voice chat with somebody, and if you aren't, the wheel on the headset will not work. It is enabled by default.
---


Note: This project depends on HeadsetControl, which is licensed under GPL. This script only calls it as a CLI dependency and does not include or modify its code.


---

Credits

Developed by seraphine

Inspired by and depends on HeadsetControl by Sapd, without his project this would not have been possible.




