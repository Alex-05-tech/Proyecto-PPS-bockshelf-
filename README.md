# 📚 Bookshelf

Aplicación web para gestionar y descubrir libros, construida con Flask, MySQL y Docker.

---

## 🐳 Arquitectura Docker

```
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│   FRONTEND      │──────▶ │    BACKEND      │──────▶ │   BASE DATOS    │
│                 │        │                 │        │                 │
│ Flask · Jinja2  │        │ Flask API REST  │        │ MySQL 8.0       │
│ Puerto: 8000    │        │ Puerto: 5000    │        │ Puerto: 3306    │
└─────────────────┘        └─────────────────┘        └─────────────────┘
localhost:8000             http://backend:5000         db:3306
(navegador)                (red interna Docker)        (red interna Docker)
```

---

## 🗂 Estructura del proyecto

```
bookshelf_v3/
├── docker-compose.yml
├── .github/workflows/ci-cd.yml
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── bookshelf.sql
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/
└── tests/
    ├── backend/
    └── frontend/
```

---

## 🚀 Instalación

**Requisitos:** Docker Desktop y Git

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio

# 2. Levanta los contenedores
docker compose up --build

# 3. Accede en el navegador
http://localhost:8000

# 4. Para detener
docker compose down
```

---

## 🔑 Credenciales por defecto

| Rol   | Usuario | Contraseña |
|-------|---------|------------|
| Admin | admin   | admin123   |

> ⚠️ Cambiar antes de desplegar en producción.

---

## ✨ Funcionalidades

- Explorar catálogo de libros con búsqueda y filtro por género
- Registrar estado de lectura: Quiero leer · Leyendo · Leído
- Valorar libros y dejar comentarios
- Panel de administración para gestionar el catálogo

---

## 🔄 CI/CD — GitHub Actions

Pipeline automático en cada push o pull request a `main`/`master`.

- **Job 1** — Arranca el backend y verifica que responde correctamente
- **Job 2** — Verifica la sintaxis del frontend
- **Job 3** — Construye y levanta los 3 contenedores Docker

---

## 🧪 Pruebas

Pruebas con Pytest organizadas en `tests/backend/` y `tests/frontend/`.
Se incluye también una colección Postman en `docs/Bookshelf_Tests_Postman.json`

```bash
cd bookshelf_v3/backend
pytest tests/ -v
```

---

## 🔐 Seguridad — OWASP Top 10

| #   | Vulnerabilidad          | Medida aplicada                                  |
|-----|-------------------------|--------------------------------------------------|
| A01 | Control de acceso       | Rutas protegidas con login y rol de admin        |
| A02 | Criptografía            | Contraseñas con hash SHA-256 y salt              |
| A03 | Inyección               | Consultas SQL parametrizadas                     |
| A04 | Diseño inseguro         | Rate limiting en login (5 intentos / 5 min)      |
| A05 | Configuración           | Cabeceras HTTP de seguridad y debug=False        |
| A06 | Componentes             | Versiones fijadas en requirements.txt            |
| A07 | Autenticación           | Sesiones Flask y mensajes de error genéricos     |
| A08 | Integridad              | Pipeline CI/CD que verifica cada commit          |
| A09 | Logging                 | Registro de eventos de seguridad                 |
| A10 | SSRF                    | Riesgo bajo, mejora pendiente                    |
