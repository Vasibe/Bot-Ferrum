# ferrum-bot

Bot de automatización web para la plataforma educativa Ferrum, desarrollado con **Python + Playwright** siguiendo **arquitectura hexagonal (DDD)**.

> Proyecto académico - Automatización de Interacción en Plataformas Educativas

---

## Flujo automatizado

```
Login → Dashboard → My Courses → ELECTIVA III → Evaluación Formativa → Taller Práctico
```

---

## Estructura del proyecto

```
ferrum-bot/
├── src/
│   ├── domain/          # Entidades, puertos, excepciones (DDD puro)
│   ├── application/     # Casos de uso
│   ├── infrastructure/  # Playwright, navegadores, adapters
│   └── config/          # Settings y variables de entorno
├── tests/
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ferrum-bot.git
cd ferrum-bot
```

### 2. Crear entorno virtual

```bash
python -m venv .venv

# Activar (Linux/Mac/Git Bash)
source .venv/bin/activate

# Activar (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configurar credenciales

```bash
cp .env.example .env
```

Crea un `.env` con tus credenciales reales:

```env
FERRUM_URL=https://ferrum.tecnologicocomfenalco.edu.co/ferrum
FERRUM_USERNAME=tu_usuario_real
FERRUM_PASSWORD=tu_contraseña_real
HEADLESS=false
SLOW_MO=100
```

> `.env` está en `.gitignore` — Git lo ignora completamente y **nunca se sube al repositorio**.

---

## Ejecución

```bash
python main.py
```

---

## Variables de entorno

| Variable          | Descripción                          | Ejemplo    |
| ----------------- | ------------------------------------ | ---------- |
| `FERRUM_URL`      | URL base de la plataforma            | `https://` |
| `FERRUM_USERNAME` | Usuario de Ferrum                    | `jdoe`     |
| `FERRUM_PASSWORD` | Contraseña                           | `secret`   |
| `HEADLESS`        | Ejecutar sin ventana visible         | `false`    |
| `SLOW_MO`         | Milisegundos de delay entre acciones | `100`      |

---

## Tecnologías

- **Python 3.11+**
- **Playwright** — automatización de navegador
- **python-dotenv** — manejo de variables de entorno
- **Arquitectura Hexagonal (DDD)** — separación de capas

---

## Seguridad

- Las credenciales se leen exclusivamente desde el archivo `.env`
- El `.env` está incluido en `.gitignore` y nunca se sube al repositorio
- Se incluye `.env.example` con estructura vacía para referencia
