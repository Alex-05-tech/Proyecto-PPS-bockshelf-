"""
test_seguridad.py — Pruebas de seguridad OWASP
Verifican que las medidas de seguridad implementadas funcionan correctamente.
Ejecutar con los contenedores levantados: pytest tests/backend/test_seguridad.py -v
"""

import requests

BASE = "http://localhost:5000/api"


# ── A01 · Control de acceso ───────────────────────────────────────────────────

def test_acceso_admin_sin_sesion():
    """Un usuario sin sesión no puede acceder a endpoints de admin."""
    r = requests.delete(f"{BASE}/books/1")
    assert r.status_code in [401, 403], "Debe bloquear el borrado sin autenticación"

def test_acceso_libros_usuario_ajeno():
    """Un usuario no puede ver los libros de otro usuario."""
    r = requests.get(f"{BASE}/user/9999/books")
    assert r.status_code in [401, 403], "No debe permitir acceder a datos de otro usuario"


# ── A03 · Inyección SQL ───────────────────────────────────────────────────────

def test_inyeccion_sql_login():
    """Un intento de inyección SQL en el login debe ser rechazado."""
    payloads = [
        {"username": "' OR '1'='1", "password": "cualquiera"},
        {"username": "admin'--", "password": "cualquiera"},
        {"username": "' OR 1=1--", "password": ""},
    ]
    for payload in payloads:
        r = requests.post(f"{BASE}/login", json=payload)
        assert r.status_code == 401, f"Inyección SQL no bloqueada: {payload['username']}"

def test_inyeccion_sql_busqueda():
    """Una búsqueda con inyección SQL no debe provocar error 500."""
    params = [
        "' OR '1'='1",
        "'; DROP TABLE books;--",
        "' UNION SELECT 1,2,3--",
    ]
    for q in params:
        r = requests.get(f"{BASE}/books", params={"q": q})
        assert r.status_code != 500, f"La búsqueda causó error 500 con: {q}"


# ── A04 · Rate Limiting ───────────────────────────────────────────────────────

def test_rate_limiting_login():
    """Después de 5 intentos fallidos debe devolver 429."""
    payload = {"username": "admin", "password": "contraseña_incorrecta"}
    status_codes = []
    for _ in range(7):
        r = requests.post(f"{BASE}/login", json=payload)
        status_codes.append(r.status_code)
    assert 429 in status_codes, "El rate limiting no está funcionando (esperaba HTTP 429)"


# ── A07 · Autenticación ───────────────────────────────────────────────────────

def test_login_campos_vacios():
    """El login con campos vacíos debe ser rechazado."""
    casos = [
        {"username": "", "password": ""},
        {"username": "admin", "password": ""},
        {"username": "", "password": "admin123"},
    ]
    for caso in casos:
        r = requests.post(f"{BASE}/login", json=caso)
        assert r.status_code in [400, 401], f"Login con campos vacíos no rechazado: {caso}"

def test_login_credenciales_incorrectas():
    """El login con credenciales incorrectas devuelve 401."""
    r = requests.post(f"{BASE}/login", json={"username": "admin", "password": "incorrecta"})
    assert r.status_code == 401

def test_mensaje_error_generico():
    """El mensaje de error no revela si el usuario existe o no."""
    r1 = requests.post(f"{BASE}/login", json={"username": "admin", "password": "mal"})
    r2 = requests.post(f"{BASE}/login", json={"username": "usuarioquenoexiste", "password": "mal"})
    datos1 = r1.json()
    datos2 = r2.json()
    assert datos1.get("error") == datos2.get("error"), \
        "El mensaje de error revela si el usuario existe o no"


# ── A05 · Cabeceras de seguridad ─────────────────────────────────────────────

def test_cabeceras_seguridad():
    """Las respuestas deben incluir las cabeceras HTTP de seguridad."""
    r = requests.get(f"{BASE}/health")
    cabeceras = r.headers
    assert "X-Content-Type-Options" in cabeceras, "Falta cabecera X-Content-Type-Options"
    assert "X-Frame-Options" in cabeceras, "Falta cabecera X-Frame-Options"
    assert "X-XSS-Protection" in cabeceras, "Falta cabecera X-XSS-Protection"


# ── A03 · Validación de inputs ────────────────────────────────────────────────

def test_registro_campos_demasiado_largos():
    """El registro con campos excesivamente largos debe ser rechazado."""
    r = requests.post(f"{BASE}/register", json={
        "username": "a" * 500,
        "email": "test@test.com",
        "password": "1234abcd"
    })
    assert r.status_code in [400, 422], "No se valida la longitud máxima del username"

def test_registro_email_invalido():
    """El registro con un email inválido debe ser rechazado."""
    r = requests.post(f"{BASE}/register", json={
        "username": "usuariotest",
        "email": "esto_no_es_un_email",
        "password": "1234abcd"
    })
    assert r.status_code in [400, 422], "No se valida el formato del email"
