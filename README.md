# Anupam Bearings — Premium Industrial Website

A full-stack Django website for Anupam Bearings, a certified Timken parts supplier based in Bengaluru and Chennai.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Django Templates + Custom CSS |
| Animations | GSAP 3 (ScrollTrigger) |
| Chatbot | Ollama3 (local LLM) |
| Email | Resend API |

---

## Quick Start

### 1. Clone & Install

```bash
cd anupam_bearings
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Database Setup

**SQLite (default for dev):**
```bash
python manage.py migrate
python manage.py seed_data   # Loads all 30+ products from catalogue
python manage.py createsuperuser
```

**PostgreSQL (production):**
```bash
# Update .env with DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
python manage.py migrate
python manage.py seed_data
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Features

### Pages
- **Home** — Cinematic intro animation, 3-slide hero, featured products, about preview, features grid, CTA
- **About** — Leadership, services, Timken history timeline, India footprint
- **Products** — Category tabs (desktop) / Accordion (mobile), enquiry modal, 30+ seeded products
- **Gallery** — Filterable masonry grid with lightbox
- **Contact** — Form with Resend email, dual office info, embedded Google Maps

### Design System (DESIGN.md)
- **No-Line Rule** — Surface tonal shifts instead of borders
- **Glassmorphism** — Nav and chatbot use `backdrop-filter: blur(12px)`
- **Machined Gradient** — `#a14000` → `#ff6a00` for all CTAs
- **Ghost Shadow** — `0px 20px 40px rgba(27,27,31,0.06)` for floating elements
- **Typography** — Space Grotesk (display) + Inter (body)

### Animations
- Cinematic SVG bearing intro (sessionStorage, runs once)
- GSAP ScrollTrigger: fade-up, slide-in, stagger, scale
- Hero slider with auto-advance, swipe support
- Chatbot pulse animation + smooth panel reveal
- Navbar height contraction on scroll (80px → 64px)
- Gallery filter transitions

### AI Chatbot (Ollama3)
- Floating bottom-right widget with pulse animation
- Context-injected with all company/product info
- Full chat history maintained per session
- Graceful fallback if Ollama is offline

### Email (Resend)
- Product enquiries → company notification
- Contact form → company notification
- Configure `RESEND_API_KEY` in `.env`

---

## Ollama Setup (AI Chatbot)

```bash
# Install Ollama: https://ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the model
ollama pull llama3

# Ollama runs automatically, or start manually:
ollama serve
```

The chatbot gracefully shows a contact fallback message if Ollama is offline.

---

## PostgreSQL Setup (Production)

```bash
# Create database
createdb anupam_bearings_db

# Update .env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=anupam_bearings_db
DB_USER=your_pg_user
DB_PASSWORD=your_pg_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Admin Panel

Access at `/admin/` after creating a superuser.

Manage:
- **Products** → Categories, Products, Enquiries
- **Contact** → ContactMessage, ChatMessage

---

## Project Structure

```
anupam_bearings/
├── anupam_bearings/       # Django project config
│   ├── settings.py
│   └── urls.py
├── core/                  # Home, About, Gallery views
├── products/              # Products, Enquiry models & views
│   └── management/commands/seed_data.py
├── contact/               # Contact form, ChatMessage
├── chatbot/               # Ollama AI chat endpoint
├── static/
│   ├── css/main.css       # Full design system
│   ├── js/main.js         # GSAP animations, slider, chatbot
│   └── images/logo.png
├── templates/
│   ├── base.html          # Nav, Footer, Chatbot, Modals
│   ├── core/              # home.html, about.html, gallery.html
│   ├── products/          # product_list.html
│   └── contact/           # contact.html
├── .env.example
├── requirements.txt
└── README.md
```

---

## Customization

### Adding Products
Via Admin Panel at `/admin/products/product/add/` or `seed_data.py`

### Changing Colors
Edit CSS variables in `static/css/main.css` under `:root`

### Updating Chatbot Context
Edit `SYSTEM_CONTEXT` in `chatbot/views.py`

### Logo
Replace `static/images/logo.png` with your new logo (maintain transparent background)
