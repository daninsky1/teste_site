from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
database = "schema.sql"

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "1234"

db_con = sqlite3.connect("test.db")
db_cur = db_con.cursor()
# NOTE(daniel): tables are dropped every time. that is we start fresh every run.

with app.open_resource(database) as f:
    db_cur.executescript(f.read().decode("utf8"))
    
db_cur.executescript(
    """INSERT INTO usuario (nome_completo, cpf, email, nascimento, senha)
        VALUES("daniel", 381, "daninsky12@gmail.com", "1996-06-11", 1234);"""
)
db_con.close()

# NOTE(daniel): date function needs to be in the read query to read dates in sqlite.
# NOTE(daniel): Maybe remove magic constants?!

# NOTE(daniel): HOME
@app.route("/", methods=["GET", "POST"])
def index():
    # NOTE(daniel): Login state
    name = ""
    cpf = session.get("cpf")
    senha = session.get("senha")
    
    login_st = False
    reg_st = False
    if not cpf and not senha:
        login_st = False
    else:
        db_con = sqlite3.connect("test.db")
        db_cur = db_con.cursor()
        db_cur.execute("SELECT nome_completo FROM usuario WHERE cpf=?", (cpf,))
        name = db_cur.fetchone()[0].capitalize() + "."
        db_con.close()
        login_st = True
        
    return render_template("index.html", login_session=login_st, usr_name=name)


# NOTE(daniel): CADASTRO E LOGIN
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/validate_register", methods=["POST"])
def validate_register():
    min_pass_length = 4
    
    name = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    birth = request.form.get("nascimento")
    password = request.form.get("senha")
    conf_pass = request.form.get("confirmar-senha")
    
    # NOTE(daniel): This should not trigger in a normal use of the page.
    if (not name) or (not cpf) or (not email) or (not birth):
        return render_template("fail.html", err_message="Erro. Alguns campos foram deixados em branco.")
    elif (password != conf_pass):
        return render_template("fail.html", err_message="Falha na confirmação de senha.")
    elif (len(request.form.get("senha")) < min_pass_length or len(request.form.get("confirmar-senha")) < min_pass_length):
        return render_template("fail.html", err_message=f"Senha inválidada. Mínimo {min_pass_length} dígitos")
    else:
        db_con = sqlite3.connect("test.db")
        db_cur = db_con.cursor()
        
        # NOTE(daniel): It's not to have multiple users, fetchone must be right.
        db_cur.execute("SELECT * FROM usuario WHERE cpf=? ", (cpf,))
        if db_cur.fetchone():
            db_con.close()
            return render_template("fail.html", err_message=f"CPF {cpf}, já foi cadastrado. Faça login.")
        db_cur.execute("SELECT * FROM usuario WHERE email=?", (email, ))
        if db_cur.fetchone():
            db_con.close()
            return render_template("fail.html", err_message=f"Email: {email}, já foi cadastrado. Faça login.")
        else:
            db_cur.execute(
                """INSERT INTO usuario (nome_completo, cpf, email, nascimento, senha)
                    VALUES(?, ?, ?, ?, ?);""", (name, cpf, email, birth, password)
            )
            db_con.commit()
            # INSERT INTO usuario (nome_completo, cpf, email, nascimento, senha)
            #         VALUES("daniel", 381, "daninsky12@gmail.com", "1996-06-11", 1234);
            db_con.close()
            session["cpf"] = cpf
            session["senha"] = password
            return render_template("reg_success.html")
    
    
@app.route("/login", methods=["POST"])
def login():
    db_con = sqlite3.connect("test.db")
    db_cur = db_con.cursor()
    
    if request.method == "POST":
        cpf = request.form.get("cpf")
        password = request.form.get("senha")
        db_cur.execute("SELECT * FROM usuario WHERE cpf=? AND senha=?;", (cpf, password))
        
        if db_cur.fetchone():
            session["cpf"] = cpf
            session["senha"] = password
            return redirect("/")
        else:
            return render_template("fail.html", err_message="Falha no Login.")


@app.route("/logout")
def logout():
    session["cpf"] = None
    session["senha"] = None
    return redirect("/")
    
    
# NOTE(daniel): NOVIDADES
@app.route("/news")
def news():
    db_con = sqlite3.connect("test.db")
    db_cur = db_con.cursor()
    
    max_news_per_page = "4"
    
    novidades = db_cur.execute(
        "SELECT * FROM novidade ORDER BY date(novidade_data) LIMIT ?;", max_news_per_page)
    list_novidades = db_cur.fetchall()
    print(list_novidades)
    print(len(list_novidades))
    
    return render_template("news.html", news=list_novidades)
    
    
#NOTE(daniel): FALE CONOSCO
@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")
    
    
@app.route("/contact_us_send_msg", methods=["POST"])
def contact_us_send_msg():
    # NOTE(daniel): Contact us message
    name = request.form.get("nome")
    email = request.form.get("email")
    msg = request.form.get("menssagem")
    
    return render_template("contact_us_success.html")
