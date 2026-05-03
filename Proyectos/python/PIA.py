# LIBRERIA ACME - Sistema de Control de Stock
# MÓDULO 1: IMPORTACIÓN DE LIBRERÍAS
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# MÓDULO 2: VARIABLES GLOBALES Y FUNCIONES AUXILIARES
MORADO = "#4A2C8A" 
ACENTO = "#7C3AED"
BG = "#F3F4F6"
VERDE = "#059669"
ROJO = "#DC2626" 
NARANJA = "#D97706" 
GRIS = "#4B5563"
COLS = ("ID","Titulo","Autor","Genero","ISBN","Stock","Precio")
ANCHOS = {"ID":36,"Titulo":185,"Autor":125,"Genero":72,"ISBN":122,"Stock":50,"Precio":66}

def crear_tabla(parent):
    t = ttk.Treeview(parent, columns=COLS, show="headings", height=14)
    for c in COLS:
        t.heading(c, text=c); t.column(c, width=ANCHOS[c], anchor="center")
    sb = tk.Scrollbar(parent, command=t.yview); t.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y"); t.pack(fill="both", expand=True)
    return t

def cargar_tabla(tabla, filas):
    for i in tabla.get_children(): tabla.delete(i)
    for f in filas:
        tabla.insert("", "end", values=(f[0],f[1],f[2],f[3],f[4],f[5],"$"+str(round(f[6],2))))
        
# MÓDULO 3: CLASE LIBRO (MODELO DE DATOS)
class Libro:
    def __init__(self, titulo, autor, genero, isbn, stock, precio):
        self.titulo = titulo 
        self.autor = autor 
        self.genero = genero
        self.isbn = isbn 
        self.stock = stock 
        self.precio = precio
        
# MÓDULO 4: BASE DE DATOS (SQLITE3) Y MANEJO DE EXCEPCIONES
class BaseDeDatos:
    def __init__(self, archivo):
        self.archivo = archivo
        try:
            con = sqlite3.connect(archivo)
            con.execute("CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY, usuario TEXT UNIQUE, password TEXT)")
            con.execute("CREATE TABLE IF NOT EXISTS libros(id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT, genero TEXT, isbn TEXT UNIQUE, stock INTEGER DEFAULT 0, precio REAL DEFAULT 0)")
            con.execute("INSERT OR IGNORE INTO usuarios(usuario,password) VALUES(?,?)", ("admin","admin123"))
            con.commit(); con.close()
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e))
        
    def verificar(self, usuario, password):
        try:
            con = sqlite3.connect(self.archivo)
            r = con.execute("SELECT id FROM usuarios WHERE usuario=? AND password=?", (usuario,password)).fetchall()
            con.close(); return len(r) > 0
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e)) 
        return False
        
    def obtener_todos(self):
        try:
            con = sqlite3.connect(self.archivo)
            r = con.execute("SELECT * FROM libros ORDER BY titulo").fetchall()
            con.close(); return r
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e)) 
        return []
        
    def agregar(self, lb):
        try:
            con = sqlite3.connect(self.archivo)
            con.execute("INSERT INTO libros(titulo,autor,genero,isbn,stock,precio) VALUES(?,?,?,?,?,?)",
                        (lb.titulo, lb.autor, lb.genero, lb.isbn, lb.stock, lb.precio))
            con.commit(); con.close(); return True
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicado", "Ya existe un libro con ese ISBN.") 
            return False
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e)) 
        return False
        
    def editar(self, id_libro, lb):
        try:
            con = sqlite3.connect(self.archivo)
            con.execute("UPDATE libros SET titulo=?,autor=?,genero=?,isbn=?,stock=?,precio=? WHERE id=?",
                        (lb.titulo, lb.autor, lb.genero, lb.isbn, lb.stock, lb.precio, id_libro))
            con.commit(); con.close(); return True
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e)); return False
        
    def borrar(self, id_libro):
        try:
            con = sqlite3.connect(self.archivo)
            con.execute("DELETE FROM libros WHERE id=?", (id_libro,))
            con.commit(); con.close(); return True
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e)) 
        return False
        
    def buscar(self, criterio, valor):
        if criterio == "Titulo": col = "titulo"
        elif criterio == "Autor": col = "autor"
        elif criterio == "Genero": col = "genero"
        else: col = "isbn"
        try:
            con = sqlite3.connect(self.archivo)
            r = con.execute("SELECT * FROM libros WHERE "+col+" LIKE ?", ("%"+valor+"%",)).fetchall()
            con.close(); return r
        except sqlite3.Error as e: messagebox.showerror("Error BD", str(e)) 
        return []
        
# MÓDULO 5: LOGIN EMPLEADO
class VentanaLogin:
    def __init__(self, padre, bd):
        self.padre = padre; self.bd = bd
        self.v = tk.Toplevel(); self.v.title("Acceso Empleados")
        self.v.configure(bg="#16213E"); self.v.resizable(False,False); self.v.geometry("360x255")
        self.v.protocol("WM_DELETE_WINDOW", self._volver)
        tk.Label(self.v, text="ACCESO EMPLEADOS", bg="#16213E", fg=ACENTO, font=("Arial",14,"bold")).pack(pady=(20,12))
        f = tk.Frame(self.v, bg="#16213E"); f.pack(padx=40, fill="x")
        tk.Label(f, text="Usuario:", bg="#16213E", fg="#9CA3AF", font=("Arial",9)).pack(anchor="w", pady=(5,1))
        self.e_usr = tk.Entry(f, bg="#0D1B2A", fg="#FFF", insertbackground="#FFF", relief="flat", bd=4, font=("Arial",9)); self.e_usr.pack(fill="x")
        tk.Label(f, text="Password:", bg="#16213E", fg="#9CA3AF", font=("Arial",9)).pack(anchor="w", pady=(5,1))
        self.e_pwd = tk.Entry(f, bg="#0D1B2A", fg="#FFF", insertbackground="#FFF", relief="flat", bd=4, show="*", font=("Arial",9)); self.e_pwd.pack(fill="x")
        self.e_usr.focus_set(); self.v.bind("<Return>", self._login)
        fb = tk.Frame(self.v, bg="#16213E"); fb.pack(pady=12)
        tk.Button(fb, text="Ingresar", bg=ACENTO, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._login).pack(side="left", padx=6)
        tk.Button(fb, text="Regresar", bg=GRIS, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._volver).pack(side="left", padx=6)
        tk.Label(self.v, text="Demo: admin / admin123", bg="#16213E", fg="#6B7280", font=("Arial",8)).pack()
        
    def _login(self, ev=None):
        u = self.e_usr.get().strip(); p = self.e_pwd.get().strip()
        if u == "" or p == "":
            messagebox.showwarning("Campos vacios", "Ingresa usuario y password.", parent=self.v); return
        if self.bd.verificar(u, p):
            self.v.destroy(); VentanaEmpleado(self.padre, self.bd, u)
        else:
            messagebox.showerror("Denegado", "Usuario o password incorrectos.", parent=self.v); self.e_pwd.delete(0, "end")
    def _volver(self): self.v.destroy(); self.padre.deiconify()
    
# MÓDULO 6: INTERFAZ EMPLEADO
class VentanaEmpleado:
    def __init__(self, padre, bd, usuario):
        self.padre = padre; self.bd = bd; self.sel_id = None
        self.v = tk.Toplevel(); self.v.title("Panel Empleado")
        self.v.configure(bg=BG); self.v.geometry("1000x650")
        self.v.protocol("WM_DELETE_WINDOW", self._salir)
        h = tk.Frame(self.v, bg=MORADO, height=46); h.pack(fill="x"); h.pack_propagate(False)
        tk.Label(h, text="LIBRERIA ACME  |  Empleado: "+usuario, bg=MORADO, fg="#FFF", font=("Arial",13,"bold")).pack(side="left", padx=20, pady=10)
        tk.Button(h, text="Cerrar sesion", bg=ROJO, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._salir).pack(side="right", padx=10, pady=8)
        cuerpo = tk.Frame(self.v, bg=BG); cuerpo.pack(fill="both", expand=True, padx=10, pady=8)
        pf = tk.Frame(cuerpo, bg="#FFF", width=230); pf.pack(side="left", fill="y", padx=(0,10)); pf.pack_propagate(False)
        tk.Label(pf, text="DATOS DEL LIBRO", bg=ACENTO, fg="#FFF", font=("Arial",10,"bold")).pack(fill="x", ipady=6)
        ff = tk.Frame(pf, bg="#FFF"); ff.pack(padx=10, fill="x")
        self.entries = {}
        for nombre in ["Titulo","Autor","Genero","ISBN","Stock","Precio"]:
            tk.Label(ff, text=nombre+":", bg="#FFF", fg="#425472", font=("Arial",8,"bold"), anchor="w").pack(fill="x", pady=(5,1))
            e = tk.Entry(ff, font=("Arial",9), bg="#F9FAFB", fg="#1F2937", relief="solid", bd=1); e.pack(fill="x")
            self.entries[nombre.lower()] = e
        fb = tk.Frame(pf, bg="#FFF"); fb.pack(pady=10)
        tk.Button(fb, text="Agregar", bg=VERDE, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._agregar).grid(row=0, column=0, padx=3, pady=3, ipadx=4, ipady=3)
        tk.Button(fb, text="Editar", bg=NARANJA, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._editar).grid(row=0, column=1, padx=3, pady=3, ipadx=4, ipady=3)
        tk.Button(fb, text="Borrar", bg=ROJO, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._borrar).grid(row=1, column=0, padx=3, pady=3, ipadx=4, ipady=3)
        tk.Button(fb, text="Limpiar", bg=GRIS, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._limpiar).grid(row=1, column=1, padx=3, pady=3, ipadx=4, ipady=3)
        pd = tk.Frame(cuerpo, bg=BG); pd.pack(side="left", fill="both", expand=True)
        bb = tk.Frame(pd, bg="#FFF"); bb.pack(fill="x", padx=10, pady=8)
        tk.Label(bb, text="Buscar por:", bg="#FFF", fg="#374151", font=("Arial",9,"bold")).pack(side="left", padx=(8,4), pady=8)
        self.crit = tk.StringVar(value="Titulo")
        ttk.Combobox(bb, textvariable=self.crit, values=["Titulo","Autor","Genero","ISBN"], state="readonly", width=8).pack(side="left", padx=4)
        self.eb = tk.Entry(bb, font=("Arial",9), bg="#F9FAFB", fg="#1F2937", relief="solid", bd=1, width=26); self.eb.pack(side="left", padx=4)
        self.eb.bind("<Return>", self._buscar)
        tk.Button(bb, text="Buscar", bg=ACENTO, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._buscar).pack(side="left", padx=4)
        tk.Button(bb, text="Ver todos", bg=GRIS, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._ver_todos).pack(side="left", padx=2)
        self.lbl = tk.Label(bb, text="", bg="#FFF", fg="#9CA3AF", font=("Arial",8)); self.lbl.pack(side="right", padx=8)
        self.tabla = crear_tabla(pd); self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        self._ver_todos()
        
    def _limpiar(self):
        for e in self.entries.values(): e.delete(0, "end")
        self.sel_id = None
        
    def _leer(self):
        t = self.entries["titulo"].get().strip(); a = self.entries["autor"].get().strip()
        g = self.entries["genero"].get().strip(); i = self.entries["isbn"].get().strip()
        if t == "" or a == "" or g == "" or i == "":
            messagebox.showwarning("Faltan datos", "Titulo, Autor, Genero e ISBN son obligatorios.", parent=self.v) 
            return None
        isbn = i.strip()
        if len(isbn) != 10 and len(isbn) != 13:
            messagebox.showwarning("ISBN invalido", "El ISBN debe tener 10 o 13 digitos.", parent=self.v) 
            return None
        if not isbn.isdigit():
            messagebox.showwarning("ISBN invalido", "El ISBN solo debe contener numeros", parent=self.v) 
            return None
        try:
            stock = int(self.entries["stock"].get()); precio = float(self.entries["precio"].get())
        except ValueError:
            messagebox.showerror("Dato invalido", "Stock: entero  |  Precio: decimal.", parent=self.v) 
            return None
        if stock < 0 or precio < 0:
            messagebox.showwarning("Valores invalidos", "Stock y precio no pueden ser negativos.", parent=self.v) 
            return None
        return Libro(t, a, g, i, stock, precio)
    
    def _agregar(self):
        lb = self._leer()
        if lb != None and self.bd.agregar(lb):
            messagebox.showinfo("Exito", "Libro guardado.", parent=self.v) 
            self._limpiar() 
            self._ver_todos()
            
    def _editar(self):
        if self.sel_id == None:
            messagebox.showwarning("Sin seleccion", "Selecciona un libro primero.", parent=self.v); return
        lb = self._leer()
        if lb != None and self.bd.editar(self.sel_id, lb):
            messagebox.showinfo("Exito", "Libro modificado.", parent=self.v) 
            self._ver_todos()
            
    def _borrar(self):
        if self.sel_id == None:
            messagebox.showwarning("Sin seleccion", "Selecciona un libro primero.", parent=self.v) 
            return
        if messagebox.askyesno("Confirmar", "Eliminar libro ID "+str(self.sel_id)+"?", parent=self.v):
            self.bd.borrar(self.sel_id); self._limpiar(); self._ver_todos()
            
    def _buscar(self, ev=None):
        v = self.eb.get().strip()
        if v == "": filas = self.bd.obtener_todos()
        else: filas = self.bd.buscar(self.crit.get(), v)
        cargar_tabla(self.tabla, filas); self.lbl.config(text=str(len(filas))+" resultado(s)")
        
    def _ver_todos(self):
        filas = self.bd.obtener_todos(); cargar_tabla(self.tabla, filas); self.lbl.config(text=str(len(filas))+" libro(s)")
        
    def _seleccionar(self, ev):
        s = self.tabla.selection()
        if not s: return
        vs = self.tabla.item(s[0], "values"); self._limpiar(); self.sel_id = vs[0]
        self.entries["titulo"].insert(0, vs[1]); self.entries["autor"].insert(0, vs[2])
        self.entries["genero"].insert(0, vs[3]); self.entries["isbn"].insert(0, vs[4])
        self.entries["stock"].insert(0, vs[5]); self.entries["precio"].insert(0, str(vs[6]).replace("$",""))
    def _salir(self): self.v.destroy(); self.padre.deiconify()
    
# MÓDULO 7: INTERFAZ CLIENTE (SOLO BÚSQUEDA)
class VentanaCliente:
    def __init__(self, padre, bd):
        self.padre = padre; self.bd = bd
        self.v = tk.Toplevel(); self.v.title("Libreria ACME - Catalogo")
        self.v.configure(bg=BG); self.v.geometry("880x560")
        self.v.protocol("WM_DELETE_WINDOW", self._volver)
        h = tk.Frame(self.v, bg=MORADO, height=46); h.pack(fill="x"); h.pack_propagate(False)
        tk.Label(h, text="LIBRERIA ACME  |  Catalogo de Libros", bg=MORADO, fg="#FFF", font=("Arial",13,"bold")).pack(side="left", padx=20, pady=10)
        tk.Button(h, text="Volver", bg="#5B21B6", fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._volver).pack(side="right", padx=10, pady=8)
        bb = tk.Frame(self.v, bg="#FFF"); bb.pack(fill="x", padx=10, pady=8)
        tk.Label(bb, text="Buscar por:", bg="#FFF", fg="#374151", font=("Arial",9,"bold")).pack(side="left", padx=(8,4), pady=8)
        self.crit = tk.StringVar(value="Titulo")
        ttk.Combobox(bb, textvariable=self.crit, values=["Titulo","Autor","Genero","ISBN"], state="readonly", width=8).pack(side="left", padx=4)
        self.eb = tk.Entry(bb, font=("Arial",9), bg="#F9FAFB", fg="#1F2937", relief="solid", bd=1, width=26); self.eb.pack(side="left", padx=4)
        self.eb.bind("<Return>", self._buscar); self.eb.focus_set()
        tk.Button(bb, text="Buscar", bg=ACENTO, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._buscar).pack(side="left", padx=4)
        tk.Button(bb, text="Ver todos", bg=GRIS, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._ver_todos).pack(side="left", padx=2)
        self.lbl = tk.Label(bb, text="", bg="#FFF", fg="#9CA3AF", font=("Arial",8)) 
        self.lbl.pack(side="right", padx=8)
        ft = tk.Frame(self.v, bg=BG) 
        ft.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self.tabla = crear_tabla(ft) 
        self._ver_todos()
        
    def _buscar(self, ev=None):
        v = self.eb.get().strip()
        if v == "": filas = self.bd.obtener_todos()
        else: filas = self.bd.buscar(self.crit.get(), v)
        cargar_tabla(self.tabla, filas); self.lbl.config(text=str(len(filas))+" resultado(s)")
    def _ver_todos(self):
        filas = self.bd.obtener_todos(); cargar_tabla(self.tabla, filas); self.lbl.config(text=str(len(filas))+" libro(s)")
    def _volver(self): self.v.destroy(); self.padre.deiconify()
    
# MÓDULO 8: VENTANA PRINCIPAL (PANTALLA DE INICIO)
class VentanaInicio:
    def __init__(self, bd):
        self.bd = bd
        self.v = tk.Tk(); self.v.title("Libreria ACME"); self.v.configure(bg=MORADO)
        self.v.resizable(False, False); self.v.geometry("400x290")
        tk.Label(self.v, text="LIBRERIA ACME", bg=MORADO, fg="#FFF", font=("Arial",22,"bold")).pack(pady=(38,4))
        tk.Label(self.v, text="Sistema de Control de Stock", bg=MORADO, fg="#C4B5FD", font=("Arial",10)).pack()
        tk.Frame(self.v, bg=ACENTO, height=2, width=260).pack(pady=14)
        f = tk.Frame(self.v, bg=MORADO); f.pack()
        tk.Button(f, text="  Empleado  ", bg=ACENTO, fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._empleado).grid(row=0, column=0, padx=12, pady=8, ipadx=6, ipady=4)
        tk.Button(f, text="  Cliente   ", bg="#5B21B6", fg="#FFF", font=("Arial",9,"bold"), relief="flat", command=self._cliente).grid(row=0, column=1, padx=12, pady=8, ipadx=6, ipady=4)
        tk.Label(self.v, text="Los clientes solo pueden buscar libros", bg=MORADO, fg="#9CA3AF", font=("Arial",8)).pack(pady=2)
        self.v.mainloop()
    def _empleado(self): self.v.withdraw(); VentanaLogin(self.v, self.bd)
    def _cliente(self): self.v.withdraw(); VentanaCliente(self.v, self.bd)
    
# MÓDULO 9: EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    bd_app = BaseDeDatos("libreria_acme.db")
    VentanaInicio(bd_app)