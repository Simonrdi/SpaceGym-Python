from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import secrets
import sqlite3
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail, Message

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') or secrets.token_urlsafe(48)
oauth= OAuth()
oauth.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

mail = Mail(app)

google = oauth.register(
    name="google",
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'}
)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
def create_table():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT DEFAULT NULL
    ) """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS spaces (
        num INTEGER PRIMARY_KEY,
        name TEXT NOT NULL      
    ) """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS prenota(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,    
        space_id INTEGER NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),    
        FOREIGN KEY (space_id) REFERENCES spaces(num)
    )
     """)
    conn.commit()
    conn.close()


@app.route("/prova")
def prova():
    return render_template("Apertura.html", google_maps_api_key=os.getenv('GOOGLE_MAPS_API_KEY', ''))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(request.form)  # Debugging per verificare i dati inviati
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("Compila tutti i campi!", "danger")
            return redirect(url_for("register"))
        hashed_password = generate_password_hash(password)
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            conn.close()
            flash("Registrazione avvenuta con successo! Ora puoi accedere.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Il nome utente è già in uso!", "danger")   
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        connect = get_db_connection()
        user = connect.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        connect.close()
        if user and check_password_hash(user["password"], password):
            session["Idutente"] = user["id"]
            session["username"] = user["email"]
            flash("accesso effettuato")
            return redirect(url_for("home")) 
        else:
            flash("credenziali errate")
    return render_template ('Login.html')

@app.route("/login/google")
def login_google():
    try:
        redirect_uri= url_for('authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error(f"Errore durante il login :{str(e)}")
        return "Errore durante il login", 500
@app.route("/authorize/google")
def authorize_google():
    token= google.authorize_access_token()
    userinfo_endpoint = google.server_metadata['userinfo_endpoint']
    resp= google.get(userinfo_endpoint)
    user_info= resp.json()
    username = user_info['email']

    conn=get_db_connection()
    conn.execute("INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)", (username, "oauth"))
    conn.commit()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (username,)).fetchone()
    conn.close()
    session["oauth_token"] = token
    session["username"] = username
    session["Idutente"] = user["id"]


    return redirect(url_for('home'))
@app.route("/prenota", methods=["GET", "POST"])
def prenota():
    conn = get_db_connection()
    spaces = conn.execute("SELECT * FROM spaces").fetchall()
    
    if request.method == "POST":
        user_id = session.get("Idutente")
        space_id = request.form.get("space_id")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        if not user_id:
            return redirect(url_for("login"))
        if not user_id or not space_id or not start_time or not end_time:
            flash("Compila tutti i campi", "danger")
            return redirect(url_for("prenota"))

        # Controlla sovrapposizioni
        overlapping = conn.execute("""
            SELECT * FROM prenota 
            WHERE space_id = ? AND 
            NOT (end_time <= ? OR start_time >= ?)
        """, (space_id, start_time, end_time)).fetchone()

        if overlapping:
            flash("Questa fascia oraria è già occupata.", "danger")
        else:
            conn.execute("""
                INSERT INTO prenota (user_id, space_id, start_time, end_time)
                VALUES (?, ?, ?, ?)
            """, (user_id, space_id, start_time, end_time))
            conn.commit()
            flash("Prenotazione effettuata con successo!", "success")
            utente = conn.execute ("SELECT email FROM users WHERE id = ?", (user_id,)).fetchone()
            if utente and utente["email"] :
                msg= Message ("Prova di conferma prenotazione", recipients=[utente["email"]])
                msg.body = "hai prenotato"
                mail.send(msg)
            else:
                app.logger.error(f"Utente con ID {user_id} non trovato. Impossibile inviare email.")

        conn.close()
        return redirect(url_for("prenota"))
    

    conn.close()
    return render_template("prenota.html", spaces=spaces)
@app.route("/home", methods=["GET", "POST"])
def home():
    conn = get_db_connection()
    user_id = session.get("Idutente")
    utente = conn.execute ("SELECT email FROM users WHERE id = ?", (user_id,)).fetchone()
    flash(f"{utente["email"]}")
    
    conn.close()
    return render_template("home.html") 

@app.route("/allenamenti")
def allenamenti():
    return render_template("Pagina palestra.html")


if '__main__' == __name__:
    create_table()
    app.run()