from flask import Flask, redirect, flash ,url_for, render_template, request
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'

# Conexion MySQL Remoto
#app.config['MYSQL_HOST'] = '198.49.79.226'
#app.config['MYSQL_USER'] = 'kosmikab_user1'
#app.config['MYSQL_PASSWORD'] = 'kosmikaboxmedia2021'
#app.config['MYSQL_DB'] = 'kosmikab_citas'

# Conexion MySQL Local
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2702'
app.config['MYSQL_DB'] = 'kosmika_Asesoria'

mysql = MySQL(app)

# Context processors
@app.context_processor
def date_now():
    return {
        'now' : datetime.utcnow()
    }

# Crear ruta inicial
@app.route('/asesoramiento', methods =['GET', 'POST'])
def crear_cita():
    
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        email = request.form['email']
        celular = request.form['celular']
        categoria = request.form['categoria']
        fecha_cita = request.form['fecha_cita']
        hora_cita = request.form['hora_cita']
        nota = request.form['nota']
        created_at = datetime.now()

        # fecha_cita = datetime.now()
        # hora_cita = datetime.now()
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO registros VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        (nombres, apellidos, email, celular, categoria, fecha_cita, hora_cita, nota, created_at))
        cursor.connection.commit()
        flash('Se ha registrado tú cita correctamente. Gracias.')
        return render_template('UI.html')
        #return redirect(url_for('/'))

    return render_template('UI.html')


# Ruta para Ver Registros de Citas
@app.route('/ver_citas')
def ver_citas():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM registros")
    citas = cursor.fetchall()
    cursor.close()
    
    return render_template('listar_citas.html', citas = citas)

# Mantener la ejecucion en el servidor de flask abierta permanentemente
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    

