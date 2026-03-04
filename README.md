================================================================================
  📚 BOOKSHELF — README
================================================================================

Aplicación web para gestionar y descubrir libros, construida con Flask,
MySQL y Docker.


================================================================================
  🐳 ARQUITECTURA DOCKER
================================================================================

  ┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
  │   FRONTEND      │──────▶│    BACKEND      │──────▶│   BASE DATOS    │
  │                 │        │                 │        │                 │
  │ Flask · Jinja2  │        │ Flask API REST  │        │ MySQL 8.0       │
  │ Puerto: 8000    │        │ Puerto: 5000    │        │ Puerto: 3306    │
  └─────────────────┘        └─────────────────┘        └─────────────────┘

     localhost:8000            http://backend:5000          db:3306
     (navegador)               (red interna Docker)    (red interna Docker)


================================================================================
  🗂  ESTRUCTURA DEL PROYECTO
================================================================================

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


================================================================================
  🚀 INSTALACIÓN
================================================================================

  Requisitos: Docker Desktop y Git

  1. Clona el repositorio
       git clone https://github.com/tu-usuario/tu-repositorio.git
       cd tu-repositorio

  2. Levanta los contenedores
       docker compose up --build

  3. Accede en el navegador
       http://localhost:8000

  4. Para detener
       docker compose down


================================================================================
  🔑 CREDENCIALES POR DEFECTO
================================================================================

  Rol      Usuario    Contraseña
  -------  ---------  ----------
  Admin    admin      admin123

  ⚠ Cambiar antes de desplegar en producción.


================================================================================
  ✨ FUNCIONALIDADES
================================================================================

  · Explorar catálogo de libros con búsqueda y filtro por género
  · Registrar estado de lectura: Quiero leer · Leyendo · Leído
  · Valorar libros y dejar comentarios
  · Panel de administración para gestionar el catálogo


================================================================================
  🔄 CI/CD — GITHUB ACTIONS
================================================================================

  Pipeline automático en cada push o pull request a main/master.

  · Job 1 — Arranca el backend y verifica que responde correctamente
  · Job 2 — Verifica la sintaxis del frontend
  · Job 3 — Construye y levanta los 3 contenedores Docker


================================================================================
  🧪 PRUEBAS
================================================================================

  Pruebas con Pytest organizadas en tests/backend/ y tests/frontend/.
  Se incluye también una colección Postman en docs/Bookshelf_Tests_Postman.json

  Para ejecutar:
    cd bookshelf_v3/backend
    pytest tests/ -v


================================================================================
  🔐 SEGURIDAD — OWASP TOP 10
================================================================================

  A01 · Control de acceso       Rutas protegidas con login y rol de admin
  A02 · Criptografía            Contraseñas con hash SHA-256 y salt
  A03 · Inyección               Consultas SQL parametrizadas
  A04 · Diseño inseguro         Rate limiting en el login (5 intentos/5 min)
  A05 · Configuración           Cabeceras HTTP de seguridad y debug=False
  A06 · Componentes             Versiones fijadas en requirements.txt
  A07 · Autenticación           Sesiones Flask y mensajes de error genéricos
  A08 · Integridad              Pipeline CI/CD que verifica cada commit
  A09 · Logging                 Registro de eventos de seguridad
  A10 · SSRF                    Riesgo bajo, mejora pendiente

================================================================================