# vaio-pi4
Repurposing Sony Vaio PCG-GRT360ZQ to use a PI4

Components:

CHASIS/LCD/POWER
- 1 x Old laptop, with big case. We are going to remove ALL components, so the more free space the better
- 1 x LCD/Display controller. You need to check in the laptop LCD for right controller. Mine was this (https://www.aliexpress.com/item/1005006254641119.html?spm=a2g0o.order_list.order_list_main.13.418d1802jBBXqt)
- 2 x Step Down Buck Converter (in my case from 19v to 5v/5A and 12v/5A)

KEYBOARD
- 1 x Raspberry PICO

TRACKPAD
- 1 x Arduino Nano/MiniPro/some atmega
- 1 x 5v/3.3v level converter

CPU/GPU
- 1 x Raspberry Pi / Orange Pi / some mini PC
- 1 x HDMI/Mini HDMI cable (it depends on the mini PC)
- 1 x USB to SDD/M.2 adapter
- 1 x SSD/M.2 disk

WIRING
- thin wires (for keybaord/trackpad)
- thick wires (12v/5v/lighting)
- some 5v leds

Notes:
- Pins combination not used in your keyboard can be used for any general purpose button. I used 2 pins for the trackpad buttons


Credits:
- Arduino PS2 Mouse - https://github.com/rucek/arduino-ps2-mouse
- Pico Laptop Keyboard - https://github.com/s12wu/laptop-keyboard-reader

TODO:
- Use all the laptop buttons for general purposes
- Use all the laptop leds
- Add a ON/OFF switch
- Regulate the Fans using a transistor

![diagram](/misc/diagram.png)

![pico](/misc/pico%20external%20pullup%20resistors.jpeg)

![pico2](/misc/keyboard%20to%20pico.jpeg)

![finished setup](/misc/all%20working.jpeg)