import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
from funciones.database import Database

class Historial:
	def __init__(self):
		self.db = Database()

		self.root_historial = tk.Toplevel()
		self.root_historial.title("Historial")
		self.root_historial.config(bg="#C4A4FF")
		self.root_historial.resizable(0,0)
		ancho = 1240
		alto  = 650
		x_root_historial = self.root_historial.winfo_screenwidth() // 2 - ancho // 2
		y_root_historial = self.root_historial.winfo_screenheight() // 2 - alto // 2
		posicion = str(ancho) + "x" + str(alto) + "+" + str(x_root_historial) + "+" + str(y_root_historial)
		self.root_historial.geometry(posicion)

		#------------------ FILTRO ------------------------------------------------

		self.frame_h = ttk.Frame(self.root_historial)
		self.frame_h.pack(pady=10)
		self.scrollbar = ttk.Scrollbar(self.frame_h)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.listado_historial = ttk.Treeview(
        	self.frame_h,
        	columns=(1, 2, 3, 4, 5, 6,7),
        	show="headings",
            height="17",
            yscrollcommand=self.scrollbar.set
            )
		stilo_h= ttk.Style()
		stilo_h.theme_use("clam")

		stilo_h.configure("Treeview.Heading", background="#3C0C97", relief="solid", foreground="#fff", bd=1)
		stilo_h.configure("Treeview.Heading", font=("Calibri", 12, "bold"))
		self.listado_historial.pack(side=tk.LEFT)

		self.scrollbar.config(command=self.listado_historial.yview)
		self.listado_historial.heading(1, text="Nombre")
		self.listado_historial.heading(2, text="Id")
		self.listado_historial.heading(3, text="Fecha")
		self.listado_historial.heading(4, text="Min.")
		self.listado_historial.heading(5, text="Consulta")
		self.listado_historial.heading(6, text="Medico")
		self.listado_historial.heading(7, text="Codigo")
		self.listado_historial.column(1, anchor=tk.CENTER, width=180)
		self.listado_historial.column(2, anchor=tk.CENTER, width=180)
		self.listado_historial.column(3, anchor=tk.CENTER, width=180)
		self.listado_historial.column(4, anchor=tk.CENTER, width=90)
		self.listado_historial.column(5, anchor=tk.CENTER, width=180)
		self.listado_historial.column(6, anchor=tk.CENTER, width=180)
		self.listado_historial.column(7, anchor=tk.CENTER, width=90)

		self.owo=tk.Frame(self.root_historial, width=300, height=140, bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1)
		self.owo.place(x=500, y=420)

		self.filtrar_historial= tk.StringVar()
		self.hitorial_cc= tk.Entry(self.root_historial, textvariable=self.filtrar_historial,font=('Calibri 14'), width=15, bd=1, relief='solid')
		self.hitorial_cc.place(x=520, y=430)
		self.hitorial_cc.delete(0,'end')

		self.btn_bc= tk.Button(self.root_historial,width=12, bd=1 ,text='Buscar',cursor="hand2", bg='#0055FF',fg='#fff', font=('Calibri 12 bold'), command=lambda:self.filtro_historial_cc(self.filtrar_historial.get()))
		self.btn_bc.place(x=680, y=430)

		self.eliminar_historial= tk.IntVar()
		self.eliminar_cc= tk.Entry(self.root_historial, textvariable=self.eliminar_historial,font=('Calibri 14'), width=15, bd=1, relief='solid')
		self.eliminar_cc.place(x=520, y=500)
		self.eliminar_cc.delete(0,'end')

		self.btn_eli= tk.Button(self.root_historial,width=12, bd=1 ,text='Eliminar',cursor="hand2", bg='#FA3333',fg='#fff', font=('Calibri 12 bold'), command=lambda:self.filtro_historial_cc(self.eliminar_historial.get()))
		self.btn_eli.place(x=680, y=500)

		estilo_calendario = {
			"background": "#E2D2FF",
			"foreground": "#000",
			"headersbackground": "#3C0C97",
			"headersforeground": "#fff",
			"selectbackground": "#0055FF",
			"selectforeground": "#fff",
			"font": ("Bahnschrift 12 bold"),
			"bordercolor": "#000",
			'locale': 'es_ES'
			}

		self.cal_h = Calendar(self.root_historial, selectmode='day',  showweeknumbers=False,year=2023, month=6, day=14, **estilo_calendario)
		self.cal_h.place(x=80,y=420)

		#--------------BUSCAR POR FECHA--------------

		self.img_c = Image.open("assets/iconos/buscar.png")
		self.img_c = self.img_c.resize((30, 30), Image.LANCZOS)
		self.p_c = ImageTk.PhotoImage(self.img_c)
		self.b_c= tk.Button(self.root_historial,bd=1, cursor="hand2",width=40, compound=tk.LEFT, image=self.p_c, bg='#fff', command=lambda:self.filtro_historial_fecha(self.cal_h.get_date()))
		self.b_c.place(x=375, y=420)

		#----RECARGAR -------------

		self.img_r = Image.open("assets/iconos/refrescar.png")
		self.img_r = self.img_r.resize((30, 30), Image.LANCZOS)
		self.p_r = ImageTk.PhotoImage(self.img_r)
		self.b_r= tk.Button(self.root_historial,bd=1, cursor="hand2",width=40, compound=tk.LEFT, image=self.p_r, bg='#fff', command=self.refrescar_historial)
		self.b_r.place(x=1180, y=348)

		for i in self.filtro_historial(): 
			self.listado_historial.insert('', 'end', values=(i))

	#-----------------------------------------------------------

	def refrescar_historial(self):
		self.limpiarfiltro()
		for i in self.filtro_historial(): 
			self.listado_historial.insert('', 'end', values=(i))

	def filtro_historial(self):
		try:
			query="SELECT nombre, cedula, fecha, hora, consulta, medico FROM historial"
			return self.db.execute_query(query)
		except Exception as er:
			messagebox.showwarning('ERROR', er)

	def datos_historial(self, lista):
		self.limpiarfiltro()
		for i in lista: 
			self.listado_historial.insert('', 'end', values=(i))
			
	def limpiarfiltro(self):
		self.listado_historial.delete(*self.listado_historial.get_children())

	def filtro_historial_cc(self, cc):
		if cc== '':
			pass
		else:
			try:
				query="SELECT nombre, cedula, fecha, hora, consulta, medico, codigo FROM historial WHERE cedula = (%s) "
				resultado = self.db.execute_query(query, cc)
				return self.datos_historial(resultado)
			except Exception as er:
				print('ERROR', er)

	def filtro_historial_fecha(self, fecha):
		if fecha== '':
			pass
		else:
			try:
				query="SELECT nombre, cedula, fecha, hora,consulta, medico, codigo FROM historial WHERE fecha = (%s) "
				resultado = self.db.execute_query(query, fecha)
				return self.datos_historial(resultado)
			except Exception as er:
				print('ERROR', er)