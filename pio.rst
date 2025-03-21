Pio  Documentación

https://docs.micropython.org/en/latest/rp2/quickref.html

https://docs.micropython.org/en/latest/rp2/tutorial/pio.html#:~:text=The%20jmp%20%28x_dec%2C%20%22delay_high%22%29%20will%20keep%20looping%20to,the%20jmp%20for%20each%20of%20these%2032%20loops%29.

https://docs.micropython.org/en/v1.17/library/rp2.StateMachine.html

https://docs.micropython.org/en/latest/library/rp2.html

https://github.com/raspberrypi/pico-micropython-examples
https://github.com/raspberrypi/pico-examples

-------------------------------------------


https://docs.micropython.org/en/latest/rp2/quickref.html


.. _rp2_quickref:

Quick reference for the RP2
===========================

.. image:: img/pico_pinout.png
    :alt: Raspberry Pi Pico
    :width: 640px

The Raspberry Pi Pico Development Board (image attribution: Raspberry Pi Foundation).

Below is a quick reference for Raspberry Pi RP2xxx boards.  If it is your first time
working with this board it may be useful to get an overview of the microcontroller:

.. toctree::
   :maxdepth: 1

   general.rst
   tutorial/intro.rst

Installing MicroPython
----------------------

See the corresponding section of tutorial: :ref:`rp2_intro`. It also includes
a troubleshooting subsection.

General board control
---------------------

The MicroPython REPL is accessed via the USB serial port. Tab-completion is useful to
find out what methods an object has. Paste mode (ctrl-E) is useful to paste a
large slab of Python code into the REPL.

The :mod:`machine` module::

    import machine

    machine.freq()          # get the current frequency of the CPU
    machine.freq(240000000) # set the CPU frequency to 240 MHz

The :mod:`rp2` module::

    import rp2

Delay and timing
----------------

Use the :mod:`time <time>` module::

    import time

    time.sleep(1)           # sleep for 1 second
    time.sleep_ms(500)      # sleep for 500 milliseconds
    time.sleep_us(10)       # sleep for 10 microseconds
    start = time.ticks_ms() # get millisecond counter
    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference

Timers
------

RP2040's system timer peripheral provides a global microsecond timebase and
generates interrupts for it.  The software timer is available currently,
and there are unlimited number of them (memory permitting). There is no need
to specify the timer id (id=-1 is supported at the moment) as it will default
to this.

Use the :mod:`machine.Timer` class::

    from machine import Timer

    tim = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
    tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))


.. _rp2_Pins_and_GPIO:

Pins and GPIO
-------------

Use the :ref:`machine.Pin <machine.Pin>` class::

    from machine import Pin

    p0 = Pin(0, Pin.OUT)    # create output pin on GPIO0
    p0.on()                 # set pin to "on" (high) level
    p0.off()                # set pin to "off" (low) level
    p0.value(1)             # set pin to on/high

    p2 = Pin(2, Pin.IN)     # create input pin on GPIO2
    print(p2.value())       # get value, 0 or 1

    p4 = Pin(4, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor
    p5 = Pin(5, Pin.OUT, value=1) # set pin high on creation

Programmable IO (PIO)
---------------------

PIO is useful to build low-level IO interfaces from scratch.  See the :mod:`rp2` module
for detailed explanation of the assembly instructions.

Example using PIO to blink an LED at 1Hz::

    from machine import Pin
    import rp2

    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
    def blink_1hz():
        # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
        set(pins, 1)
        set(x, 31)                  [6]
        label("delay_high")
        nop()                       [29]
        jmp(x_dec, "delay_high")

        # Cycles: 1 + 7 + 32 * (30 + 1) = 1000
        set(pins, 0)
        set(x, 31)                  [6]
        label("delay_low")
        nop()                       [29]
        jmp(x_dec, "delay_low")

    # Create and start a StateMachine with blink_1hz, outputting on Pin(25)
    sm = rp2.StateMachine(0, blink_1hz, freq=2000, set_base=Pin(25))
    sm.active(1)

UART (serial bus)
-----------------

There are two UARTs, UART0 and UART1. UART0 can be mapped to GPIO 0/1, 12/13
and 16/17, and UART1 to GPIO 4/5 and 8/9.


See :ref:`machine.UART <machine.UART>`. ::

    from machine import UART, Pin
    uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
    uart1.write('hello')  # write 5 bytes
    uart1.read(5)         # read up to 5 bytes

.. note::

    REPL over UART is disabled by default. You can see the :ref:`rp2_intro` for
    details on how to enable REPL over UART.


PWM (pulse width modulation)
----------------------------

There are 8 independent PWM generators called slices, which each have two
channels making it 16 PWM channels in total which can be clocked from
8Hz to 62.5Mhz at a machine.freq() of 125Mhz. The two channels of a
slice run at the same frequency, but can have a different duty rate.
The two channels are usually assigned to adjacent GPIO pin pairs with
even/odd numbers. So GPIO0 and GPIO1 are at slice 0, GPIO2 and GPIO3
are at slice 1, and so on. A certain channel can be assigned to
different GPIO pins (see Pinout). For instance slice 0, channel A can be assigned
to both GPIO0 and GPIO16.

Use the ``machine.PWM`` class::

    from machine import Pin, PWM

    # create PWM object from a pin and set the frequency of slice 0
    # and duty cycle for channel A
    pwm0 = PWM(Pin(0), freq=2000, duty_u16=32768)
    pwm0.freq()             # get the current frequency of slice 0
    pwm0.freq(1000)         # set/change the frequency of slice 0
    pwm0.duty_u16()         # get the current duty cycle of channel A, range 0-65535
    pwm0.duty_u16(200)      # set the duty cycle of channel A, range 0-65535
    pwm0.duty_u16(0)        # stop the output at channel A
    print(pwm0)             # show the properties of the PWM object.
    pwm0.deinit()           # turn off PWM of slice 0, stopping channels A and B

ADC (analog to digital conversion)
----------------------------------

RP2040 has five ADC channels in total, four of which are 12-bit SAR based
ADCs: GP26, GP27, GP28 and GP29. The input signal for ADC0, ADC1, ADC2 and
ADC3 can be connected with GP26, GP27, GP28, GP29 respectively (On Pico board,
GP29 is connected to VSYS). The standard ADC range is 0-3.3V. The fifth
channel is connected to the in-built temperature sensor and can be used for
measuring the temperature.

Use the :ref:`machine.ADC <machine.ADC>` class::

    from machine import ADC, Pin
    adc = ADC(Pin(26))     # create ADC object on ADC pin
    adc.read_u16()         # read value, 0-65535 across voltage range 0.0v - 3.3v

Software SPI bus
----------------

Software SPI (using bit-banging) works on all pins, and is accessed via the
:ref:`machine.SoftSPI <machine.SoftSPI>` class::

    from machine import Pin, SoftSPI

    # construct a SoftSPI bus on the given pins
    # polarity is the idle state of SCK
    # phase=0 means sample on the first edge of SCK, phase=1 means the second
    spi = SoftSPI(baudrate=100_000, polarity=1, phase=0, sck=Pin(0), mosi=Pin(2), miso=Pin(4))

    spi.init(baudrate=200000) # set the baudrate

    spi.read(10)            # read 10 bytes on MISO
    spi.read(10, 0xff)      # read 10 bytes while outputting 0xff on MOSI

    buf = bytearray(50)     # create a buffer
    spi.readinto(buf)       # read into the given buffer (reads 50 bytes in this case)
    spi.readinto(buf, 0xff) # read into the given buffer and output 0xff on MOSI

    spi.write(b'12345')     # write 5 bytes on MOSI

    buf = bytearray(4)      # create a buffer
    spi.write_readinto(b'1234', buf) # write to MOSI and read from MISO into the buffer
    spi.write_readinto(buf, buf) # write buf to MOSI and read MISO back into buf

.. Warning::
   Currently *all* of ``sck``, ``mosi`` and ``miso`` *must* be specified when
   initialising Software SPI.

Hardware SPI bus
----------------

The RP2040 has 2 hardware SPI buses which is accessed via the
:ref:`machine.SPI <machine.SPI>` class and has the same methods as software
SPI above::

    from machine import Pin, SPI

    spi = SPI(1, 10_000_000)  # Default assignment: sck=Pin(10), mosi=Pin(11), miso=Pin(8)
    spi = SPI(1, 10_000_000, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
    spi = SPI(0, baudrate=80_000_000, polarity=0, phase=0, bits=8, sck=Pin(6), mosi=Pin(7), miso=Pin(4))

Software I2C bus
----------------

Software I2C (using bit-banging) works on all output-capable pins, and is
accessed via the :ref:`machine.SoftI2C <machine.SoftI2C>` class::

    from machine import Pin, SoftI2C

    i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100_000)

    i2c.scan()              # scan for devices

    i2c.readfrom(0x3a, 4)   # read 4 bytes from device with address 0x3a
    i2c.writeto(0x3a, '12') # write '12' to device with address 0x3a

    buf = bytearray(10)     # create a buffer with 10 bytes
    i2c.writeto(0x3a, buf)  # write the given buffer to the peripheral

Hardware I2C bus
----------------

The driver is accessed via the :ref:`machine.I2C <machine.I2C>` class and
has the same methods as software I2C above::

    from machine import Pin, I2C

    i2c = I2C(0)   # default assignment: scl=Pin(9), sda=Pin(8)
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)

I2S bus
-------

See :ref:`machine.I2S <machine.I2S>`. ::

    from machine import I2S, Pin

    i2s = I2S(0, sck=Pin(16), ws=Pin(17), sd=Pin(18), mode=I2S.TX, bits=16, format=I2S.STEREO, rate=44100, ibuf=40000) # create I2S object
    i2s.write(buf)             # write buffer of audio samples to I2S device

    i2s = I2S(1, sck=Pin(0), ws=Pin(1), sd=Pin(2), mode=I2S.RX, bits=16, format=I2S.MONO, rate=22050, ibuf=40000) # create I2S object
    i2s.readinto(buf)          # fill buffer with audio samples from I2S device

The ``ws`` pin number must be one greater than the ``sck`` pin number.

The I2S class is currently available as a Technical Preview.  During the preview period, feedback from
users is encouraged.  Based on this feedback, the I2S class API and implementation may be changed.

Two I2S buses are supported with id=0 and id=1.

Real time clock (RTC)
---------------------

See :ref:`machine.RTC <machine.RTC>` ::

    from machine import RTC

    rtc = RTC()
    rtc.datetime((2017, 8, 23, 2, 12, 48, 0, 0)) # set a specific date and
                                                 # time, eg. 2017/8/23 1:12:48
    rtc.datetime() # get date and time

WDT (Watchdog timer)
--------------------

The RP2040 has a watchdog which is a countdown timer that can restart
parts of the chip if it reaches zero.

See :ref:`machine.WDT <machine.WDT>`. ::

    from machine import WDT

    # enable the WDT with a timeout of 5s (1s is the minimum)
    wdt = WDT(timeout=5000)
    wdt.feed()

The maximum value for timeout is 8388 ms.

OneWire driver
--------------

The OneWire driver is implemented in software and works on all pins::

    from machine import Pin
    import onewire

    ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
    ow.scan()               # return a list of devices on the bus
    ow.reset()              # reset the bus
    ow.readbyte()           # read a byte
    ow.writebyte(0x12)      # write a byte on the bus
    ow.write('123')         # write bytes on the bus
    ow.select_rom(b'12345678') # select a specific device by its ROM code

There is a specific driver for DS18S20 and DS18B20 devices::

    import time, ds18x20
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(ds.read_temp(rom))

Be sure to put a 4.7k pull-up resistor on the data line.  Note that
the ``convert_temp()`` method must be called each time you want to
sample the temperature.

NeoPixel and APA106 driver
--------------------------

Use the ``neopixel`` and ``apa106`` modules::

    from machine import Pin
    from neopixel import NeoPixel

    pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
    np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels
    np[0] = (255, 255, 255) # set the first pixel to white
    np.write()              # write data to all pixels
    r, g, b = np[0]         # get first pixel colour


The APA106 driver extends NeoPixel, but internally uses a different colour order::

    from apa106 import APA106
    ap = APA106(pin, 8)
    r, g, b = ap[0]

APA102 (DotStar) uses a different driver as it has an additional clock pin.








































https://docs.micropython.org/en/latest/rp2/tutorial/pio.html#:~:text=The%20jmp%20%28x_dec%2C%20%22delay_high%22%29%20will%20keep%20looping%20to,the%20jmp%20for%20each%20of%20these%2032%20loops%29.


Programmable IO
===============

The RP2040 has hardware support for standard communication protocols like I2C,
SPI and UART. For protocols where there is no hardware support, or where there
is a requirement of custom I/O behaviour, Programmable Input Output (PIO) comes
into play.  Also, some MicroPython applications make use of a technique called
bit banging in which pins are rapidly turned on and off to transmit data.  This
can make the entire process slow as the processor concentrates on bit banging
rather than executing other logic.  However, PIO allows bit banging to happen
in the background while the CPU is executing the main work.

Along with the two central Cortex-M0+ processing cores, the RP2040 has two PIO
blocks each of which has four independent state machines.  These state machines
can transfer data to/from other entities using First-In-First-Out (FIFO) buffers,
which allow the state machine and main processor to work independently yet also
synchronise their data.  Each FIFO has four words (each of 32 bits) which can be
linked to the DMA to transfer larger amounts of data.

All PIO instructions follow a common pattern::

    <instruction> .side(<side_set_value>) [<delay_value>]

The side-set ``.side(...)`` and delay ``[...]`` parts are both optional, and if
specified allow the instruction to perform more than one operation.  This keeps
PIO programs small and efficient.

There are nine instructions which perform the following tasks:

- ``jmp()`` transfers control to a different part of the code
- ``wait()`` pauses until a particular action happens
- ``in_()`` shifts the bits from a source (scratch register or set of pins) to the
  input shift register
- ``out()`` shifts the bits from the output shift register to a destination
- ``push()`` sends data to the RX FIFO
- ``pull()`` receives data from the TX FIFO
- ``mov()`` moves data from a source to a destination
- ``irq()`` sets or clears an IRQ flag
- ``set()`` writes a literal value to a destination

The instruction modifiers are:

- ``.side()`` sets the side-set pins at the start of the instruction
- ``[]`` delays for a certain number of cycles after execution of the instruction

There are also directives:

- ``wrap_target()`` specifies where the program execution will get continued from
- ``wrap()`` specifies the instruction where the control flow of the program will
  get wrapped from
- ``label()`` sets a label for use with ``jmp()`` instructions
- ``word()`` emits a raw 16-bit value which acts as an instruction in the program

An example
----------

Take the ``pio_1hz.py`` example for a simple understanding of how to use the PIO
and state machines. Below is the code for reference.

.. code-block:: python3

    # Example using PIO to blink an LED and raise an IRQ at 1Hz.

    import time
    from machine import Pin
    import rp2


    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
    def blink_1hz():
        # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
        irq(rel(0))
        set(pins, 1)
        set(x, 31)                  [5]
        label("delay_high")
        nop()                       [29]
        jmp(x_dec, "delay_high")

        # Cycles: 1 + 1 + 6 + 32 * (30 + 1) = 1000
        nop()
        set(pins, 0)
        set(x, 31)                  [5]
        label("delay_low")
        nop()                       [29]
        jmp(x_dec, "delay_low")


    # Create the StateMachine with the blink_1hz program, outputting on Pin(25).
    sm = rp2.StateMachine(0, blink_1hz, freq=2000, set_base=Pin(25))

    # Set the IRQ handler to print the millisecond timestamp.
    sm.irq(lambda p: print(time.ticks_ms()))

    # Start the StateMachine.
    sm.active(1)

This creates an instance of class :class:`rp2.StateMachine` which runs the
``blink_1hz`` program at 2000Hz, and connects to pin 25.  The ``blink_1hz``
program uses the PIO to blink an LED connected to this pin at 1Hz, and also
raises an IRQ as the LED turns on.  This IRQ then calls the ``lambda`` function
which prints out a millisecond timestamp.

The ``blink_1hz`` program is a PIO assembler routine.  It connects to a single
pin which is configured as an output and starts out low.  The instructions do
the following:

- ``irq(rel(0))`` raises the IRQ associated with the state machine.
- The LED is turned on via the ``set(pins, 1)`` instruction.
- The value 31 is put into register X, and then there is a delay for 5 more
  cycles, specified by the ``[5]``.
- The ``nop() [29]`` instruction waits for 30 cycles.
- The ``jmp(x_dec, "delay_high")`` will keep looping to the ``delay_high`` label
  as long as the register X is non-zero, and will also post-decrement X.  Since
  X starts with the value 31 this jump will happen 31 times, so the ``nop() [29]``
  runs 32 times in total (note there is also one instruction cycle taken by the
  ``jmp`` for each of these 32 loops).
- The single ``nop()`` correlates with the cycle used for IRQ raise, and ensures
  the same number of cycles are used for LED on and LED off.
- ``set(pins, 0)`` will turn the LED off by setting pin 25 low.
- Another 32 loops of ``nop() [29]`` and ``jmp(...)`` will execute.
- Because ``wrap_target()`` and ``wrap()`` are not specified, their default will
  be used and execution of the program will wrap around from the bottom to the
  top.  This wrapping does not cost any execution cycles.

The entire routine takes exactly 2000 cycles of the state machine.  Setting the
frequency of the state machine to 2000Hz makes the LED blink at 1Hz.

-------------------------------




























https://docs.micropython.org/en/v1.17/library/rp2.StateMachine.html

.. currentmodule:: rp2
.. _rp2.StateMachine:

class StateMachine -- access to the RP2040's programmable I/O interface
=======================================================================

The :class:`StateMachine` class gives access to the RP2040's PIO (programmable
I/O) interface.

For assembling PIO programs, see :func:`rp2.asm_pio`.


Constructors
------------

.. class:: StateMachine(id, [program, ...])

    Get the state machine numbered *id*. The RP2040 has two identical PIO
    instances, each with 4 state machines: so there are 8 state machines in
    total, numbered 0 to 7.

    Optionally initialize it with the given program *program*: see
    `StateMachine.init`.


Methods
-------

.. method:: StateMachine.init(program, freq=-1, *, in_base=None, out_base=None, set_base=None, jmp_pin=None, sideset_base=None, in_shiftdir=None, out_shiftdir=None, push_thresh=None, pull_thresh=None)

    Configure the state machine instance to run the given *program*.

    The program is added to the instruction memory of this PIO instance. If the
    instruction memory already contains this program, then its offset is
    re-used so as to save on instruction memory.

    - *freq* is the frequency in Hz to run the state machine at. Defaults to
      the system clock frequency.

      The clock divider is computed as ``system clock frequency / freq``, so
      there can be slight rounding errors.

      The minimum possible clock divider is one 65536th of the system clock: so
      at the default system clock frequency of 125MHz, the minimum value of
      *freq* is ``1908``. To run state machines at slower frequencies, you'll
      need to reduce the system clock speed with `machine.freq()`.
    - *in_base* is the first pin to use for ``in()`` instructions.
    - *out_base* is the first pin to use for ``out()`` instructions.
    - *set_base* is the first pin to use for ``set()`` instructions.
    - *jmp_pin* is the first pin to use for ``jmp(pin, ...)`` instructions.
    - *sideset_base* is the first pin to use for side-setting.
    - *in_shiftdir* is the direction the ISR will shift, either
      `PIO.SHIFT_LEFT` or `PIO.SHIFT_RIGHT`.
    - *out_shiftdir* is the direction the OSR will shift, either
      `PIO.SHIFT_LEFT` or `PIO.SHIFT_RIGHT`.
    - *push_thresh* is the threshold in bits before auto-push or conditional
      re-pushing is triggered.
    - *pull_thresh* is the threshold in bits before auto-push or conditional
      re-pushing is triggered.

.. method:: StateMachine.active([value])

    Gets or sets whether the state machine is currently running.

    >>> sm.active()
    True
    >>> sm.active(0)
    False

.. method:: StateMachine.restart()

    Restarts the state machine and jumps to the beginning of the program.

    This method clears the state machine's internal state using the RP2040's
    ``SM_RESTART`` register. This includes:

     - input and output shift counters
     - the contents of the input shift register
     - the delay counter
     - the waiting-on-IRQ state
     - a stalled instruction run using `StateMachine.exec()`

.. method:: StateMachine.exec(instr)

    Execute a single PIO instruction. Uses `asm_pio_encode` to encode the
    instruction from the given string *instr*.

    >>> sm.exec("set(0, 1)")

.. method:: StateMachine.get(buf=None, shift=0)

    Pull a word from the state machine's RX FIFO.

    If the FIFO is empty, it blocks until data arrives (i.e. the state machine
    pushes a word).

    The value is shifted right by *shift* bits before returning, i.e. the
    return value is ``word >> shift``.

.. method:: StateMachine.put(value, shift=0)

    Push a word onto the state machine's TX FIFO.

    If the FIFO is full, it blocks until there is space (i.e. the state machine
    pulls a word).

    The value is first shifted left by *shift* bits, i.e. the state machine
    receives ``value << shift``.

.. method:: StateMachine.rx_fifo()

    Returns the number of words in the state machine's RX FIFO. A value of 0
    indicates the FIFO is empty.

    Useful for checking if data is waiting to be read, before calling
    `StateMachine.get()`.

.. method:: StateMachine.tx_fifo()

    Returns the number of words in the state machine's TX FIFO. A value of 0
    indicates the FIFO is empty.

    Useful for checking if there is space to push another word using
    `StateMachine.put()`.

.. method:: StateMachine.irq(handler=None, trigger=0|1, hard=False)

     Returns the IRQ object for the given StateMachine.

     Optionally configure it.

----------------------------








https://docs.micropython.org/en/latest/library/rp2.html



.. currentmodule:: rp2

:mod:`rp2` --- functionality specific to the RP2040
===================================================

.. module:: rp2
    :synopsis: functionality specific to the RP2

The ``rp2`` module contains functions and classes specific to the RP2040, as
used in the Raspberry Pi Pico.

See the `RP2040 Python datasheet
<https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf>`_
for more information, and `pico-micropython-examples
<https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio>`_
for example code.


PIO related functions
---------------------

The ``rp2`` module includes functions for assembling PIO programs.

For running PIO programs, see :class:`rp2.StateMachine`.

.. function:: asm_pio(*, out_init=None, set_init=None, sideset_init=None, in_shiftdir=0, out_shiftdir=0, autopush=False, autopull=False, push_thresh=32, pull_thresh=32, fifo_join=PIO.JOIN_NONE)

    Assemble a PIO program.

    The following parameters control the initial state of the GPIO pins, as one
    of `PIO.IN_LOW`, `PIO.IN_HIGH`, `PIO.OUT_LOW` or `PIO.OUT_HIGH`. If the
    program uses more than one pin, provide a tuple, e.g.
    ``out_init=(PIO.OUT_LOW, PIO.OUT_LOW)``.

    - *out_init* configures the pins used for ``out()`` instructions.
    - *set_init* configures the pins used for ``set()`` instructions. There can
      be at most 5.
    - *sideset_init* configures the pins used side-setting. There can be at
      most 5.

    The following parameters are used by default, but can be overridden in
    `StateMachine.init()`:

    - *in_shiftdir* is the default direction the ISR will shift, either
      `PIO.SHIFT_LEFT` or `PIO.SHIFT_RIGHT`.
    - *out_shiftdir* is the default direction the OSR will shift, either
      `PIO.SHIFT_LEFT` or `PIO.SHIFT_RIGHT`.
    - *push_thresh* is the threshold in bits before auto-push or conditional
      re-pushing is triggered.
    - *pull_thresh* is the threshold in bits before auto-pull or conditional
      re-pulling is triggered.

    The remaining parameters are:

    - *autopush* configures whether auto-push is enabled.
    - *autopull* configures whether auto-pull is enabled.
    - *fifo_join* configures whether the 4-word TX and RX FIFOs should be
      combined into a single 8-word FIFO for one direction only. The options
      are `PIO.JOIN_NONE`, `PIO.JOIN_RX` and `PIO.JOIN_TX`.

.. function:: asm_pio_encode(instr, sideset_count, sideset_opt=False)

    Assemble a single PIO instruction. You usually want to use `asm_pio()`
    instead.

    >>> rp2.asm_pio_encode("set(0, 1)", 0)
    57345

.. function:: bootsel_button()

    Temporarily turns the QSPI_SS pin into an input and reads its value,
    returning 1 for low and 0 for high.
    On a typical RP2040 board with a BOOTSEL button, a return value of 1
    indicates that the button is pressed.

    Since this function temporarily disables access to the external flash
    memory, it also temporarily disables interrupts and the other core to
    prevent them from trying to execute code from flash.

.. class:: PIOASMError

    This exception is raised from `asm_pio()` or `asm_pio_encode()` if there is
    an error assembling a PIO program.


PIO assembly language instructions
----------------------------------

PIO state machines are programmed in a custom assembly language with nine core
PIO-machine instructions.  In MicroPython, PIO assembly routines are written as
a Python function with the decorator ``@rp2.asm_pio()``, and they use Python
syntax.  Such routines support standard Python variables and arithmetic, as well
as the following custom functions that encode PIO instructions and direct the
assembler.  See sec 3.4 of the RP2040 datasheet for further details.

wrap_target()
    Specify the location where execution continues after program wrapping.
    By default this is the start of the PIO routine.

wrap()
    Specify the location where the program finishes and wraps around.
    If this directive is not used then it is added automatically at the end of
    the PIO routine.  Wrapping does not cost any execution cycles.

label(label)
    Define a label called *label* at the current location.  *label* can be a
    string or integer.

word(instr, label=None)
    Insert an arbitrary 16-bit word in the assembled output.

    - *instr*: the 16-bit value
    - *label*: if given, look up the label and logical-or the label's value with
      *instr*

jmp(...)
    This instruction takes two forms:

    jmp(label)
        - *label*: label to jump to unconditionally

    jmp(cond, label)
        - *cond*: the condition to check, one of:

            - ``not_x``, ``not_y``: true if register is zero
            - ``x_dec``, ``y_dec``: true if register is non-zero, and do post
              decrement
            - ``x_not_y``: true if X is not equal to Y
            - ``pin``: true if the input pin is set
            - ``not_osre``: true if OSR is not empty (hasn't reached its
              threshold)

        - *label*: label to jump to if condition is true

wait(polarity, src, index)
    Block, waiting for high/low on a pin or IRQ line.

    - *polarity*: 0 or 1, whether to wait for a low or high value
    - *src*: one of: ``gpio`` (absolute pin), ``pin`` (pin relative to
      StateMachine's ``in_base`` argument), ``irq``
    - *index*: 0-31, the index for *src*

in_(src, bit_count)
    Shift data in from *src* to ISR.

    - *src*: one of: ``pins``, ``x``, ``y``, ``null``, ``isr``, ``osr``
    - *bit_count*: number of bits to shift in (1-32)

out(dest, bit_count)
    Shift data out from OSR to *dest*.

    - *dest*: one of: ``pins``, ``x``, ``y``, ``pindirs``, ``pc``, ``isr``,
      ``exec``
    - *bit_count*: number of bits to shift out (1-32)

push(...)
    Push ISR to the RX FIFO, then clear ISR to zero.
    This instruction takes the following forms:

    - push()
    - push(block)
    - push(noblock)
    - push(iffull)
    - push(iffull, block)
    - push(iffull, noblock)

    If ``block`` is used then the instruction stalls if the RX FIFO is full.
    The default is to block.  If ``iffull`` is used then it only pushes if the
    input shift count has reached its threshold.

pull(...)
    Pull from the TX FIFO into OSR.
    This instruction takes the following forms:

    - pull()
    - pull(block)
    - pull(noblock)
    - pull(ifempty)
    - pull(ifempty, block)
    - pull(ifempty, noblock)

    If ``block`` is used then the instruction stalls if the TX FIFO is empty.
    The default is to block.  If ``ifempty`` is used then it only pulls if the
    output shift count has reached its threshold.

mov(dest, src)
    Move into *dest* the value from *src*.

    - *dest*: one of: ``pins``, ``x``, ``y``, ``exec``, ``pc``, ``isr``, ``osr``
    - *src*: one of: ``pins``, ``x``, ``y``, ``null``, ``status``, ``isr``,
      ``osr``; this argument can be optionally modified by wrapping it in
      ``invert()`` or ``reverse()`` (but not both together)

irq(...)
    Set or clear an IRQ flag.
    This instruction takes two forms:

    irq(index)
        - *index*: 0-7, or ``rel(0)`` to ``rel(7)``

    irq(mode, index)
        - *mode*: one of: ``block``, ``clear``
        - *index*: 0-7, or ``rel(0)`` to ``rel(7)``

    If ``block`` is used then the instruction stalls until the flag is cleared
    by another entity.  If ``clear`` is used then the flag is cleared instead of
    being set.  Relative IRQ indices add the state machine ID to the IRQ index
    with modulo-4 addition.  IRQs 0-3 are visible from to the processor, 4-7 are
    internal to the state machines.

set(dest, data)
    Set *dest* with the value *data*.

    - *dest*: ``pins``, ``x``, ``y``, ``pindirs``
    - *data*: value (0-31)

nop()
    This is a pseudoinstruction that assembles to ``mov(y, y)`` and has no side
    effect.

.side(value)
    This is a modifier which can be applied to any instruction, and is used to
    control side-set pin values.

    - *value*: the value (bits) to output on the side-set pins

.delay(value)
    This is a modifier which can be applied to any instruction, and specifies
    how many cycles to delay for after the instruction executes.

    - *value*: cycles to delay, 0-31 (maximum value reduced if side-set pins are
      used)

[value]
    This is a modifier and is equivalent to ``.delay(value)``.


Classes
-------

.. toctree::
    :maxdepth: 1

    rp2.Flash.rst
    rp2.PIO.rst
    rp2.StateMachine.rst
--------------------------------
https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

__________________________
