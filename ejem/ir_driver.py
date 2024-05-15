import time
import rp2
from machine import Pin
import asyncio

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def count():
    label('inicio')
    mov(x,invert(null))
    jmp(pin,'uno')
    label('cero')
    nop()
    jmp(x_dec,'cero_bis')
    jmp('fin')
    label('cero_bis')
    jmp(pin,'fin')
    jmp('cero')
    label('uno')
    nop()
    jmp(x_dec,'uno_bis')
    jmp('fin')
    label('uno_bis')
    nop()
    jmp(pin,'uno')
    label('fin')
    mov(isr,x)
    push(noblock)
    jmp('inicio')

   


class Ir_reader:
    def __init__(self,sm, pin_ir, max_wait=18000, one_zero_th=1000, max_valid=3000):
        """
        sm: number of state machine
        pin_ir: GP PIN for the ir sensor
        """
        self.max_wait = max_wait
        self.one_zero_th = one_zero_th
        self.max_valid = max_valid
        self.sm = rp2.StateMachine(
            sm,
            count,
            freq=38000*100,
            jmp_pin= Pin(pin_ir, Pin.IN, Pin.PULL_UP)
        )
        self.sm.active(1)
        self.codes={
            '0000000000000000010101010101010100010100010000000100000100010101010':"0",
            '0000000000000000010101010101010100000101000000000101000001010101010':"1",
            '0000000000000000010101010101010100000001010000000101010000010101010':"2",
            '0000000000000000010101010101010100010101010001000100000000010001010':"3",
            '0000000000000000010101010101010100000001000000000101010001010101010':"4",
            '0000000000000000010101010101010100000101010000000101000000010101010':"5",
            '0000000000000000010101010101010100010001010001000100010000010001010':"6",
            '0000000000000000010101010101010100010000000001000100010101010001010':"7",
            '0000000000000000010101010101010100010000010001000100010100010001010':"8",
            '0000000000000000010101010101010100010001000001000100010001010001010':"9",
            '0000000000000000010101010101010101000100010000000001000100010101010':"+"
        }



    async def read_elapsed(self,timeout_ms=100):
        start_ms=time.ticks_ms()
        
        while timeout_ms==-1 or time.ticks_ms()-start_ms<timeout_ms:
            if self.sm.rx_fifo()!=0:
                return self.sm.get()
            else:
                await asyncio.sleep_ms(1) 
        await asyncio.sleep_ms(1)
        return -1

    async def read_button(self,eo=True):
        elapsed=0
        
        even_odd = eo
        code=""
        while elapsed < self.max_wait:
            dat=await self.read_elapsed()
            if dat== -1 and code!="":
                return code
            dat=2**32-dat
            if even_odd and dat<self.max_valid:
                code += "0" if dat<self.one_zero_th else "1"
        return code


# Example for two IR sensors, for GP16 and GP17
if __name__=="__main__":

    async def read_code(sm, pin):
        obj = Ir_reader(sm,pin)
        while True:
            result =  await obj.read_button()
            if result in obj.codes:
                result1 = obj.codes[result]
            else:
                print(result)
                result1="-"
                
            print(pin, "Received:", len(result), result,result1)


    async def main():
        task_1 = asyncio.create_task(read_code(1,17))
        task_2 = asyncio.create_task(read_code(0,16))
        await asyncio.gather(task_1,task_2)

    asyncio.run(main())

