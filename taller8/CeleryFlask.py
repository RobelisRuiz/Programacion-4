
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from celery import Celery

import redis
PalabraClave = "palabra"
DefinicionClave = "definicion"

r = redis.Redis(host='127.0.0.1', port=6379)
r.set("id", -1)


def VerificarPalabraExistente(palabra):
    CantPalabras = r.llen(PalabraClave)
    PalabraExistente = False
    for i in range(CantPalabras):
        PalabraActual = r.lindex(PalabraClave, i).decode('utf-8')
        if(PalabraActual == palabra):
            PalabraExistente = True
            break
    return PalabraExistente


def AgregarPalabraDef(palabra, definicion):
    r.incr("id")
    r.rpush(PalabraClave, palabra)
    r.rpush(DefinicionClave, definicion)
    print("\n palabra agregada correctamente!")


def ActualizarPalabra(AntiguaPalabra, NuevaPalabra, NuevaDefinicion):
    CantPalabras = r.llen(PalabraClave)
    for i in range(CantPalabras):
        PalabraActual = r.lindex(PalabraClave, i).decode('utf-8')
        if(PalabraActual == AntiguaPalabra):
            r.lset(PalabraClave, i, NuevaPalabra)
            r.lset(DefinicionClave, i, NuevaDefinicion)
            break

    print("\n !La palabra" + AntiguaPalabra + "fue actualizada!")


def EliminarPalabra(palabra):
    CantPalabras = r.llen(PalabraClave)
    for i in range(CantPalabras):
        PalabraActual = r.lindex(PalabraClave, i).decode('utf-8')
        DefinicionActual = r.lindex(DefinicionClave, i).decode('utf-8')
        if(PalabraActual == palabra):
            r.lrem(PalabraClave, i, PalabraActual)
            r.lrem(DefinicionClave, i, DefinicionActual)
            break
    print("\n ¡Palabra eliminada!")


def ShowAllWords():
    CantPalabras = r.llen(PalabraClave)
    palabras = []

    for i in range(CantPalabras):
        palabras.append({"name": r.lindex(PalabraClave, i).decode(
            "utf-8"), "definicion": r.lindex(DefinicionClave, i).decode("utf-8")})
    return palabras


print(r.keys())

app = Flask(__name__)


@app.route('/Index')
def index():
    return render_template("Index.html")


@app.route('/AgregarPalabra', methods=['GET', 'POST'])
def AgregarPalabra():
    if request.method == 'POST':
        palabra = request.form["word"]
        definicion = request.form["meaning"]
        if VerificarPalabraExistente(palabra) == False:
            AgregarPalabraDef(palabra, definicion)
            return render_template("AgregarPalabra.html", message="!!Palabra añadida :)")
        else:
            return render_template("AgregarPalabra.html", message="!!La palabra ya existe :(")

    return render_template("AgregarPalabra.html")


@app.route('/EditarPalabra', methods=['GET', 'POST'])
def EditarPalabra():
    if request.method == 'POST':
        AntiguaPalabra = request.form["oldWord"]
        NuevaPalabra = request.form["word"]
        NuevaDefinicion = request.form["meaning"]

        if VerificarPalabraExistente(AntiguaPalabra):
            ActualizarPalabra(AntiguaPalabra, NuevaPalabra, NuevaDefinicion)

            return render_template("EditarPalabra.html", message=False)
        else:

            return render_template("EditarPalabra.html", message=True)

    return render_template("EditarPalabra.html")


@app.route('/EliminarPalabra', methods=['GET', 'POST'])
def eliminarPalabra():
    if request.method == 'POST':
        palabra = request.form["word"]

        if VerificarPalabraExistente(palabra):
            EliminarPalabra(palabra)
            ShowAllWords()
            return render_template("EliminarPalabra.html", message=False)
        else:
            ShowAllWords()
            return render_template("EliminarPalabra.html", message=True)

    return render_template("EliminarPalabra.html")


@app.route('/ListadoPalabras', methods=['GET', 'POST'])
def listadoPalabra():
    allPalabras = ShowAllWords()

    return render_template("ListadoPalabras.html", palabras=allPalabras)


@app.route('/BuscarSignificado', methods=['GET', 'POST'])
def BuscarSignificado():
    if request.method == 'POST':
        palabra = request.form["palabra"]
        if VerificarPalabraExistente(palabra):
            CantPalabras = r.llen(PalabraClave)
            for i in range(CantPalabras):
                PalabraActual = r.lindex(PalabraClave, i).decode('utf-8')
                if(PalabraActual == palabra):
                    getPalabra = {"palabra": palabra, "definicion": r.lindex(
                        DefinicionClave, i).decode("utf-8")}

                    return render_template("BuscarSignificado.html", ShowWord=getPalabra)
        else:
            return render_template("BuscarSignificado.html", message=True)
    return render_template("BuscarSignificado.html")


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '57f2ff6b9a0188'
app.config['MAIL_PASSWORD'] = 'f82835a15c4057'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

celery = Celery(app.name, broker='redis://localhost:6379/0')
mail = Mail(app)


@Celery.task
def send_async_email(email_data):
    print(email_data + "hola")
    msg = Message(email_data['subject'],
                  sender='aldes@quintero.com',
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    mail.send(msg)

@app.route('/sendEmail', methods=['GET', 'POST'])
def sendEmail():
    if request.method == 'GET':
        return render_template('sendEmail.html')

    email = request.form['email']
    message = request.form['message']

    email_data = {
        'subject': 'Hello from the other side!',
        'to': email,
        'body': message,
    }

    send_async_email(email_data)


if __name__ == "__main__":
    app.run(debug=True)