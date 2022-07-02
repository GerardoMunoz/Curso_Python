
import tkinter as tk


draw_mode='Rectángulo'
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
	if draw_mode=='Rectángulo':
		figura=lienzo.create_rectangle(x0,y0,x0+10,y0+10,fill="black")
		print('uno')
	elif draw_mode=='Línea':
		figura=lienzo.create_line(x0,y0,x0+10,y0+10,fill="black")
		print('dos')
	elif draw_mode=='Texto':
		figura=lienzo.create_text(x0, y0, text=entr_ttxt.get(), fill="black", font=('Helvetica 10 bold'))
		print('tres')
	else:
		print('press draw_mode',draw_mode)
	

def move(event):
	#print(event.x, event.y)
	x1,y1 = (event.x, event.y)
	if figura and draw_mode in ['Rectángulo','Línea']:
		lienzo.coords(figura, x0, y0, x1, y1)
	

def release(event):
	...

def erase(event):
	global figura 
	lienzo.delete(figura)	
	figura=None





ventana = tk.Tk()

botonera = tk.Frame(ventana)
botonera.pack(side = tk.TOP)
boton_rec = tk.Button(botonera,text='Rectángulo', command=lambda:set_mode('Rectángulo'))
boton_rec.pack(side = tk.LEFT)
boton_lin = tk.Button(botonera,text='Línea', command=lambda:set_mode('Línea'))
boton_lin.pack(side = tk.LEFT)
boton_txt = tk.Button(botonera,text='Texto', command=lambda:set_mode('Texto'))
boton_txt.pack(side = tk.LEFT)
entr_ttxt = tk.Entry(botonera)
entr_ttxt.pack(side = tk.LEFT)



lienzo = tk.Canvas(ventana,bg='white')
lienzo.pack(side =  tk.BOTTOM, fill=tk.BOTH, expand=True)
lienzo.bind("<ButtonPress>", press)
lienzo.bind("<B1-Motion>", move)
lienzo.bind("<ButtonRelease>", release)
lienzo.bind("<Control-Button-1>",erase)


ventana.mainloop()


