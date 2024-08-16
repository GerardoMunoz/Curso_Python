import tkinter as tk

def PWM_y(x, frecuencia, amplitud_pp, ciclo_trabajo):
    ancho_pantalla = 512
    alto_pantalla = 128
    t_total = 1  # Duración total de la señal en segundos
    voltaje_min = -10  # Voltaje mínimo (en V)
    voltaje_max = 10   # Voltaje máximo (en V)
    x_T =  ancho_pantalla / frecuencia
    x_ciclo = x % x_T
    if x_ciclo <= ciclo_trabajo * x_T:
        voltaje = amplitud_pp / 2
    else:
        voltaje = -amplitud_pp / 2
    y = int(-6.4*voltaje+64)
    
    return y

# Crear la ventana principal
root = tk.Tk()
root.title("Señal PWM")

# Crear el canvas
canvas_width = 512
canvas_height = 128
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Parámetros de la señal PWM
frecuencia = 10  # Frecuencia en Hz
amplitud_pp = 15  # Amplitud pico a pico en voltios
ciclo_trabajo = 0.9  # Ciclo de trabajo (50%)

# Dibujar la señal PWM en el canvas
x0=0
y0=  PWM_y(x0, frecuencia, amplitud_pp, ciclo_trabajo)
for x1 in range(1,canvas_width):
    y1 = PWM_y(x1, frecuencia, amplitud_pp, ciclo_trabajo)
    canvas.create_line(x0, y0, x1, y1, fill="blue")
    x0,y0=x1,y1

# Iniciar el bucle principal de la aplicación
root.mainloop()
