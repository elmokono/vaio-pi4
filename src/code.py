import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from keycode_win_us import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import board
import digitalio
import time
import microcontroller
import busio

# Function to set a pin as an input (external pullup is soldered to the board) so it's high unless grounded by a key press
def go_z(p):
    pins[p].direction = digitalio.Direction.INPUT  # set as input
    pins[p].pull = None


# Function to set a pin as an output and drive it to a logic low (0 volts)
def go_0(p):
    pins[p].pull = None  # disable pullup
    pins[p].direction = digitalio.Direction.OUTPUT  # set as output
    pins[p].value = 0  # drive low

# definition of matrix keymap (which pin connection belongs to which key)
MousecodeLeftClick = 100
MousecodeRightClick = 101
keymap = [
    [15, 19, Keycode.PRINT_SCREEN],
    [6, 18, Keycode.ONE],
    [5, 18, Keycode.CAPS_LOCK],
    [8, 13, Keycode.X],
    [7, 14, Keycode.C],
    [12, 21, Keycode.B],
    [13, 17, Keycode.COMMA],
    [4, 13, Keycode.ALTGR],
    [12, 23, Keycode.DOWN_ARROW],
    [6, 14, Keycode.W],
    [5, 12, Keycode.A],
    [7, 12, Keycode.S],
    [9, 16, Keycode.Y],
    [2, 10, 0],  # Fn
    [4, 9, Keycode.LEFT_ALT],
    [8, 11, Keycode.FOUR],
    [7, 18, Keycode.FIVE],
    [8, 9, Keycode.E],
    [7, 11, Keycode.R],
    [8, 14, Keycode.D],
    [14, 17, Keycode.F],
    # [,,Keycode.OEM_102],
    [9, 21, Keycode.EIGHT],
    [17, 18, Keycode.NINE],
    [6, 13, Keycode.Z],
    [11, 21, Keycode.U],
    [14, 21, Keycode.J],
    [13, 16, Keycode.N],
    # [,,Keycode.AKUT],
    [18, 19, Keycode.EQUALS],
    [13, 19, Keycode.ENTER],
    [12, 20, Keycode.FORWARD_SLASH],
    [13, 20, Keycode.APPLICATION],
    [8, 18, Keycode.THREE],
    [5, 11, Keycode.TAB],
    [6, 9, Keycode.Q],
    [9, 17, Keycode.I],
    [14, 16, Keycode.H],
    [5, 10, Keycode.GRAVE_ACCENT],
    [18, 23, Keycode.PAGE_UP],
    [7, 10, Keycode.F5],
    [10, 21, Keycode.F8],
    [15, 20, Keycode.BACKSPACE],
    [7, 9, Keycode.T],
    [18, 21, Keycode.O],
    [14, 19, Keycode.QUOTE],
    [5, 15, Keycode.ESCAPE],
    [10, 17, Keycode.F10],
    [15, 17, Keycode.F11],
    [10, 22, Keycode.INSERT],
    [16, 18, Keycode.SEVEN],
    [11, 20, Keycode.LEFT_BRACKET],
    [9, 20, Keycode.SEMICOLON],
    [15, 22, Keycode.DELETE],
    [11, 23, Keycode.PAGE_DOWN],
    [13, 23, Keycode.LEFT_ARROW],
    [15, 23, Keycode.RIGHT_ARROW],
    [6, 10, Keycode.F1],
    [6, 15, Keycode.F2],
    [7, 15, Keycode.F6],
    # [,,Keycode.ZIRKUMFLEX],
    [8, 15, Keycode.F4],
    [6, 11, Keycode.TWO],
    [12, 16, Keycode.G],
    [14, 22, Keycode.L],
    [14, 20, Keycode.MINUS],
    [3, 15, Keycode.RIGHT_SHIFT],
    [15, 16, Keycode.SIX],
    [7, 13, Keycode.V],
    [6, 12, Keycode.SPACE],
    [11, 17, Keycode.ZERO],
    [11, 16, Keycode.K],
    [13, 21, Keycode.M],
    [8, 10, Keycode.F3],
    [10, 16, Keycode.F7],
    [10, 20, Keycode.F12],
    [15, 21, Keycode.F9],
    # [,,Keycode.PAUSE],
    [9, 23, Keycode.UP_ARROW],
    [18, 20, Keycode.P],
    [12, 17, Keycode.PERIOD],
    [0, 14, Keycode.LEFT_CONTROL],
    [0, 12, Keycode.RIGHT_CONTROL],
    [3, 18, Keycode.LEFT_SHIFT],
    [1, 11, Keycode.WINDOWS],
    [9, 19, Keycode.RIGHT_BRACKET],
    [11, 22, Keycode.BACKSLASH],
    [18, 22, Keycode.HOME],
    [14, 23, Keycode.END],
    [10, 19, Keycode.KEYPAD_NUMLOCK],
    [15, 19, Keycode.PRINT_SCREEN],
    [0,1,MousecodeLeftClick],
    [2,3,MousecodeRightClick]
]
# list that saves the current state of each key, 1 = released, 0 = pressed
keystatus = [1] * len(keymap)

# try connecting to USB HID, if it fails, reset and try again after 15 seconds.
# (this is needed in my environment because USB devices aren't accepted for the first few seconds)
try:
    kbd = Keyboard(usb_hid.devices)
    mouse = Mouse(usb_hid.devices)
    cc = ConsumerControl(usb_hid.devices)
except:
    print("USB error! Restarting in 15 seconds")
    time.sleep(15)
    microcontroller.reset()

print("HID ok")

uart = busio.UART(board.GP0, board.GP1, baudrate=115200)
print("UART ok")

# which pins is the keyboard ribbon connector connected to?
KBD_pinnumbers = [
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15,
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP21,
    board.GP22,
    board.GP26,
    board.GP27,
    board.GP28,
]

pins = []
for x, p in enumerate(KBD_pinnumbers):
    if x < 24:
        pins.append(digitalio.DigitalInOut(p))
    else:
        pins.append(p)  # mcp pins are already DigitalInOut'ed and can just be copied

# save some RAM by deleting this list we won't use again
del KBD_pinnumbers

# set each pin as input
for p in range(24):
    go_z(p)

print("GPIO KB ok")

mousePolling=0
mousePollingCountAlive=0 #after 500 polls we turn on led

while True:

    for idx, line in enumerate(keymap):  # check each possible combination
        go_0(line[0])
        reading = pins[line[1]].value  # pull down, read, pull up
        go_z(line[0])

        if (not keystatus[idx] == reading):  # key status changed, report it to USB HID keyboard
            keystatus[idx] = reading
            report = (not line[2] == 0)  # FN key isn't reported via USB but handled directly on the pico

            if (keystatus[13] == 0 and reading == 0):  # If FN button is pressed too, handle it as FN-Combination (only on key down)
                report = False
                # customize these FN-combination responses to your liking
                if line[2] == Keycode.DOWN_ARROW:  # volume down
                    cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                if line[2] == Keycode.UP_ARROW:  # volume up
                    cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                if line[2] == Keycode.F3:  # mute / unmute
                    cc.send(ConsumerControlCode.MUTE)

                # if line[2] == Keycode.KEYPAD_NUMLOCK:  # scroll lock
                #    cc.send(ConsumerControlCode.)

                # RECORD = 0xB2
                # FAST_FORWARD = 0xB3
                # REWIND = 0xB4
                # SCAN_NEXT_TRACK = 0xB5
                # SCAN_PREVIOUS_TRACK = 0xB6
                # STOP = 0xB7
                # EJECT = 0xB8
                # PLAY_PAUSE = 0xCD
                # MUTE = 0xE2
                # VOLUME_DECREMENT = 0xEA
                # VOLUME_INCREMENT = 0xE9
                # BRIGHTNESS_DECREMENT = 0x70
                # BRIGHTNESS_INCREMENT = 0x6F

            if report:
                if reading == 0:  # New key pressed
                    if (line[2] == MousecodeLeftClick):
                        mouse.press(Mouse.LEFT_BUTTON)
                    else:
                        if (line[2] == MousecodeRightClick):
                            mouse.press(Mouse.RIGHT_BUTTON)
                        else:
                            kbd.press(line[2])
                else:  # Key released
                    if (line[2] == MousecodeLeftClick):
                        mouse.release(Mouse.LEFT_BUTTON)
                    else:
                        if (line[2] == MousecodeRightClick):
                            mouse.release(Mouse.RIGHT_BUTTON)
                        else:
                            kbd.release(line[2])
        #mouse
        mousePolling+=1
        mousePollingCountAlive+=1
        if mousePolling==20:
            mousePolling=0

            signal = 'M' #mouse
            if (mousePollingCountAlive > 10000):
                signal='H'

            if (mousePollingCountAlive > 10200):
                signal='L'
                mousePollingCountAlive = 0

            uart.write(signal) #M=mouse, H=LED ON, L=LED OFF
            data = uart.readline()
            if data: # b'1000\tx=0\ty=0\r\n'
                decoded_data = data.decode('utf-8')
                parts = decoded_data.split('\t')
                x_part = parts[1]  # Esto será 'x=0'
                y_part = parts[2]  # Esto será 'y=0'
                x_value = int(x_part.split('=')[1])
                y_value = int(y_part.split('=')[1]) * -1
                #print(f"x = {x_value}, y = {y_value}")
                mouse.move(x=x_value, y=y_value)


    #print(mouse_data);

# Write your code here :-)
