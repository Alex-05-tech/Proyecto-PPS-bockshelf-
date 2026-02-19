from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib
import os
from functools import wraps

# ── Apunta las templates a la carpeta frontend ────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))   # .../backend
FRONTEND_DIR    = os.path.join(BASE_DIR, '..', 'frontend')     # .../frontend
TEMPLATES_DIR   = os.path.join(FRONTEND_DIR, 'templates')
STATIC_DIR      = os.path.join(FRONTEND_DIR, 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)
app.secret_key = 'bookshelf_secret_2024'

# ── Configuración MySQL ───────────────────────────────────────────────────────
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': '',          # ← pon tu contraseña aquí si tienes
    'database': 'bookshelf',
    'charset':  'utf8mb4'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ── Decoradores de auth ───────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Acceso restringido a administradores.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapped

# ── Rutas principales ─────────────────────────────────────────────────────────
@app.route('/')
def index():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    search = request.args.get('q', '').strip()
    genre  = request.args.get('genre', '').strip()

    sql = """SELECT b.*, u.username AS added_by
             FROM books b LEFT JOIN users u ON b.created_by = u.id
             WHERE 1=1"""
    params = []
    if search:
        sql += " AND (b.title LIKE %s OR b.author LIKE %s)"
        params += [f'%{search}%', f'%{search}%']
    if genre:
        sql += " AND b.genre = %s"
        params.append(genre)
    sql += " ORDER BY b.orden ASC, b.id DESC"
    cur.execute(sql, params)
    books = cur.fetchall()

    cur.execute("SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL AND genre != '' ORDER BY genre")
    genres = [r['genre'] for r in cur.fetchall()]

    user_books = {}
    if 'user_id' in session:
        cur.execute("SELECT book_id, status, rating, liked FROM user_books WHERE user_id = %s", (session['user_id'],))
        for row in cur.fetchall():
            user_books[row['book_id']] = row

    cur.close(); conn.close()
    return render_template('index.html', books=books, genres=genres,
                           user_books=user_books, search=search, current_genre=genre)

@app.route('/book/<int:bid>')
def book_detail(bid):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT b.*, u.username AS added_by
                   FROM books b LEFT JOIN users u ON b.created_by = u.id
                   WHERE b.id = %s""", (bid,))
    book = cur.fetchone()
    if not book:
        flash('Libro no encontrado.', 'error')
        return redirect(url_for('index'))

    cur.execute("""SELECT ub.*, u.username
                   FROM user_books ub JOIN users u ON ub.user_id = u.id
                   WHERE ub.book_id = %s AND (ub.comment IS NOT NULL OR ub.rating IS NOT NULL)
                   ORDER BY ub.updated_at DESC""", (bid,))
    reviews = cur.fetchall()

    user_book = None
    if 'user_id' in session:
        cur.execute("SELECT * FROM user_books WHERE user_id = %s AND book_id = %s",
                    (session['user_id'], bid))
        user_book = cur.fetchone()

    cur.execute("""SELECT COUNT(*) AS total, AVG(rating) AS avg_r
                   FROM user_books WHERE book_id = %s AND rating IS NOT NULL""", (bid,))
    stats = cur.fetchone()

    cur.close(); conn.close()
    return render_template('book_detail.html', book=book, reviews=reviews,
                           user_book=user_book, stats=stats)

@app.route('/book/<int:bid>/update', methods=['POST'])
@login_required
def update_user_book(bid):
    status  = request.form.get('status', 'quiero_leer')
    rating  = request.form.get('rating') or None
    liked_v = request.form.get('liked', '')
    comment = request.form.get('comment', '').strip() or None
    liked   = int(liked_v) if liked_v != '' else None

    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM user_books WHERE user_id = %s AND book_id = %s",
                (session['user_id'], bid))
    if cur.fetchone():
        cur.execute("""UPDATE user_books
                       SET status=%s, rating=%s, liked=%s, comment=%s, updated_at=NOW()
                       WHERE user_id=%s AND book_id=%s""",
                    (status, rating, liked, comment, session['user_id'], bid))
    else:
        cur.execute("""INSERT INTO user_books (user_id, book_id, status, rating, liked, comment)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (session['user_id'], bid, status, rating, liked, comment))
    conn.commit(); cur.close(); conn.close()
    flash('¡Tu lectura ha sido actualizada!', 'success')
    return redirect(url_for('book_detail', bid=bid))

@app.route('/my-books')
@login_required
def my_books():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT b.*, ub.status, ub.rating, ub.liked, ub.comment, ub.updated_at
                   FROM user_books ub JOIN books b ON ub.book_id = b.id
                   WHERE ub.user_id = %s ORDER BY ub.updated_at DESC""", (session['user_id'],))
    all_books = cur.fetchall()
    cur.close(); conn.close()

    reading = [b for b in all_books if b['status'] == 'leyendo']
    read    = [b for b in all_books if b['status'] == 'leido']
    want    = [b for b in all_books if b['status'] == 'quiero_leer']
    return render_template('my_books.html', reading=reading, read=read, want=want)

# ── Admin ─────────────────────────────────────────────────────────────────────
@app.route('/admin')
@admin_required
def admin():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT b.*, u.username AS added_by
                   FROM books b LEFT JOIN users u ON b.created_by = u.id ORDER BY b.orden ASC""")
    books = cur.fetchall()
    cur.execute("SELECT id, username, email, is_admin, created_at FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close(); conn.close()
    return render_template('admin.html', books=books, users=users)

@app.route('/admin/book/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        conn = get_db(); cur = conn.cursor()
        cur.execute("""INSERT INTO books (title, author, synopsis, genre, year, cover_color, cover_image, created_by)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (request.form['title'], request.form['author'],
                     request.form.get('synopsis', ''), request.form.get('genre', ''),
                     request.form.get('year') or None,
                     request.form.get('cover_color', '#7c6f64'),
                     request.form.get('cover_image', '').strip() or None,
                     session['user_id']))
        conn.commit(); cur.close(); conn.close()
        flash('Libro añadido correctamente.', 'success')
        return redirect(url_for('admin'))
    return render_template('book_form.html', book=None, action='Añadir')

@app.route('/admin/book/edit/<int:bid>', methods=['GET', 'POST'])
@admin_required
def edit_book(bid):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM books WHERE id = %s", (bid,))
    book = cur.fetchone()
    if not book:
        flash('Libro no encontrado.', 'error')
        cur.close(); conn.close()
        return redirect(url_for('admin'))
    if request.method == 'POST':
        cur2 = conn.cursor()
        cur2.execute("""UPDATE books
                        SET title=%s, author=%s, synopsis=%s, genre=%s, year=%s,
                            cover_color=%s, cover_image=%s
                        WHERE id=%s""",
                     (request.form['title'], request.form['author'],
                      request.form.get('synopsis', ''), request.form.get('genre', ''),
                      request.form.get('year') or None,
                      request.form.get('cover_color', '#7c6f64'),
                      request.form.get('cover_image', '').strip() or None,
                      bid))
        conn.commit(); cur2.close(); cur.close(); conn.close()
        flash('Libro actualizado correctamente.', 'success')
        return redirect(url_for('admin'))
    cur.close(); conn.close()
    return render_template('book_form.html', book=book, action='Editar')

@app.route('/admin/book/delete/<int:bid>', methods=['POST'])
@admin_required
def delete_book(bid):
    conn = get_db(); cur = conn.cursor()
    cur.execute("DELETE FROM user_books WHERE book_id = %s", (bid,))
    cur.execute("DELETE FROM books WHERE id = %s", (bid,))
    conn.commit(); cur.close(); conn.close()
    flash('Libro eliminado.', 'success')
    return redirect(url_for('admin'))

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = get_db(); cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                    (request.form['username'], hash_pw(request.form['password'])))
        user = cur.fetchone(); cur.close(); conn.close()
        if user:
            session['user_id']  = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            flash(f'¡Bienvenido, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        email    = request.form['email'].strip()
        password = hash_pw(request.form['password'])
        try:
            conn = get_db(); cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, password))
            conn.commit()
            uid = cur.lastrowid
            cur.close(); conn.close()
            session['user_id']  = uid
            session['username'] = username
            session['is_admin'] = False
            flash('¡Cuenta creada! Bienvenido a Bookshelf.', 'success')
            return redirect(url_for('index'))
        except Exception:
            flash('El nombre de usuario o email ya existe.', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
