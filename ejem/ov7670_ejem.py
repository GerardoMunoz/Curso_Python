#https://docs.circuitpython.org/projects/ov7670/en/latest/examples.html
# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

The camera is placed in YUV mode, so the top 8 bits of each color
value can be treated as "greyscale".

It's important that you use a terminal program that can interpret
"ANSI" escape sequences.  The demo uses them to "paint" each frame
on top of the prevous one, rather than scrolling.

Remember to take the lens cap off, or un-comment the line setting
the test pattern!
"""

import sys
import time

import digitalio
import busio
import board

from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
    OV7670_TEST_PATTERN_COLOR_BAR_FADE,
)

# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus

#with digitalio.DigitalInOut(board.D39) as shutdown:
#    shutdown.switch_to_output(True)
#    time.sleep(0.001)
cam_bus = busio.I2C(board.GP21, board.GP20)

cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP9,
    shutdown=board.GP15,
    reset=board.GP14,
)
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = True

print(cam.width, cam.height)

buf = bytearray(2 * cam.width * cam.height)
print('##################################')
print(buf)
cam.capture(buf)
print('##################################')
print(len(buf))
print('##################################')
print(len(list(buf)))


chars = b" .:-=+*#%@"

width = cam.width
row = bytearray(2 * width)
while True:

    cam.capture(buf)
    for j in range(cam.height):
        for i in range(cam.width):
            row[i * 2] = row[i * 2 + 1] = chars[
                buf[2 * (width * j + i)] * (len(chars) - 1) // 255
            ]
        print(row)
    print()
    time.sleep(2)
