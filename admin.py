import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
import pymysql
import datetime

#-------- MIS COMPLEMENTOS------------------
from funciones.database import Database
from funciones.usuarios import Usuarios
from funciones.historial import Historial
from assets.styles import style
#-------------------------------------------

class Person():
	def __init__(self, nombre, apellidos, cedula, correo, telefono, tipo_id):
		self.nombre   = nombre
		self.apellidos= apellidos
		self.cedula   = cedula
		self.correo   = correo
		self.telefono = telefono
		self.tipo_id = tipo_id

		self.db = Database()
		self.db.connect()

		if(self.nombre == "" or self.apellidos == "" or self.cedula == "" or self.correo == "" or self.telefono == ''):
			messagebox.showwarning("aviso","Debe llenar todos los campos")
		else:
			query ="INSERT INTO personas (nombre, apellidos, cedula, correo, telefono, tipo_id) VALUES (%s,%s,%s,%s,%s,%s)"
			values = (self.nombre, self.apellidos, self.cedula, self.correo, self.telefono, self.tipo_id)
			self.db.insertar(query, values)

#--------------------------------------------------------------
#--------------------------------------------------------------

class Admin:
	def __init__(self, root_admin):
		self.root_admin = root_admin
		self.db = Database()
		self.db.connect()
		#-------------------------------------------------------
		self.ancho_ventana = 1350
		self.alto_ventana = 750
		self.x_ventana = self.root_admin.winfo_screenwidth() // 2 - self.ancho_ventana // 2
		self.y_ventana = self.root_admin.winfo_screenheight() // 2 - self.alto_ventana // 2
		self.posicion = str(self.ancho_ventana) + "x" + str(self.alto_ventana) + "+" + str(self.x_ventana) + "+" + str(self.y_ventana)
		self.root_admin.geometry(self.posicion)
		self.root_admin.config(bg='#C4A4FF')
		self.root_admin.title('CitaSalud')

		#--------------------------------------------------------
		self.c=tk.Label(self.root_admin, text="Nueva Cita", font=('Bahnschrift, 14 bold'), bg='#C4A4FF')
		self.c.place(x=30, y=5)
		self.frame=tk.Frame(self.root_admin, width=1330, height=100, bg='#E2D2FF', highlightbackground='#3C0C97', highlightthickness=1).place(x=10, y=30)
		self.frame2=tk.Frame(self.root_admin, width=1330, height=100, bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1).place(x=10, y=170)
		
		#-------------- CREAR CITAS -----------------------------
		#---cedula-----------------------------------------------
		self.cita_cc= tk.StringVar()
		self.cc_l=tk.Label(self.frame, text="Num. Id", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.cc_l.place(x=40, y=37)
		self.cc_e=tk.Entry(self.frame, textvariable=self.cita_cc, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.cc_e.place(x=105, y=37)

		self.buscar1 = Image.open("assets/iconos/buscar.png")
		self.buscar1 = self.buscar1.resize((30, 30), Image.LANCZOS)
		self.photo_buscar1 = ImageTk.PhotoImage(self.buscar1)
		self.btn_buscar1= tk.Button(self.root_admin,bd=1, cursor="hand2", compound=tk.TOP, image=self.photo_buscar1, command=lambda:self.buscar_user(self.cita_cc.get()))
		self.btn_buscar1.place(x=330, y=37)

		#---nombre----------------------------------------
		self.cita_nombre= tk.StringVar()
		self.nom_l=tk.Label(self.frame, text="Nombre *", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.nom_l.place(x=40, y=87)
		self.nom_e=tk.Entry(self.frame,state="disable", textvariable=self.cita_nombre, font=('Bahnschrift 15'), justify="center", bg="#fff", width=30)
		self.nom_e.place(x=105, y=87)

		#---fecha----------------------------------------
		self.cita_fecha= tk.StringVar()
		self.fetch_l=tk.Label(self.frame, text="Fecha *", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.fetch_l.place(x=390, y=37)
		self.fetch_e=tk.Entry(self.frame,textvariable=self.cita_fecha, font=('Bahnschrift 15'), width=10, justify="center", bg="#fff")
		self.fetch_e.place(x=455, y=37)

		self.fech = Image.open("assets/iconos/calendar.png")
		self.fech = self.fech.resize((30, 30), Image.LANCZOS)
		self.photo_fech = ImageTk.PhotoImage(self.fech)
		self.btn_fech= tk.Button(self.root_admin,bd=1, cursor="hand2", compound=tk.TOP, image=self.photo_fech, command=self.seleccionar_fecha)
		self.btn_fech.place(x=575, y=37)

		#---hora----------------------------------------
		self.horal=tk.Label(self.frame, text="Hora", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.horal.place(x=1115, y=40)
		self.cita_hora=tk.StringVar()
		self.hora_l = ttk.Combobox(self.frame, textvariable=self.cita_hora, font=('Bahnschrift 12'), width=8)
		self.hora_l.place(x=1160, y=40)

		#---consulta----------------------------------------
		self.consultal=tk.Label(self.frame, text="Consulta", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.consultal.place(x=620, y=37)

		self.cita_consulta = tk.StringVar()
		self.consultas = ttk.Combobox(self.frame, textvariable=self.cita_consulta, font=('Bahnschrift 12'), width=11)
		self.consultas['values'] = ('Pediatria', 'Oftalmologia', 'Odontologia', 'Neurologia', 'Ginecologia') 
		self.consultas.place(x=705, y=40)
		self.consultas.bind('<<ComboboxSelected>>', self.seleccionar_medico)

		#---Medico----------------------------------------
		self.consultal=tk.Label(self.frame, text="Medico", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.consultal.place(x=855, y=37)
		
		self.cita_medico = tk.StringVar()
		self.medicos = ttk.Combobox(self.frame, textvariable=self.cita_medico,font=('Bahnschrift 12'), width=17)
		self.medicos.place(x=912, y=40)
		self.medicos.bind('<<ComboboxSelected>>', self.seleccionar_hora)

		#--- --------- -------------------------------------

		self.agendar_cita= tk.Button(self.frame, bd=1,text="Agendar", width=13, font=('Bahnschrift 14 bold'), cursor="hand2", bg='#3C0C97', fg='#fff', command=self.agendar_cita)
		self.agendar_cita.place(x=450, y=85)

		#************** CREAR NUEVO USUARIO ****************************

		self.c=tk.Label(self.root_admin, text="Nuevo Usuario", font=('Bahnschrift, 14 bold'), bg='#C4A4FF')
		self.c.place(x=30, y=140)

		#---nombre -------------------------------------
		self.persona_nombre = tk.StringVar()
		self.nombre=tk.Label(self.frame, text="Nombre", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.nombre.place(x=40, y=180)
		self.nombre=tk.Entry(self.frame, textvariable=self.persona_nombre ,font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.nombre.place(x=115, y=180)
		#---apellidos -------------------------------------
		self.persona_apellidos = tk.StringVar()
		self.apellidos=tk.Label(self.frame, text="Apellidos", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.apellidos.place(x=350, y=180)
		self.apellidos=tk.Entry(self.frame, textvariable=self.persona_apellidos, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.apellidos.place(x=425, y=180)

		#---cedula -------------------------------------
		self.persona_cedula = tk.StringVar()
		self.cedula_l=tk.Label(self.frame, text="Num. Id", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.cedula_l.place(x=670, y=180)
		self.cedula=tk.Entry(self.frame, textvariable=self.persona_cedula, font=('Bahnschrift 15'), width=12, justify="center", bg="#fff")
		self.cedula.place(x=745, y=180)
		self.cedula.delete(0,'end')

		#---correo -------------------------------------
		self.persona_correo = tk.StringVar()
		self.correo=tk.Label(self.frame, text="Correo ", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.correo.place(x=40, y=230)
		self.correo=tk.Entry(self.frame, textvariable=self.persona_correo, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.correo.place(x=115, y=230)

		#---Telefono -------------------------------------
		self.persona_telefono = tk.StringVar()
		self.tel=tk.Label(self.frame, text="Telefono", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.tel.place(x=350, y=230)
		self.tel=tk.Entry(self.frame, textvariable=self.persona_telefono, font=('Bahnschrift 15'), justify="center", bg="#fff")
		self.tel.place(x=425, y=230)
		self.tel.delete(0,'end')

		#---tipo -------------------------------------
		self.tipol=tk.Label(self.frame, text="Tipo Id", font=('Bahnschrift 13 bold'), bg='#E2D2FF')
		self.tipol.place(x=670, y=230)

		self.tipo_id = tk.StringVar()
		self.ides = ttk.Combobox(self.frame, textvariable=self.tipo_id)
		self.ides['values'] = ('Cedula de Ciudadania', 'Registro Civil', 'Tarjeta de Identidad', 'Permiso temporal') 
		self.ides.place(x=745, y=230)

		#-------------- AÑADIR USUARIO --------------------------

		self.registrar= tk.Button(self.frame, bd=1,text="Registrar", width=13, font=('Bahnschrift 14 bold'), cursor="hand2", bg='#3C0C97', fg='#fff', command=self.registrar_persona)
		self.registrar.place(x=900, y=227)

		self.limpiar= tk.Button(self.frame, bd=1,text="Limpiar", width=6, font=('Bahnschrift 14 bold'), cursor="hand2", bg='#F92D2D', fg='#fff', command=self.limpiar_registro)
		self.limpiar.place(x=900, y=180)

		#--------------------------------------------------------
		self.frame4=tk.Frame(self.root_admin, width=610, height=435, bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1).place(x=10, y=280)
		self.frame4=tk.Frame(self.root_admin, width=400, height=50,  bg='#fff',highlightbackground='#3C0C97', highlightthickness=1).place(x=20, y=290)
		
		self.filtro_cedula = tk.StringVar()
		self.buscar=tk.Entry(self.frame,textvariable=self.filtro_cedula ,font=('Bahnschrift 15'), justify="center", bg="#fff", bd=1, relief='solid')
		self.buscar.place(x=30, y=300)
		self.buscar.delete(0,'end')

		self.buscar = Image.open("assets/iconos/buscar.png")
		self.buscar = self.buscar.resize((30, 30), Image.LANCZOS)
		self.photo_buscar = ImageTk.PhotoImage(self.buscar)
		self.btn_buscar= tk.Button(self.root_admin,bd=1, cursor="hand2",width=90, compound=tk.LEFT, image=self.photo_buscar,text="Buscar", bg='#3C0C97', fg='#fff',font=('Bahnschrift 12 bold'), command=lambda:self.filtro_cc(self.filtro_cedula.get()))
		self.btn_buscar.place(x=270, y=296)

		self.recargar = Image.open("assets/iconos/refrescar.png")
		self.recargar = self.recargar.resize((30, 30), Image.LANCZOS)
		self.photo_recargar = ImageTk.PhotoImage(self.recargar)
		self.btn_recargar= tk.Button(self.root_admin,bd=1, cursor="hand2",width=90, compound=tk.LEFT, image=self.photo_recargar,text="Refrescar", bg='#fff', fg='#3C0C97',font=('Bahnschrift 10 bold'), command=self.refrescar)
		self.btn_recargar.place(x=480, y=310)

		#----------- LISTADO DE CITAS -------------------------

		self.listado = ttk.Treeview(
        	self.frame4,
        	columns=(1, 2, 3, 4, 5, 6),
        	show="headings",
            height="16"
            )
		stilo= ttk.Style()
		stilo.theme_use("clam")

		stilo.configure("Treeview.Heading", 
			background='#3C0C97',
			relief="solid", 
			foreground="#000", 
			bd=1)
		stilo.configure("Treeview.Heading", font=("Calibri", 12, "bold"))
		self.listado.place(x=20, y=350)

		self.listado.heading(1, text="Nombre")
		self.listado.heading(2, text="Id")
		self.listado.heading(3, text="Fecha")
		self.listado.heading(4, text="Hora")
		self.listado.heading(5, text="Consulta")
		self.listado.heading(6, text="Medico")
		self.listado.column(1, anchor=tk.CENTER, width=160)
		self.listado.column(2, anchor=tk.CENTER, width=110)
		self.listado.column(3, anchor=tk.CENTER, width=50)
		self.listado.column(4, anchor=tk.CENTER, width=50)
		self.listado.column(5, anchor=tk.CENTER, width=90)
		self.listado.column(6, anchor=tk.CENTER, width=110)

		#------- FILTRO DE DOCTORES --------------------------

		self.frame5=tk.Frame(self.root_admin, width=350, height=435,  bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1)
		self.frame5.place(x=640, y=280)
		
		#----------- DOCTORES --------------------------------

		self.scrollbar = ttk.Scrollbar(self.frame4)
		self.scrollbar.place()
		self.list_doctores = ttk.Treeview(
        	self.frame4,
        	columns=(1, 2, 3),
        	show="headings",
            height="10",
            yscrollcommand=self.scrollbar.set
            )
		stilo= ttk.Style()
		stilo.theme_use("clam")

		stilo.configure("Treeview.Heading", background='#3C0C97', relief="solid", foreground="#fff", bd=1)
		self.list_doctores.place(x=660, y=290)

		self.scrollbar.config(command=self.list_doctores.yview)
		self.list_doctores.heading(1, text="Nombre")
		self.list_doctores.heading(2, text="Rol")
		self.list_doctores.heading(3, text="Estado")
		self.list_doctores.column(1, anchor=tk.CENTER, width=150)
		self.list_doctores.column(2, anchor=tk.CENTER, width=80)
		self.list_doctores.column(3, anchor=tk.CENTER, width=80)

		for i in self.filtro_all(): 
			self.listado.insert('', 'end', values=(i))

		#------------------------------------------------------

		self.odonto = Image.open("assets/iconos/odontologia.png")
		self.odonto = self.odonto.resize((70, 70), Image.LANCZOS)
		self.p_odonto = ImageTk.PhotoImage(self.odonto)
		self.btn_odonto= tk.Button(self.root_admin , cursor="hand2", compound=tk.TOP, image=self.p_odonto, command=lambda:self.filtro_medicos('odontologia'))
		self.btn_odonto.place(x=680, y=540)

		self.gine = Image.open("assets/iconos/ginecologia.png")
		self.gine = self.gine.resize((70, 70), Image.LANCZOS)
		self.p_gine = ImageTk.PhotoImage(self.gine)
		self.btn_gine= tk.Button(self.root_admin , cursor="hand2", compound=tk.TOP, image=self.p_gine, command=lambda:self.filtro_medicos('ginecologia'))
		self.btn_gine.place(x=765, y=540)

		self.pedi = Image.open("assets/iconos/pediatria.png")
		self.pedi = self.pedi.resize((70, 70), Image.LANCZOS)
		self.p_pedi = ImageTk.PhotoImage(self.pedi)
		self.btn_pedi= tk.Button(self.root_admin ,bg='#fff', cursor="hand2", compound=tk.TOP, image=self.p_pedi, command=lambda:self.filtro_medicos('pediatria'))
		self.btn_pedi.place(x=850, y=540)

		self.oftalmologia = Image.open("assets/iconos/oftalmologia.png")
		self.oftalmologia = self.oftalmologia.resize((70, 70), Image.LANCZOS)
		self.p_oftalmologia = ImageTk.PhotoImage(self.oftalmologia)
		self.btn_oftalmologia= tk.Button(self.root_admin , cursor="hand2", compound=tk.TOP, image=self.p_oftalmologia, command=lambda:self.filtro_medicos('oftalmologia'))
		self.btn_oftalmologia.place(x=680, y=630)

		self.radiologia = Image.open("assets/iconos/radiologia.png")
		self.radiologia = self.radiologia.resize((70, 70), Image.LANCZOS)
		self.p_radiologia = ImageTk.PhotoImage(self.radiologia)
		self.btn_radiologia= tk.Button(self.root_admin , cursor="hand2", compound=tk.TOP, image=self.p_radiologia, command=lambda:self.filtro_medicos('radiologia'))
		self.btn_radiologia.place(x=765, y=630)

		self.interna = Image.open("assets/iconos/neurologia.png")
		self.interna = self.interna.resize((70, 70), Image.LANCZOS)
		self.p_interna = ImageTk.PhotoImage(self.interna)
		self.btn_interna= tk.Button(self.root_admin ,bg='#fff', cursor="hand2", compound=tk.TOP, image=self.p_interna, command=lambda:self.filtro_medicos('neurologia'))
		self.btn_interna.place(x=850, y=630)	

		#------------ MAS OPCIONES ---------------------

		self.frame6=tk.Frame(self.root_admin, width=300, height=435,  bg='#E2D2FF',highlightbackground='#3C0C97', highlightthickness=1)
		self.frame6.place(x=1020, y=280)
		'''
		self.doctor = Image.open("assets/iconos/doctor.png")
		self.doctor = self.doctor.resize((70, 70), Image.LANCZOS)
		self.p_doctor = ImageTk.PhotoImage(self.doctor)
		self.btn_doctor= tk.Button(self.root_admin,width=200,bd=1,bg='#fff', text='Doctores',font=('Bahnschrift 12 bold') ,cursor="hand2", compound=tk.TOP, image=self.p_doctor,command=self.llamar_doctores)
		self.btn_doctor.place(x=1075, y=290)
		'''
		self.user = Image.open("assets/iconos/user.png")
		self.user = self.user.resize((70, 70), Image.LANCZOS)
		self.p_user = ImageTk.PhotoImage(self.user)
		self.btn_user= tk.Button(self.root_admin,width=200,bd=1,bg='#fff', text='Usuarios',font=('Bahnschrift 12 bold') ,cursor="hand2", compound=tk.TOP, image=self.p_user, command=self.llamar_user)
		self.btn_user.place(x=1075, y=340)

		self.histori = Image.open("assets/iconos/historial.png")
		self.histori = self.histori.resize((70, 70), Image.LANCZOS)
		self.p_histori = ImageTk.PhotoImage(self.histori)
		self.btn_histori= tk.Button(self.root_admin,width=200,bd=1,bg='#fff', text='Historial',font=('Bahnschrift 12 bold') ,cursor="hand2", compound=tk.TOP, image=self.p_histori, command=self.llamar_historial)
		self.btn_histori.place(x=1075, y=500)

		#-----------------------------------------------
		self.current_person = None

	#---------------------------
	def llamar_user(self):
		return Usuarios()
	def llamar_historial(self):
		return Historial()
	#---------------------------------------------------
	def llamar_doctores(self):

		self.root_doc = tk.Toplevel()
		self.root_doc.title("Doctores")
		self.root_doc.config(bg="#C4A4FF")
		self.root_doc.resizable(0,0)
		ancho = 540
		alto  = 500
		x_root_doc = self.root_doc.winfo_screenwidth() // 2 - ancho // 2
		y_root_doc = self.root_doc.winfo_screenheight() // 2 - alto // 2
		posicion = str(ancho) + "x" + str(alto) + "+" + str(x_root_doc) + "+" + str(y_root_doc)
		self.root_doc.geometry(posicion)
		
		self.image = Image.open("assets/img/owo.png")
		self.image = self.image.resize((500,400),Image.LANCZOS)
		self.img = ImageTk.PhotoImage(self.image)
		tk.Label(self.root_doc, image = self.img, bg="#fff").place(x=10,y=20)

		self.entry1_v=tk.StringVar()
		self.entry1=tk.Entry(self.root_doc,textvariable=self.entry1_v ,bg='#fff',width=20,justify="center", bd=0,font=('Calibri 18 bold'), fg="#3F3F3F")
		self.entry1.place(x=250,y=140)

		self.entry2_v=tk.StringVar()
		self.entry2=tk.Entry(self.root_doc,textvariable=self.entry2_v ,bg='#fff',width=20,justify="center", bd=0,font=('Calibri 18 bold'), fg="#FC2F2F")
		self.entry2.place(x=250,y=205)

		self.entry3_v=tk.StringVar()
		self.entry3=tk.Entry(self.root_doc,textvariable=self.entry3_v ,bg='#fff',width=20,justify="center", bd=0,font=('Calibri 18 bold'), fg="#3F3F3F")
		self.entry3.place(x=250,y=265)

		self.entry4_v=tk.StringVar()
		self.entry4=tk.Entry(self.root_doc,textvariable=self.entry4_v ,bg='#C4A4FF',width=20,justify="center", bd=0,font=('Calibri 18 bold'), fg="#3F3F3F")
		self.entry4.place(x=100,y=440)
		tk.Frame(self.root_doc, width=250, height=2, bg='#000').place(x=100,y=475)
		
		self.buscar2 = Image.open("assets/iconos/buscar.png")
		self.buscar2 = self.buscar1.resize((30, 30), Image.LANCZOS)
		self.photo_buscar2 = ImageTk.PhotoImage(self.buscar1)
		self.btn_buscar2= tk.Button(self.root_doc,bd=1, cursor="hand2", compound=tk.TOP, image=self.photo_buscar2)
		self.btn_buscar2.place(x=350, y=440)

	def seleccionar_fecha(self):

		def obtener_fecha():
			fecha_seleccionada = cal.get_date()
			self.fetch_e.delete(0, tk.END)
			self.fetch_e.insert(tk.END, fecha_seleccionada)
			calendario.destroy()

		calendario = tk.Toplevel()
		calendario.title("Calendario")
		calendario.configure(bg="#f0f0f0")
		calendario.resizable(0,0)

		ancho = 300
		alto  = 300
		x_c = calendario.winfo_screenwidth() // 2 - ancho // 2
		y_c = calendario.winfo_screenheight() // 2 - alto // 2
		posicion = str(ancho) + "x" + str(alto) + "-" + str(x_c) + "+" + str(y_c)
		calendario.geometry(posicion)
	
		cal = Calendar(calendario, selectmode='day', year=2023, showweeknumbers=False, month=6, day=14, **style.estilo_calendario)
		cal.pack(pady=6)

		boton_seleccionar = tk.Button(calendario, text="Seleccionar", command=obtener_fecha,
				bg='#3C0C97', fg="#fff", font=("Arial", 12), padx=10, pady=5)
		boton_seleccionar.pack(pady=6)

	#--------------------------------------------

	def registrar_persona(self):
		if not self.current_person:
			self.current_person = Person(
				self.persona_nombre.get(), 
				self.persona_apellidos.get(), 
				self.persona_cedula.get(), 
				self.persona_correo.get(), 
				self.persona_telefono.get(),
				self.tipo_id.get())
		self.current_person = None

	def limpiar_registro(self):
		self.nombre.delete(0,'end')
		self.apellidos.delete(0,'end')
		self.cedula.delete(0,'end')
		self.correo.delete(0,'end')
		self.tel.delete(0,'end')

	def buscar_user(self, cedula):
		if cedula == '':
			messagebox.showwarning('Aviso','Debe ingresar un Id en el campo a la izquierda')
		else:
		
			query = "SELECT nombre, apellidos FROM personas WHERE cedula = (%s)"
			value = cedula
			datos = self.db.execute_query(query, value)
			lista = list(datos)

			for i in lista:
				conver_list= list(i)
				informacion="_".join(map(str, conver_list))
				output=informacion.split('_')
				self.cita_nombre.set(output[0] + " " + output[1])

	def verificar_cita(self):
		query= "SELECT fecha, hora from citas where cedula = (%s)"
		value = self.cita_cc.get()

		fechayhora = self.db.execute_query(query, value)

		owo = list(item for sublist in fechayhora for item in sublist)
		print(owo)

	def agendar_cita(self):

		v1 = self.cita_nombre.get()
		v2 = self.cita_cc.get()
		v3 = self.cita_fecha.get()
		v4 = self.cita_hora.get()
		v5 = self.cita_consulta.get()
		v6 = self.cita_medico.get()

		query = "INSERT INTO citas (nombre, cedula, fecha, hora, consulta, medico) VALUES (%s,%s,%s,%s,%s,%s)"
		query2 = "INSERT INTO historial (nombre, cedula, fecha, hora, consulta, medico) VALUES (%s,%s,%s,%s,%s,%s)"
		values = (v1,v2,v3,v4,v5,v6)

		if v2 == '' or v3 == '' or v4 == '' or v5 == '' or v6 == '':
			messagebox.showerror("Alerta",'Debe llenar todos los campos')
		else:
			self.db.guardar_cita(query2, values)
			self.db.insertar_cita(query, values)

			self.verificar_cita()

		self.cc_e.delete(0, 'end')

		self.nom_e.config(state="normal")
		self.nom_e.delete(0, 'end')
		self.nom_e.config(state="disabled")
		
		self.fetch_e.delete(0, 'end')

	def refrescar(self):
		self.limpiarfiltro()
		for i in self.filtro_all(): 
			self.listado.insert('', 'end', values=(i))

	def datos_db(self, lista):
		self.limpiarfiltro()
		for i in lista: 
			self.listado.insert('', 'end', values=(i))
			
	def limpiarfiltro(self):
		self.listado.delete(*self.listado.get_children())

	def filtro_all(self):
		try:
			fecha_actual = datetime.date.today()
			dia = fecha_actual.day
			mes = fecha_actual.month
			anio = fecha_actual.strftime('%y')
			hoy = f"{dia}/{mes}/{anio}"
			query="SELECT nombre, cedula, fecha, hora, consulta, medico FROM citas WHERE fecha = (%s)"
			value = hoy
			return self.db.execute_query(query, value)

		except Exception as er:
			messagebox.showwarning('ERROR', er)

	def filtro_cc(self, cc):

		if cc== '':
			pass
		else:
			try:
				query="SELECT nombre, cedula, fecha, hora, consulta, medico FROM citas WHERE cedula = (%s) "
				resultado = self.db.execute_query(query, cc)
				return self.datos_db(resultado)
			except Exception as er:
				print('ERROR', er)

	def filtro_medicos(self, data):

		self.list_doctores.delete(*self.list_doctores.get_children())

		try:
			query="SELECT nombre, especialidad, estado FROM doctores_especialidad WHERE especialidad = (%s)"
			value = data
			
			consulta = self.db.execute_query(query, data)

			for i in consulta: 
				self.list_doctores.insert('', 'end', values=(i))

		except Exception as er:
			messagebox.showwarning('ERROR', er)

	def seleccionar_medico(self, event):
		x = self.cita_consulta.get()
		query= "SELECT nombre FROM doctores_especialidad WHERE especialidad = (%s)"
		datos = self.db.execute_query(query, x)

		datos_convertidos = tuple(item for sublist in datos for item in sublist)

		self.medicos['values']=datos_convertidos

	def seleccionar_hora(self, event):

		x = self.cita_medico.get()

		query= "SELECT hora_1, hora_2,hora_3,hora_4,hora_5,hora_6,hora_7,hora_8 FROM doctores_especialidad WHERE nombre = (%s)"
		datos = self.db.execute_query(query, x)
		
		datos_convertidos = tuple(item for sublist in datos for item in sublist)

		self.hora_l['values']=datos_convertidos
	

#------------------------------------------------------------
def runapp():
	root = tk.Tk()
	app = Admin(root)
	root.mainloop()
