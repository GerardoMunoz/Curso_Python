import time
import rp2
from machine import Pin


SM = 0
IR_PIN = 22

PIO_FREQ = 10_000_000

# Como queremos probar inicialmente:
# 1 cuenta ≈ 1 us
OFF_THRESHOLD_US = 20000


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def count1():

    # =====================================================
    # Y = OFF threshold
    # =====================================================

    pull(block)
    mov(y, osr)

    # =====================================================
    # Estado inicial
    # =====================================================

    jmp(pin, "OFF_ON")

    # =====================================================
    # OFF
    # =====================================================

    label("ON_OFF")

    mov(x, y)

    label("OFF_LOOP")

    # -----------------------------------------------------
    # Decrementamos X
    # -----------------------------------------------------

    jmp(x_dec, "OFF_DUMMY")

    
    # -----------------------------------------------------
    # Permanecemos en OFF hasta que aparezca ON
    # -----------------------------------------------------

    label("OFF_SLEEP")

    jmp(pin, "OFF_ON")
    jmp("OFF_SLEEP")


    # -----------------------------------------------------
    # OFF todavía no terminó
    # -----------------------------------------------------

    label("OFF_DUMMY")

    # ¿Terminó OFF porque apareció ON?
    jmp(pin, "OFF_END")

    # Padding
    nop()[6]

    jmp("OFF_LOOP")


    # -----------------------------------------------------
    # OFF ya terminó
    # -----------------------------------------------------

    label("OFF_END")

    mov(isr, invert(x))
    push(noblock)

    jmp("OFF_ON")


    # =====================================================
    # OFF → ON
    # =====================================================

    label("OFF_ON")

    # X = 0xFFFFFFFF
    mov(x, y)


    # =====================================================
    # ON
    # =====================================================

    label("ON_LOOP")

    # Mientras siga ON seguimos contando
    jmp(x_dec, "ON_DUMMY")

    mov(isr, null)
    push(noblock)


    label("ON_DUMMY")

    nop()[7]

    # ¿Seguimos ON?
    jmp(pin, "ON_LOOP")


    # -----------------------------------------------------
    # ON → OFF
    #
    # X contiene el contador restante.
    # Lo enviamos directamente.
    #
    # Al interpretarlo como signed32 será negativo,
    # por lo que Python puede distinguirlo de ON.
    # -----------------------------------------------------

    mov(isr, invert(x))
    push(noblock)

    jmp("ON_OFF")
    

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
sm.put(OFF_THRESHOLD_US)


print("IR reader iniciado")
print("PIO_FREQ:", PIO_FREQ)
print("OFF threshold:", OFF_THRESHOLD_US, "us")
print()


# =========================================================
# Leer FIFO
# =========================================================

while True:

    if sm.rx_fifo()>0:

        raw = sm.get()

        # -------------------------------------------------
        # 0 = OFF timeout
        # -------------------------------------------------

        if raw == 0:
            print("0  -> END")

        # -------------------------------------------------
        # ON / OFF
        # -------------------------------------------------

        else:

            # Convertimos uint32 → int32
            if raw & 0x80000000:
                value = raw - 0x100000000
            else:
                value = raw

            print(value, end=', ')

    time.sleep_ms(1)