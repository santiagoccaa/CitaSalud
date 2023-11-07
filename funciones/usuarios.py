import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from funciones.database import Database

class Usuarios:
	def __init__(self):
		self.db = Database()

		self.ventana = tk.Toplevel()
		self.ventana.title("Usuarios")
		self.ventana.config(bg="#C4A4FF")
		self.ventana.resizable(0,0)
		ancho = 1200
		alto  = 600
		x_ventana = self.ventana.winfo_screenwidth() // 2 - ancho // 2
		y_ventana = self.ventana.winfo_screenheight() // 2 - alto // 2
		posicion = str(ancho) + "x" + str(alto) + "+" + str(x_ventana) + "+" + str(y_ventana)
		self.ventana.geometry(posicion)

		#------------------ FILTRO ------------------------------------------------

		self.treeview_frame = ttk.Frame(self.ventana)
		self.treeview_frame.pack(pady=10)
		self.scrollbar = ttk.Scrollbar(self.treeview_frame)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.listado_users = ttk.Treeview(
        	self.treeview_frame,
        	columns=(1, 2, 3, 4, 5),
        	show="headings",
            height="20",
            yscrollcommand=self.scrollbar.set
            )
		stilo= ttk.Style()
		stilo.theme_use("clam")

		stilo.configure("Treeview.Heading", background="#3C0C97", relief="solid", foreground="#fff", bd=1)
		stilo.configure("Treeview.Heading", font=("Calibri", 12, "bold"))
		self.listado_users.pack(side=tk.LEFT)

		self.scrollbar.config(command=self.listado_users.yview)
		self.listado_users.heading(1, text="Nombre")
		self.listado_users.heading(2, text="Apellidos")
		self.listado_users.heading(3, text="ID")
		self.listado_users.heading(4, text="Correo")
		self.listado_users.heading(5, text="Telefono")
		self.listado_users.column(1, anchor=tk.CENTER)
		self.listado_users.column(2, anchor=tk.CENTER)
		self.listado_users.column(3, anchor=tk.CENTER)
		self.listado_users.column(4, anchor=tk.CENTER)
		self.listado_users.column(5, anchor=tk.CENTER)

		tk.Frame(self.ventana, width=320, height=140, bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1).place(x=10, y=450)
		
		self.filtrar_users= tk.StringVar()
		self.filtro_users_cc= tk.Entry(self.ventana, textvariable=self.filtrar_users,font=('Calibri 14'), width=15, bd=1, relief='solid')
		self.filtro_users_cc.place(x=20, y=470)
		self.filtro_users_cc.delete(0,'end')

		self.btn_buscar= tk.Button(self.ventana,width=12, bd=1 ,text='Buscar',cursor="hand2", bg='#0055FF',fg='#fff', font=('Calibri 12 bold'), command=lambda:self.filtro_cc_users(self.filtrar_users.get()))
		self.btn_buscar.place(x=180, y=470)

		self.eliminar_user= tk.StringVar()
		self.eliminar= tk.Entry(self.ventana, textvariable=self.eliminar_user,font=('Calibri 14'), width=15, bd=1, relief='solid')
		self.eliminar.place(x=20, y=530)
		self.eliminar.delete(0,'end')

		self.btn_eliminar= tk.Button(self.ventana,width=12, bd=1 ,text='Eliminar',cursor="hand2", bg='#FA3333',fg='#fff', font=('Calibri 12 bold'), command=lambda:self.eliminar_usuario(self.eliminar_user.get()))
		self.btn_eliminar.place(x=180, y=530)

		#--------------------- EDITAR USUARIOS--------------

		self.owo=tk.Frame(self.ventana, width=850, height=140, bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1)
		self.owo.place(x=340, y=450)

		self.edit_nombre = tk.StringVar()
		self.nombre=tk.Label(self.ventana, text="Nombre", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.nombre.place(x=560, y=455)
		self.nombre_edit=tk.Entry(self.ventana, textvariable=self.edit_nombre ,font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.nombre_edit.place(x=560, y=485)

		#---apellidos -------------------------------------
		self.edit_apellidos = tk.StringVar()
		self.apellidos=tk.Label(self.ventana, text="Apellidos", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.apellidos.place(x=560, y=515)
		self.apellidos_edit=tk.Entry(self.ventana, textvariable=self.edit_apellidos, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.apellidos_edit.place(x=560, y=550)

		#---cedula -------------------------------------
		self.edit_cedula = tk.StringVar()
		self.cedula_l=tk.Label(self.ventana, text="Num. Id", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.cedula_l.place(x=350, y=455)
		self.cedula_edit=tk.Entry(self.ventana, textvariable=self.edit_cedula, font=('Bahnschrift 15'), width=12, justify="center", bg="#fff")
		self.cedula_edit.place(x=350, y=485)
		self.cedula_edit.delete(0,'end')

		self.b_edit = Image.open("assets/iconos/buscar.png")
		self.b_edit = self.b_edit.resize((30, 30), Image.LANCZOS)
		self.p_edit = ImageTk.PhotoImage(self.b_edit)
		self.b_edit= tk.Button(self.ventana,bd=1, cursor="hand2", compound=tk.TOP, image=self.p_edit, command=lambda:self.buscar_edit(self.edit_cedula.get()))
		self.b_edit.place(x=490, y=485)

		#---tipo -------------------------------------
		self.tipol=tk.Label(self.ventana, text="Tipo Id", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.tipol.place(x=350, y=515)

		self.edit_tipo = tk.StringVar()
		self.ides_edit = ttk.Combobox(self.ventana, textvariable=self.edit_tipo)
		self.ides_edit['values'] = ('Cedula', 'Registro Civil', 'Tarjeta de Identidad', 'Pasaporte') 
		self.ides_edit.place(x=350, y=550)

		#---correo -------------------------------------
		self.edit_correo = tk.StringVar()
		self.correo_edit=tk.Label(self.ventana, text="Correo ", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.correo_edit.place(x=800, y=455)
		self.correo_edit=tk.Entry(self.ventana, textvariable=self.edit_correo, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.correo_edit.place(x=800, y=485)

		#---Telefono -------------------------------------
		self.edit_tel = tk.StringVar()
		self.telL_edir=tk.Label(self.ventana, text="Telefono", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.telL_edir.place(x=800, y=515)
		self.tel_edir=tk.Entry(self.ventana, textvariable=self.edit_tel, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.tel_edir.place(x=800, y=550)
		self.tel_edir.delete(0,'end')

		#----RECARGAR -------------

		self.img_r = Image.open("assets/iconos/refrescar.png")
		self.img_r = self.img_r.resize((30, 30), Image.LANCZOS)
		self.p_r = ImageTk.PhotoImage(self.img_r)
		self.b_r= tk.Button(self.ventana,bd=1, cursor="hand2",width=40, compound=tk.LEFT, image=self.p_r, bg='#fff', command=self.refrescar_users)
		self.b_r.place(x=1120, y=400)

		#----- BOTON PARA EDITAR ----------------

		self.b_e= tk.Button(self.ventana,bd=1, cursor="hand2",width=16, text='Editar Informacion', bg='#3C0C97',fg='#fff', font=('Bahnschrift 12 bold') ,command=self.editar_user)
		self.b_e.place(x=1030, y=540)

		#-----------------------------------------

		for i in self.filtro_usuarios(): 
			self.listado_users.insert('', 'end', values=(i))

	#-----------------------------------------------------------

	def refrescar_users(self):
		self.limpiarfiltro()
		for i in self.filtro_usuarios(): 
			self.listado_users.insert('', 'end', values=(i))

	def filtro_usuarios(self):
		try:
			query="SELECT nombre, apellidos, cedula, correo, telefono FROM personas"
			return self.db.execute_query(query)
		except Exception as er:
			messagebox.showwarning('ERROR', er)

	def datos_db(self, lista):
		self.limpiarfiltro()
		for i in lista: 
			self.listado_users.insert('', 'end', values=(i))
			
	def limpiarfiltro(self):
		self.listado_users.delete(*self.listado_users.get_children())

	def filtro_cc_users(self, cc):
		if cc== '':
			pass
		else:
			try:
				query="SELECT nombre, apellidos, cedula, correo, telefono FROM personas WHERE cedula = (%s) "
				resultado = self.db.execute_query(query, cc)
				return self.datos_db(resultado)
			except Exception as er:
				print('ERROR', er)

	def eliminar_usuario(self, cc):
		if cc== '':
			pass
		else:
			try:
				query="DELETE FROM personas WHERE cedula = (%s) "
				self.db.execute_query(query, cc)
			except Exception as er:
				print('ERROR', er)

	def buscar_edit(self, cc):
		
		if cc == '':
			pass
		else:
			query = "SELECT nombre, apellidos, cedula, correo, telefono, tipo_id FROM personas WHERE cedula = (%s)"
			value = cc
			datos = self.db.execute_query(query, value)
			lista = list(datos)

			for i in lista:
				conver_list= list(i)
				informacion="_".join(map(str, conver_list))
				output=informacion.split('_')
				self.edit_nombre.set(output[0])
				self.edit_apellidos.set(output[1])
				self.edit_cedula.set(output[2])
				self.edit_correo.set(output[3])
				self.edit_tel.set(output[4])
				self.edit_tipo.set(output[5])

	def editar_user(self):

		data1= self.edit_nombre.get()
		data2= self.edit_apellidos.get()
		data3= self.edit_cedula.get()
		data4= self.edit_correo.get()
		data5= self.edit_tel.get()
		data6= self.edit_tipo.get()

		query = "UPDATE `personas` SET `nombre` = %s, `apellidos` = %s, `cedula` = %s, `correo` = %s, `telefono` = %s, `tipo_id` = %s WHERE `cedula` = %s"
		values = (data1, data2, data3, data4, data5, data6, data3)
		datos = self.db.execute_query(query, values)

