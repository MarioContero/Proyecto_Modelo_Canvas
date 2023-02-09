from flask import Flask, render_template, request, redirect, make_response, session
import pdfkit
import sqlite3

app = Flask(__name__)
app.secret_key = 'ada7sd6aasdasdasdasdas'

# Crear conexión a la base de datos
conn = sqlite3.connect("datos.db")

# Crear tabla si no existe
conn.execute("""
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula INT UNIQUE,
    proveedores TEXT,
    clientes TEXT,
    presupuesto TEXT,
    publicidad TEXT,
    activos TEXT
)
""")
conn.commit()
conn.close()


@app.route("/")
def index():
    if 'cedula' in session:
        cedula  = session["cedula"]
        conn = sqlite3.connect("datos.db")
        datos = conn.execute("SELECT id, cedula, proveedores, clientes, presupuesto, publicidad, activos FROM proyectos WHERE cedula = " + cedula).fetchone()
        print(datos)
        conn.close()
        return render_template("index.html", datos = datos)
    else: 
        return redirect("/login")
        

@app.route("/guardar", methods=["POST"])
def guardar():
    cedula = session["cedula"]
    proveedores = request.form.get("proveedores")
    clientes = request.form.get("clientes")
    presupuesto = request.form.get("presupuesto")
    publicidad = request.form.get("publicidad")
    activos = request.form.get("activos")
    conn = sqlite3.connect("datos.db")
    conn.execute("""INSERT OR REPLACE INTO proyectos (cedula, proveedores, clientes, presupuesto, publicidad, activos) 
        VALUES (?, ?, ?, ?, ?, ?);""", (cedula, proveedores, clientes, presupuesto, publicidad, activos))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/borrar")
def borrar():
    cedula = session["cedula"]
    conn = sqlite3.connect("datos.db")
    conn.execute("DELETE FROM proyectos WHERE cedula = "+cedula)
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/pdf")
def pdf():
    cedula = session["cedula"]
    conn = sqlite3.connect("datos.db")
    datos = conn.execute("SELECT * FROM proyectos WHERE cedula ="+cedula).fetchone()
    conn.close()
    html = render_template("index.html", datos = datos)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Proyecto.pdf'
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cedula = request.form.get("cedula")
        session["cedula"] = cedula
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)