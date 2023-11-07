import pymysql
from tkinter import messagebox

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='hospital'
            )
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error de conexión: {str(e)}')

        return self.connection

    def disconnect(self):
        if self.connect():
            self.connect().close()

    def insertar(self, query, values=None):
        try:
            with self.connect().cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                    messagebox.showinfo("Aviso","La persona fue registrada con exito")
                
        except pymysql.Error as e:
            messagebox.showerror('Alerta','ESTE USUARIO YA EXISTE')

    def eliminar(self, query, values=None):
        try:
            with self.connect().cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                    messagebox.showinfo("Aviso","Cita eliminada correctamente")
                
        except pymysql.Error as e:
            messagebox.showwarning("Alerta","Ocurrio un errro al intentar eliminar la cita")

    def insertar_cita(self, query, values=None):
        try:
            with self.connect().cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                    messagebox.showinfo("Aviso","La cita fue programada correctamente")
        except pymysql.Error as e:
            print("Error al ejecutar la consulta:", {str(e)})

    def guardar_cita(self, query, values=None):
        try:
            with self.connect().cursor() as cursor:
                if values:
                    cursor.execute(query, values)
        except pymysql.Error as e:
            print("Error al ejecutar la consulta:", {str(e)})

    def execute_query(self, query, values=None):
        try:
            with self.connect().cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                    data = cursor.fetchall()
                else:
                    cursor.execute(query)
                    data = cursor.fetchall()
                return data
                self.connection.commit()

        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error al ejecutar la consulta: {str(e)}')
            print(e)
