from uctypes import BF_POS, BF_LEN, UINT32, BFUINT32, struct
import time

# Dirección base del RTC
RTC_BASE = 0x4005c000

# Campos del registro CLKDIV_M1
CLKDIV_M1_FIELDS = {
    "DIVIDER": 0 << BF_POS | 16 << BF_LEN | BFUINT32
}

# Campos del registro SETUP_0
SETUP_0_FIELDS = {
    "YEAR": 12 << BF_POS | 12 << BF_LEN | BFUINT32,
    "MONTH": 8 << BF_POS | 4 << BF_LEN | BFUINT32,
    "DAY": 0 << BF_POS | 5 << BF_LEN | BFUINT32
}

# Campos del registro SETUP_1
SETUP_1_FIELDS = {
    "DOTW": 24 << BF_POS | 3 << BF_LEN | BFUINT32,
    "HOUR": 16 << BF_POS | 5 << BF_LEN | BFUINT32,
    "MIN": 8 << BF_POS | 6 << BF_LEN | BFUINT32,
    "SEC": 0 << BF_POS | 6 << BF_LEN | BFUINT32
}

# Campos del registro CTRL
CTRL_FIELDS = {
    "FORCE_NOTLEAP_YEAR": 8 << BF_POS | 1 << BF_LEN | BFUINT32,
    "LOAD": 4 << BF_POS | 1 << BF_LEN | BFUINT32,
    "RTC_ACTIVE": 1 << BF_POS | 1 << BF_LEN | BFUINT32,
    "RTC_ENABLE": 0 << BF_POS | 1 << BF_LEN | BFUINT32
}

# Campos del registro IRQ_SETUP_0
IRQ_SETUP_0_FIELDS = {
    "MATCH_ENA": 28 << BF_POS | 1 << BF_LEN | BFUINT32,
    "YEAR_ENA": 26 << BF_POS | 1 << BF_LEN | BFUINT32,
    "MONTH_ENA": 25 << BF_POS | 1 << BF_LEN | BFUINT32,
    "DAY_ENA": 24 << BF_POS | 1 << BF_LEN | BFUINT32,
    "YEAR": 12 << BF_POS | 12 << BF_LEN | BFUINT32,
    "MONTH": 8 << BF_POS | 4 << BF_LEN | BFUINT32,
    "DAY": 0 << BF_POS | 5 << BF_LEN | BFUINT32
}

# Campos del registro IRQ_SETUP_1
IRQ_SETUP_1_FIELDS = {
    "DOTW_ENA": 31 << BF_POS | 1 << BF_LEN | BFUINT32,
    "HOUR_ENA": 30 << BF_POS | 1 << BF_LEN | BFUINT32,
    "MIN_ENA": 29 << BF_POS | 1 << BF_LEN | BFUINT32,
    "SEC_ENA": 28 << BF_POS | 1 << BF_LEN | BFUINT32,
    "DOTW": 24 << BF_POS | 3 << BF_LEN | BFUINT32,
    "HOUR": 16 << BF_POS | 5 << BF_LEN | BFUINT32,
    "MIN": 8 << BF_POS | 6 << BF_LEN | BFUINT32,
    "SEC": 0 << BF_POS | 6 << BF_LEN | BFUINT32
}

# Campos del registro RTC_1
RTC_1_FIELDS = {
    "YEAR": 12 << BF_POS | 12 << BF_LEN | BFUINT32,
    "MONTH": 8 << BF_POS | 4 << BF_LEN | BFUINT32,
    "DAY": 0 << BF_POS | 5 << BF_LEN | BFUINT32
}

# Campos del registro RTC_0
RTC_0_FIELDS = {
    "DOTW": 24 << BF_POS | 3 << BF_LEN | BFUINT32,
    "HOUR": 16 << BF_POS | 5 << BF_LEN | BFUINT32,
    "MIN": 8 << BF_POS | 6 << BF_LEN | BFUINT32,
    "SEC": 0 << BF_POS | 6 << BF_LEN | BFUINT32
}

# Campos del registro INTR
INTR_FIELDS = {
    "RTC": 0 << BF_POS | 1 << BF_LEN | BFUINT32
}

# Campos del registro INTE
INTE_FIELDS = {
    "RTC": 0 << BF_POS | 1 << BF_LEN | BFUINT32
}

# Campos del registro INTF
INTF_FIELDS = {
    "RTC": 0 << BF_POS | 1 << BF_LEN | BFUINT32
}

# Campos del registro INTS
INTS_FIELDS = {
    "RTC": 0 << BF_POS | 1 << BF_LEN | BFUINT32
}

# Definición de registros del RTC
RTC_REGS = {
    "CLKDIV_M1_REG": 0x00 | UINT32,
    "CLKDIV_M1": (0x00, CLKDIV_M1_FIELDS),
    "SETUP_0_REG": 0x04 | UINT32,
    "SETUP_0": (0x04, SETUP_0_FIELDS),
    "SETUP_1_REG": 0x08 | UINT32,
    "SETUP_1": (0x08, SETUP_1_FIELDS),
    "CTRL_REG": 0x0c | UINT32,
    "CTRL": (0x0c, CTRL_FIELDS),
    "IRQ_SETUP_0_REG": 0x10 | UINT32,
    "IRQ_SETUP_0": (0x10, IRQ_SETUP_0_FIELDS),
    "IRQ_SETUP_1_REG": 0x14 | UINT32,
    "IRQ_SETUP_1": (0x14, IRQ_SETUP_1_FIELDS),
    "RTC_1_REG": 0x18 | UINT32,
    "RTC_1": (0x18, RTC_1_FIELDS),
    "RTC_0_REG": 0x1c | UINT32,
    "RTC_0": (0x1c, RTC_0_FIELDS),
    "INTR_REG": 0x20 | UINT32,
    "INTR": (0x20, INTR_FIELDS),
    "INTE_REG": 0x24 | UINT32,
    "INTE": (0x24, INTE_FIELDS),
    "INTF_REG": 0x28 | UINT32,
    "INTF": (0x28, INTF_FIELDS),
    "INTS_REG": 0x2c | UINT32,
    "INTS": (0x2c, INTS_FIELDS)
}

# Instanciar la estructura del RTC
RTC_DEVICE = struct(RTC_BASE, RTC_REGS)

# Ejemplo de lectura de registros del RTC
rtc = RTC_DEVICE




def leer_rtc():
    # Leer los registros RTC_0 y RTC_1 para obtener la fecha y la hora
    sec = rtc.RTC_0.SEC
    min = rtc.RTC_0.MIN
    hour = rtc.RTC_0.HOUR
    dotw = rtc.RTC_0.DOTW

    day = rtc.RTC_1.DAY
    month = rtc.RTC_1.MONTH
    year = rtc.RTC_1.YEAR

    # Formatear y devolver la fecha y la hora
    fecha_hora = f"Año: {year}, Mes: {month}, Día: {day}, Hora: {hour}, Minuto: {min}, Segundo: {sec}, Día de la semana: {dotw}"
    return fecha_hora

# Llamada a la función para leer y mostrar la hora y la fecha
print(leer_rtc())




def configurar_rtc(year, month, day, dotw, hour, minute, second):
    # Asegurarse de que el RTC esté deshabilitado antes de configurarlo
    rtc.CTRL.RTC_ENABLE = 0
    
    # Configurar la fecha y la hora en los registros SETUP_0 y SETUP_1
    rtc.SETUP_0.YEAR = year
    rtc.SETUP_0.MONTH = month
    rtc.SETUP_0.DAY = day
    
    rtc.SETUP_1.DOTW = dotw
    rtc.SETUP_1.HOUR = hour
    rtc.SETUP_1.MIN = minute
    rtc.SETUP_1.SEC = second
    
    # Cargar la configuración y habilitar el RTC
    rtc.CTRL.LOAD = 1  # Load new time
    rtc.CTRL.RTC_ENABLE = 1  # Enable RTC

# Ejemplo de uso: configurar el RTC para 1 de enero de 2023, 12:00:00 PM, domingo
configurar_rtc(2023, 1, 1, 0, 12, 0, 0)

# Leer y mostrar la fecha y la hora configurada
print(leer_rtc())








