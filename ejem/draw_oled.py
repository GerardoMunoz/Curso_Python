import board
import busio
import adafruit_ssd1306

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

