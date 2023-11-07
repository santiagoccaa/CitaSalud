import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

#-------- MIS COMPLEMENTOS------------------
from funciones.database import Database
from assets.styles import style
from admin import runapp
#-------------------------------------------

class App:
	def __init__(self, root, call_admin=False):
		self.call_admin = call_admin
		self.root = root
		self.db = Database()

		self.ancho_ventana = 900
		self.alto_ventana = 500
		self.x_ventana = self.root.winfo_screenwidth() // 2 - self.ancho_ventana // 2
		self.y_ventana = self.root.winfo_screenheight() // 2 - self.alto_ventana // 2
		self.posicion = str(self.ancho_ventana) + "x" + str(self.alto_ventana) + "+" + str(self.x_ventana) + "+" + str(self.y_ventana)
		self.root.geometry(self.posicion)
		self.root.config(bg='#fff')
		self.root.title('Login')

		#------------ IMAGEM --------------------------
		self.image = Image.open("assets/img/login.png")
		self.image = self.image.resize((450,450),Image.LANCZOS)

		self.img = ImageTk.PhotoImage(self.image)
		tk.Label(self.root, image = self.img, bg="#fff").place(x=0,y=0)

		#------------------ FRAMES --------------------------
		self.frame=tk.Frame(self.root, width=450, height=500, bg='#16a086').place(x=450, y=0)

		#------------------ CONTENIDO -----------------------

		self.title = tk.Label(self.frame, text="Bienvenido de Vuelta!", **style.title).place(x=540, y=50)

		#--- NOMBRE    ----
		self.var_name = tk.StringVar()
		self.name = tk.Label(self.frame, text= "Usuario", **style.data).place(x=540, y=150)
		self.entry_name = tk.Entry(self.frame, textvariable=self.var_name , **style.ENTRY).place(x=540, y=180)
		
		#--- CONTRASEÑA ---
		self.var_pasw = tk.StringVar()
		self.pasw = tk.Label(self.frame, text= "Contraseña", **style.data).place(x=540, y=230)
		self.entry_pasw = tk.Entry(self.frame, textvariable=self.var_pasw , **style.ENTRY, show="*").place(x=540, y=260)
		
		#------ BOTON INICIAR --------------

		self.login= tk.Button(self.frame,command=lambda:self.verify(self.var_name.get(), self.var_pasw.get()) ,text="Iniciar", **style.BTN_LOGIN, cursor="hand2").place(x=560, y=350)
		
		#---- CONEXION----------------------

		self.db.connect()
	def admin(self):
		runapp()

	def verify(self, name, pasw):
		self.conn = self.db.connect()

		if name and pasw != '':
			try:
				query = "SELECT * FROM users WHERE nombre = (%s) and password = (%s)"
				values = (name, pasw)
				
				self.cursor = self.conn.cursor()
				self.cursor.execute(query, values)

				self.data = self.cursor.fetchall()

				user_exists = bool(self.data)

				if user_exists:
					if self.call_admin:
						self.root.destroy()
						self.admin()	
				else:
					messagebox.showinfo('Aviso', 'El usuario no existe')

			except pymysql.Error as e:
				print('Error', f'Error de conexión: {str(e)}')
		else:
			messagebox.showerror("Aviso", "Debe llenar todos los campos")

if __name__ == '__main__':
	root = tk.Tk()
	app = App(root, call_admin=True)
	root.mainloop()
