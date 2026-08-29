import time
import rp2
from machine import Pin


SM = 0
IR_PIN = 22

PIO_FREQ = 10_000_000

# Como queremos probar inicialmente:
# 1 cuenta ≈ 1 us
on_THRESHOLD_US = 20000


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def count1():

    # =====================================================
    # Y = on threshold
    # =====================================================

    pull(block)
    mov(y, osr)

    # =====================================================
    # Estado inicial
    # =====================================================

    jmp(pin, "on_off")

    # =====================================================
    # on
    # =====================================================

    label("off_on")

    mov(x, y)

    label("on_LOOP")

    # -----------------------------------------------------
    # Decrementamos X
    # -----------------------------------------------------

    jmp(x_dec, "on_DUMMY") #1

    
    # -----------------------------------------------------
    # Permanecemos en on hasta que aparezca off
    # -----------------------------------------------------

    label("on_SLEEP")

    jmp(pin, "on_off")
    jmp("on_SLEEP")


    # -----------------------------------------------------
    # on todavía no terminó
    # -----------------------------------------------------

    label("on_DUMMY") 

    # ¿Terminó on porque apareció off?
    jmp(pin, "on_END") #2

    # Padding
    nop()[6]           #3

    jmp("on_LOOP")     #4


    # -----------------------------------------------------
    # on ya terminó
    # -----------------------------------------------------

    label("on_END")

    mov(isr, invert(x))#
    push(noblock)

    jmp("on_off")


    # =====================================================
    # on → off
    # =====================================================

    label("on_off")

    # X = 0xFFFFFFFF
    mov(x, y)


    # =====================================================
    # off
    # =====================================================

    label("off_LOOP")

    # Mientras siga off seguimos contando
    jmp(x_dec, "off_DUMMY") #1

    mov(isr, null)
    push(noblock)

    # Si pasa on_THRESHOLD_US esperamos el cero

    label("off_SLEEP")
    jmp(pin,"off_SLEEP")
    jmp("off_on")

    label("off_DUMMY")

    nop()[7]             #2

    # ¿Seguimos off?
    jmp(pin, "off_LOOP")  #3


    # -----------------------------------------------------
    # off → on
    #
    # X contiene el contador restante.
    # Lo enviamos directamente.
    #
    # Al interpretarlo como signed32 será negativo,
    # por lo que Python puede distinguirlo de off.
    # -----------------------------------------------------

    mov(isr, x)#
    push(noblock)

    jmp("off_on")
    

# =========================================================
# State Machine
# =========================================================

sm = rp2.StateMachine(
    SM,
    count1,
    freq=PIO_FREQ,
    jmp_pin=Pin(IR_PIN, Pin.IN, Pin.PULL_UP)
)

sm.active(1)

# Cargar threshold
sm.put(on_THRESHOLD_US)


print("IR reader iniciado")
print("PIO_FREQ:", PIO_FREQ)
print("on threshold:", on_THRESHOLD_US, "us")
print()


# =========================================================
# Leer FIFO
# =========================================================

while True:

    if sm.rx_fifo()>0:

        raw = sm.get()

        # -------------------------------------------------
        # 0 = on timeout
        # -------------------------------------------------

        if raw == 0:
            print("0  -> END")

        # -------------------------------------------------
        # off / on
        # -------------------------------------------------

        else:

            # Convertimos uint32 → int32
            if raw & 0x80000000:
                value = 0x100000000 -raw-on_THRESHOLD_US
            else:
                value = on_THRESHOLD_US-raw

            print(-value, end=', ')

    #time.sleep_ms(1)