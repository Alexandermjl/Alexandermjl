# LIBRERÍA ACME 
# MÓDULO 1: IMPORTACIÓN DE LIBRERÍAS
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# MÓDULO 2: VARIABLES GLOBALES Y FUNCIONES AUXILIARES
MORADO="#4A2C8A"; ACENTO="#7C3AED"; BG="#F3F4F6"
VERDE="#059669"; ROJO="#DC2626"; NARANJA="#D97706"; GRIS="#4B5563"
COLS = ("ID","Titulo","Autor","Genero","ISBN","Stock","Precio")

def boton(p,txt,cmd,col): 
    return tk.Button(p,text=txt,bg=col,fg="#FFF",font=("Arial",9,"bold"),relief="flat",cursor="hand2",command=cmd)

def centrar(v,w,h): 
    x=(v.winfo_screenwidth()-w)//2; y=(v.winfo_screenheight()-h)//2; 
    v.geometry(str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y))

def mk_tabla(p):
    anc={"ID":36,"Titulo":185,"Autor":125,"Genero":72,"ISBN":122,"Stock":50,"Precio":66}
    t=ttk.Treeview(p,columns=COLS,show="headings",height=14)
    for c in COLS: t.heading(c,text=c); t.column(c,width=anc.get(c,80),anchor="center")
    sb=tk.Scrollbar(p,command=t.yview); t.configure(yscrollcommand=sb.set)
    sb.pack(side="right",fill="y"); t.pack(fill="both",expand=True); return t

def cargar(t,filas):
    for i in t.get_children(): t.delete(i)
    for f in filas: t.insert("","end",values=(f[0],f[1],f[2],f[3],f[4],f[5],"$"+str(round(f[6],2))))

def barra_busqueda(padre,crit_var,entry_ref,fn_buscar,fn_todos):
    bb=tk.Frame(padre,bg="#FFF"); bb.pack(fill="x",padx=10,pady=8)
    tk.Label(bb,text="Buscar por:",bg="#FFF",fg="#374151",font=("Arial",9,"bold")).pack(side="left",padx=(8,4),pady=8)
    ttk.Combobox(bb,textvariable=crit_var,values=["Titulo","Autor","Genero","ISBN"],state="readonly",width=8).pack(side="left",padx=4)
    e=tk.Entry(bb,font=("Arial",9),bg="#F9FAFB",fg="#1F2937",relief="solid",bd=1,width=26); e.pack(side="left",padx=4)
    e.bind("<Return>",lambda ev: fn_buscar()); entry_ref.append(e)
    boton(bb,"Buscar",fn_buscar,ACENTO).pack(side="left",padx=4)
    boton(bb,"Ver todos",fn_todos,GRIS).pack(side="left",padx=2)
    lbl=tk.Label(bb,text="",bg="#FFF",fg="#9CA3AF",font=("Arial",8)); lbl.pack(side="right",padx=8); return lbl

# MÓDULO 3: CLASE LIBRO (MODELO DE DATOS)
class Libro:
    def __init__(self, titulo, autor, genero, isbn, stock, precio):
        self.titulo=titulo; self.autor=autor; self.genero=genero; self.isbn=isbn
        self.stock=stock; self.precio=precio

# MÓDULO 4: BASE DE DATOS (SQLITE3) Y MANEJO DE EXCEPCIONES
class BaseDeDatos:
    def __init__(self, archivo):
        self.archivo=archivo
        try:
            c=sqlite3.connect(archivo)
            c.execute("CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY,usuario TEXT UNIQUE,password TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS libros(id INTEGER PRIMARY KEY,titulo TEXT,autor TEXT,genero TEXT,isbn TEXT UNIQUE,stock INTEGER DEFAULT 0,precio REAL DEFAULT 0)")
            # Datos de prueba iniciales
            for u,p in [("admin","admin123")]:
                c.execute("INSERT OR IGNORE INTO usuarios(usuario,password) VALUES(?,?)",(u,p))
            c.commit(); c.close()
        except sqlite3.Error as e: messagebox.showerror("Error BD",str(e))

    def _q(self, sql, p=()):
        try:
            c=sqlite3.connect(self.archivo); c.execute(sql,p); c.commit(); c.close(); return True
        except sqlite3.Error as e: messagebox.showerror("Error BD",str(e)); return False
        
    def _r(self, sql, p=()):
        try:
            c=sqlite3.connect(self.archivo); r=c.execute(sql,p).fetchall(); c.close(); return r
        except sqlite3.Error as e: messagebox.showerror("Error BD",str(e)); return []
        
    def verificar(self,u,p): return len(self._r("SELECT id FROM usuarios WHERE usuario=? AND password=?",(u,p)))>0
    def todos(self): return self._r("SELECT * FROM libros ORDER BY titulo")
    def editar(self,id,lb): return self._q("UPDATE libros SET titulo=?,autor=?,genero=?,isbn=?,stock=?,precio=? WHERE id=?",(lb.titulo,lb.autor,lb.genero,lb.isbn,lb.stock,lb.precio,id))
    def borrar(self,id): return self._q("DELETE FROM libros WHERE id=?",(id,))
    
    def buscar(self,criterio,valor):
        col={"Titulo":"titulo","Autor":"autor","Genero":"genero","ISBN":"isbn"}[criterio]
        return self._r("SELECT * FROM libros WHERE "+col+" LIKE ?",("%"+valor+"%",))

    def agregar(self,lb):
        try:
            c=sqlite3.connect(self.archivo)
            c.execute("INSERT INTO libros(titulo,autor,genero,isbn,stock,precio) VALUES(?,?,?,?,?,?)",(lb.titulo,lb.autor,lb.genero,lb.isbn,lb.stock,lb.precio))
            c.commit(); c.close(); return True
        except sqlite3.IntegrityError: messagebox.showwarning("Duplicado","ISBN ya existe."); return False
        except sqlite3.Error as e: messagebox.showerror("Error BD",str(e)); return False

# MÓDULO 5: LOGIN EMPLEADO
class VentanaLogin:
    def __init__(self,padre,bd):
        self.padre=padre; self.bd=bd; self.v=tk.Toplevel(); self.v.title("Acceso Empleados")
        self.v.configure(bg="#16213E"); self.v.resizable(False,False); centrar(self.v,360,255); self.v.protocol("WM_DELETE_WINDOW",self._volver)
        
        tk.Label(self.v,text="ACCESO EMPLEADOS",bg="#16213E",fg=ACENTO,font=("Arial",14,"bold")).pack(pady=(20,12))
        f=tk.Frame(self.v,bg="#16213E"); f.pack(padx=40); f.columnconfigure(0,weight=1)
        
        tk.Label(f,text="Usuario:",bg="#16213E",fg="#9CA3AF",font=("Arial",9)).pack(anchor="w",pady=(5,1))
        self.e_usr=tk.Entry(f,bg="#0D1B2A",fg="#FFF",insertbackground="#FFF",relief="flat",bd=4,font=("Arial",9)); self.e_usr.pack(fill="x")
        
        tk.Label(f,text="Password:",bg="#16213E",fg="#9CA3AF",font=("Arial",9)).pack(anchor="w",pady=(5,1))
        self.e_pwd=tk.Entry(f,bg="#0D1B2A",fg="#FFF",insertbackground="#FFF",relief="flat",bd=4,show="*",font=("Arial",9)); self.e_pwd.pack(fill="x")
        
        self.e_usr.focus_set(); self.v.bind("<Return>",lambda ev: self._login())
        fb=tk.Frame(self.v,bg="#16213E"); fb.pack(pady=12)
        boton(fb,"Ingresar",self._login,ACENTO).pack(side="left",padx=6); boton(fb,"Regresar",self._volver,GRIS).pack(side="left",padx=6)
        tk.Label(self.v,text="Demo: admin / admin123",bg="#16213E",fg="#6B7280",font=("Arial",8)).pack()
        
    def _login(self):
        try:
            u=self.e_usr.get().strip(); p=self.e_pwd.get().strip()
            if not u or not p: messagebox.showwarning("Campos vacios","Ingresa usuario y password.",parent=self.v); return
            if self.bd.verificar(u,p): self.v.destroy(); VentanaEmpleado(self.padre,self.bd,u)
            else: messagebox.showerror("Denegado","Usuario o password incorrectos.",parent=self.v); self.e_pwd.delete(0,"end")
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)
        
    def _volver(self): self.v.destroy(); self.padre.deiconify()


# MÓDULO 6: INTERFAZ EMPLEADO 
class VentanaEmpleado:
    def __init__(self,padre,bd,usuario):
        self.padre=padre; self.bd=bd; self.sel_id=None; self.v=tk.Toplevel(); self.v.title("Panel Empleado")
        self.v.configure(bg=BG); centrar(self.v,1000,650); self.v.protocol("WM_DELETE_WINDOW",self._salir)
        
        h=tk.Frame(self.v,bg=MORADO,height=46); h.pack(fill="x"); h.pack_propagate(False)
        tk.Label(h,text="LIBRERIA ACME  |  Empleado: "+usuario,bg=MORADO,fg="#FFF",font=("Arial",13,"bold")).pack(side="left",padx=20,pady=10); boton(h,"Cerrar sesion",self._salir,ROJO).pack(side="right",padx=10,pady=8)
        
        cuerpo=tk.Frame(self.v,bg=BG); cuerpo.pack(fill="both",expand=True,padx=10,pady=8)
        pf=tk.Frame(cuerpo,bg="#FFF",width=230); pf.pack(side="left",fill="y",padx=(0,10)); pf.pack_propagate(False)
        tk.Label(pf,text="DATOS DEL LIBRO",bg=ACENTO,fg="#FFF",font=("Arial",10,"bold")).pack(fill="x",ipady=6)
        
        ff=tk.Frame(pf,bg="#FFF"); ff.pack(padx=10,fill="x")
        for lbl,nom in [("Titulo:","e_titulo"),("Autor:","e_autor"),("Genero:","e_genero"),("ISBN:","e_isbn"),("Stock:","e_stock"),("Precio:","e_precio")]:
            tk.Label(ff,text=lbl,bg="#FFF",fg="#425472",font=("Arial",8,"bold"),anchor="w").pack(fill="x",pady=(5,1))
            e=tk.Entry(ff,font=("Arial",9),bg="#F9FAFB",fg="#1F2937",relief="solid",bd=1); e.pack(fill="x"); setattr(self,nom,e)
            
        fb=tk.Frame(pf,bg="#FFF"); fb.pack(pady=10)
        for txt,cmd,col,r,c in [("Agregar",self._agregar,VERDE,0,0),("Editar",self._editar,NARANJA,0,1),("Borrar",self._borrar,ROJO,1,0),("Limpiar",self._limpiar,GRIS,1,1)]:
            boton(fb,txt,cmd,col).grid(row=r,column=c,padx=3,pady=3,ipadx=4,ipady=3)
            
        pd=tk.Frame(cuerpo,bg=BG); pd.pack(side="left",fill="both",expand=True)
        self.crit=tk.StringVar(value="Titulo"); self._eb=[]
        self.lbl=barra_busqueda(pd,self.crit,self._eb,self._buscar,self._ver_todos)
        self.tabla=mk_tabla(pd); self.tabla.bind("<<TreeviewSelect>>",self._seleccionar)
        self._ver_todos()

    def _limpiar(self):
        for e in [self.e_titulo,self.e_autor,self.e_genero,self.e_isbn,self.e_stock,self.e_precio]: e.delete(0,"end")
        self.sel_id=None

    def _leer(self):
        try:
            t,a,g,i=self.e_titulo.get().strip(),self.e_autor.get().strip(),self.e_genero.get().strip(),self.e_isbn.get().strip()
            if not all([t,a,g,i]): messagebox.showwarning("Faltan datos","Titulo, Autor, Genero e ISBN son obligatorios.",parent=self.v); return None
            return Libro(t,a,g,i,int(self.e_stock.get()),float(self.e_precio.get()))
        except ValueError: messagebox.showerror("Dato invalido","Stock: entero  |  Precio: decimal.",parent=self.v); return None
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v); return None

    def _agregar(self):
        try:
            lb=self._leer(); lb and self.bd.agregar(lb) and (messagebox.showinfo("Exito","Libro guardado.",parent=self.v), self._limpiar(), self._ver_todos())
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _editar(self):
        try:
            if not self.sel_id: messagebox.showwarning("Sin seleccion","Haz clic en un libro primero.",parent=self.v); return
            lb=self._leer(); lb and self.bd.editar(self.sel_id,lb) and (messagebox.showinfo("Exito","Libro modificado.",parent=self.v), self._ver_todos())
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _borrar(self):
        try:
            if not self.sel_id: messagebox.showwarning("Sin seleccion","Haz clic en un libro primero.",parent=self.v); return
            if messagebox.askyesno("Confirmar","Eliminar libro ID "+str(self.sel_id)+"?",parent=self.v):
                self.bd.borrar(self.sel_id); self._limpiar(); self._ver_todos()
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _buscar(self):
        try:
            v=self._eb[0].get().strip(); filas=self.bd.buscar(self.crit.get(),v) if v else self.bd.todos()
            cargar(self.tabla,filas); self.lbl.config(text=str(len(filas))+" resultado(s)")
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _ver_todos(self):
        try: filas=self.bd.todos(); cargar(self.tabla,filas); self.lbl.config(text=str(len(filas))+" libro(s)")
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _seleccionar(self,ev):
        try:
            s=self.tabla.selection()
            if not s: return
            vs=self.tabla.item(s[0],"values"); self._limpiar(); self.sel_id=vs[0]
            for e,val in zip([self.e_titulo,self.e_autor,self.e_genero,self.e_isbn,self.e_stock],[vs[1],vs[2],vs[3],vs[4],vs[5]]): e.insert(0,val)
            self.e_precio.insert(0,str(vs[6]).replace("$",""))
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _salir(self): self.v.destroy(); self.padre.deiconify()

# MÓDULO 7: INTERFAZ CLIENTE (SOLO BÚSQUEDA)
class VentanaCliente:
    def __init__(self,padre,bd):
        self.padre=padre; self.bd=bd; self.v=tk.Toplevel(); self.v.title("Libreria ACME - Catalogo")
        self.v.configure(bg=BG); centrar(self.v,880,560); self.v.protocol("WM_DELETE_WINDOW",self._volver)
        
        h=tk.Frame(self.v,bg=MORADO,height=46); h.pack(fill="x"); h.pack_propagate(False)
        tk.Label(h,text="LIBRERIA ACME  |  Catalogo de Libros",bg=MORADO,fg="#FFF",font=("Arial",13,"bold")).pack(side="left",padx=20,pady=10); boton(h,"Volver",self._volver,"#5B21B6").pack(side="right",padx=10,pady=8)
        
        self.crit=tk.StringVar(value="Titulo"); self._eb=[]
        self.lbl=barra_busqueda(self.v,self.crit,self._eb,self._buscar,self._ver_todos)
        self._eb[0].focus_set()
        
        ft=tk.Frame(self.v,bg=BG); ft.pack(fill="both",expand=True,padx=10,pady=(0,10))
        self.tabla=mk_tabla(ft); self._ver_todos()

    def _buscar(self):
        try:
            v=self._eb[0].get().strip(); filas=self.bd.buscar(self.crit.get(),v) if v else self.bd.todos()
            cargar(self.tabla,filas); self.lbl.config(text=str(len(filas))+" resultado(s)")
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _ver_todos(self):
        try: filas=self.bd.todos(); cargar(self.tabla,filas); self.lbl.config(text=str(len(filas))+" libro(s)")
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.v)

    def _volver(self): self.v.destroy(); self.padre.deiconify()


# MÓDULO 8: VENTANA PRINCIPAL (PANTALLA DE INICIO)
class VentanaInicio:
    def __init__(self,bd):
        self.bd=bd; self.v=tk.Tk(); self.v.title("Libreria ACME"); self.v.configure(bg=MORADO); self.v.resizable(False,False); centrar(self.v,400,290)
        
        tk.Label(self.v,text="LIBRERIA ACME",bg=MORADO,fg="#FFF",font=("Arial",22,"bold")).pack(pady=(38,4))
        tk.Label(self.v,text="Sistema de Control de Stock",bg=MORADO,fg="#C4B5FD",font=("Arial",10)).pack()
        tk.Frame(self.v,bg=ACENTO,height=2,width=260).pack(pady=14)
        
        f=tk.Frame(self.v,bg=MORADO); f.pack()
        boton(f,"  Empleado  ",self._empleado,ACENTO).grid(row=0,column=0,padx=12,pady=8,ipadx=6,ipady=4)
        boton(f,"  Cliente   ",self._cliente,"#5B21B6").grid(row=0,column=1,padx=12,pady=8,ipadx=6,ipady=4)
        tk.Label(self.v,text="Clientes: solo busqueda",bg=MORADO,fg="#9CA3AF",font=("Arial",8)).pack(pady=2)
        
        self.v.mainloop()

    def _empleado(self): self.v.withdraw(); VentanaLogin(self.v,self.bd)
    def _cliente(self): self.v.withdraw(); VentanaCliente(self.v,self.bd)

# MÓDULO 9: EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    # Instanciar base de datos y arrancar aplicación
    bd_app = BaseDeDatos("libreria_acme.db")
    VentanaInicio(bd_app)