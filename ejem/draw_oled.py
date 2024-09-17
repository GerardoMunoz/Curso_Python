

import board
import busio
import adafruit_ssd1306 #https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20240910/adafruit-circuitpython-bundle-9.x-mpy-20240910.zip
                        #https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/
                        # extract the files 'adafruit_ssd1306.mpy', 'adafruit_framebuf.mpy' and save in the dir '/lib'
SCL, SDA = board.GP17, board.GP16
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
display.fill(0)
display.show()
draw = [
    "         **         ",
    "      **    **      ",
    "    **        **    ",
    "  **            **  ",
    " **              ** ",
    " **    **  **    ** ",
    " **              ** ",
    "  **            **  ",
    "    **        **    ",
    "      **    **      ",
    "         **         ",
    "         **         ",
    "      **    **      ",
    "    **        **    ",
    "  **            **  ",
    " **              ** ",
    " **    **  **    ** ",
    " **              ** ",
    "  **            **  ",
    "    **        **    ",
    "      **    **      ",
    "         **         ",
    "      **    **      ",
    "    **        **    ",
    "  **            **  ",
    " **              ** ",
    " **    **  **    ** ",
    " **              ** ",
    "  **            **  ",
    "    **        **    ",
    "      **    **      ",
    "      **    **      ",
    ]

rows = len(draw)
columns = len(draw[0])
columns2=128
print('rows,columns',rows,columns)
image_bytearray = bytearray(rows * columns)
image_bytearray[0]=columns
for i in range(0,rows,8):
    for j in range(columns):
        #print('i,j,k',i,j)
        a=sum(0 if draw[i+k][j]==" " else 2**k for k in range(8))
        display.buffer[i*columns2//8+j+1]=a
display.show()

