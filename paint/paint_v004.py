
import tkinter as tk

class Potenciometro():
	ancho=10
	nombre='Potenciometro'
		  
	def __init__(self,canvas,x0,y0,**kwargs):
		self.canvas = canvas
		self.coords=x0,y0
		self.lineas=self.zigzag_vert(x0,y0,3,**kwargs)
			
			
			
	def zigzag_vert(self,x0,y0,n,**kwargs):
		ANCHO=Potenciometro.ancho
		lineas = []
		for i in range(n):
			lineas.append(self.canvas.create_line(x0,y0+2*i*ANCHO,x0+ANCHO,y0+(2*i+1)*ANCHO,**kwargs))
			lineas.append(self.canvas.create_line(x0+ANCHO,y0+(2*i+1)*ANCHO,x0,y0+(2*i+2)*ANCHO,**kwargs))
		return lineas
	
	def delete(self):
		for linea in self.lineas:
			self.canvas.delete(linea)

	def move(self,x1,y1):
		pass
		
	
class Rectangulo():
	
	nombre='Rectángulo'
	
	def __init__(self,canvas,x0,y0,**kwargs):
		self.canvas = canvas
		self.coords=x0,y0
		self.lineas=[canvas.create_rectangle(x0,y0,x0+10,y0+10,**kwargs)]

	def delete(self):
		for linea in self.lineas:
			self.canvas.delete(linea)
			
	def move(self,x1,y1):
		x0,y0=self.coords
		for linea in self.lineas:
			self.canvas.coords(linea, x0, y0, x1, y1)
		
		
class Linea():
	
	nombre='Línea'
	
	def __init__(self,canvas,x0,y0,**kwargs):
		self.canvas = canvas
		self.coords=x0,y0
		self.lineas=[canvas.create_line(x0,y0,x0+10,y0+10,**kwargs)]

	def delete(self):
		for linea in self.lineas:
			self.canvas.delete(linea)

	def move(self,x1,y1):
		x0,y0=self.coords
		for linea in self.lineas:
			self.canvas.coords(linea, x0, y0, x1, y1)

		
class Texto():
	
	nombre='Texto'
	
	def __init__(self,canvas,x0,y0,**kwargs):
		self.canvas = canvas
		self.coords=x0,y0
		self.lineas=[canvas.create_text(x0, y0, text=entr_ttxt.get(), font=('Helvetica 10 bold'),**kwargs)]

	def delete(self):
		for linea in self.lineas:
			self.canvas.delete(linea)

	def move(self,x1,y1):
		pass
		

draw_mode=Rectangulo
figura=None
x0,y0=0,0

def set_mode(mode):
	global draw_mode #debe ser global para poderla modificar
	draw_mode = mode
	print(draw_mode)
	

def press(event):
	global x0,y0,figura,draw_mode
	#print(event.x, event.y)
	x0,y0 = (event.x, event.y)
	if draw_mode:
		figura=draw_mode(lienzo,x0,y0,fill="black")
	else:
		print('press draw_mode',draw_mode)
	

def move(event):
	x1,y1 = (event.x, event.y)
	if figura:
		figura.move( x1, y1)
	


def erase(event):
	global figura 
	if figura:
		figura.delete()
	figura=None





ventana = tk.Tk()

botonera = tk.Frame(ventana)
botonera.pack(side = tk.TOP)
boton = tk.Button(botonera,text=Potenciometro.nombre, command=lambda:set_mode(Potenciometro))
boton.pack(side = tk.LEFT)
boton = tk.Button(botonera,text=Rectangulo.nombre, command=lambda :set_mode(Rectangulo))
boton.pack(side = tk.LEFT)
boton = tk.Button(botonera,text=Linea.nombre, command=lambda :set_mode(Linea))
boton.pack(side = tk.LEFT)
boton = tk.Button(botonera,text=Texto.nombre, command=lambda :set_mode(Texto))
boton.pack(side = tk.LEFT)
entr_ttxt = tk.Entry(botonera)
entr_ttxt.pack(side = tk.LEFT)
entr_ttxt.insert(tk.END, 'text o')



lienzo = tk.Canvas(ventana,bg='white')
lienzo.pack(side =  tk.BOTTOM, fill=tk.BOTH, expand=True)
lienzo.bind("<ButtonPress>", press)
lienzo.bind("<B1-Motion>", move)
lienzo.bind("<Control-Button-1>",erase)



ventana.mainloop()


