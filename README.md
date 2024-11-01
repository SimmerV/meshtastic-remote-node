# meshtastic-remote-node

--MR-W Meshtastic Build--

With this build, I am running a high level router/repeater in Modesto. The entire box sits at ~130ft on a radio tower, and is controlled entirely via the RPI4. 
I can use VNC to use the web flasher or web client, and SSH for all else. 



///Parts List: 

Raspberry Pi4
Station G2 radio
Airframes cavity filter
2 channel relay
2x Noctua 60mm fans


///Scripts included:

fan_control.py  # Controls Noctua fans via PWM
restart_node.py  # Standalone restart script 
flash_firmware.py  # Places Station G2 in firmware flashing mode
