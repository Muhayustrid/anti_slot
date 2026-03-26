# 🎰 AntiSlot - Deteksi Judi Online di Komentar YouTube

Sistem deteksi otomatis untuk mengidentifikasi komentar spam promosi judi online pada video YouTube menggunakan Machine Learning (scikit-learn) dan AI (LLM).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Tech Stack](#-tech-stack)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Konfigurasi Environment Variables](#-konfigurasi-environment-variables)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Struktur Project](#-struktur-project)
- [Preview Aplikasi](#-preview-aplikasi)
- [API Keys Setup](#-api-keys-setup)
- [Deployment](#-deployment)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---

## 🚀 Fitur

### 1. **Deteksi Spam Judi Online**
- Analisis komentar YouTube menggunakan Machine Learning (SVM, SGD Classifier)
- Deteksi promosi judi dengan berbagai teknik penyamaran (homoglyph, alay, simbol)
- Akurasi tinggi dengan model yang sudah di-training

### 2. **AI Insight**
- Analisis mendalam menggunakan LLM (OpenRouter)
- Identifikasi pola spam dan modus promosi
- Deteksi false positive (komentar yang salah deteksi)

### 3. **Moderasi Komentar**
- Login dengan akun YouTube (OAuth 2.0)
- Hapus/reject komentar spam secara massal
- Ban user yang menyebarkan spam

### 4. **Dashboard Video**
- Lihat semua video dari channel Anda
- Filter video berdasarkan waktu
- Statistik komentar per video

---

## 🛠 Tech Stack

| Kategori | Teknologi |
|----------|-----------|
| **Backend** | Django 5.2, Python 3.10+ |
| **Machine Learning** | scikit-learn 1.7, joblib |
| **AI/LLM** | OpenRouter API (model gratis) |
| **API** | YouTube Data API v3, Google OAuth 2.0 |
| **Frontend** | HTML, CSS, JavaScript, HTMX |
| **Database** | SQLite (development), PostgreSQL (production) |
| **Deployment** | Railway, Gunicorn, WhiteNoise |

---

## 📦 Prasyarat

Sebelum memulai, pastikan Anda memiliki:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Package manager Python (otomatis terinstall dengan Python)
- **Git** - [Download Git](https://git-scm.com/)
- **Google Cloud Account** - Untuk YouTube API & OAuth
- **OpenRouter Account** - Untuk AI/LLM (gratis)

---

## 🔧 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/Muhayustrid/anti_slot.git
cd anti_slot
```

### 2. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd Pendeteksi_Judol
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Buat file `.env` di folder `Pendeteksi_Judol/`:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Kemudian edit file `.env` dengan konfigurasi Anda (lihat [Konfigurasi Environment Variables](#-konfigurasi-environment-variables)).

### 5. Jalankan Migrasi Database

```bash
python manage.py migrate
```

### 6. Jalankan Server

```bash
python manage.py runserver
```

Buka browser dan akses: **http://127.0.0.1:8000**

---

## ⚙️ Konfigurasi Environment Variables

Buat file `.env` di folder `Pendeteksi_Judol/` dengan format berikut:

```env
# ============================================
# DJANGO SETTINGS
# ============================================
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=1  # Gunakan 1 untuk development, 0 untuk production

# ============================================
# YOUTUBE DATA API v3
# ============================================
YOUTUBE_API_KEY=AIzaSy...your-api-key

# ============================================
# GOOGLE OAUTH 2.0
# ============================================
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_OAUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_OAUTH_REDIRECT_URIS=http://127.0.0.1:8000/oauth/callback/,http://localhost:8000/oauth/callback/

# ============================================
# OPENROUTER LLM API
# ============================================
OPENROUTER_API_KEY=sk-or-v1-...your-api-key
```

---

## 🏃 Menjalankan Aplikasi

### Development Mode

```bash
# Aktifkan virtual environment terlebih dahulu
cd Pendeteksi_Judol

# Jalankan development server
python manage.py runserver

# Server akan berjalan di http://127.0.0.1:8000
```

### Production Mode

```bash
# Set DEBUG=0 di file .env
DJANGO_DEBUG=0

# Collect static files
python manage.py collectstatic

# Jalankan dengan Gunicorn
gunicorn Pendeteksi_Judol.wsgi:application --bind 0.0.0.0:8000
```

### Perintah Berguna Lainnya

```bash
# Buat superuser (admin)
python manage.py createsuperuser

# Jalankan migrasi
python manage.py migrate

# Buat migrasi baru setelah mengubah models
python manage.py makemigrations

# Buka Django Shell
python manage.py shell

# Jalankan tests
python manage.py test
```

---

## 📁 Struktur Project

```
Pendeteksi_Judol/
├── Pendeteksi_Judol/          # Konfigurasi project Django
│   ├── settings.py            # Pengaturan Django
│   ├── urls.py                # URL routing utama
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
│
├── deteksi/                   # App utama untuk deteksi
│   ├── models.py              # Database models
│   ├── views.py               # Views/controllers
│   ├── urls.py                # URL routing app
│   ├── admin.py               # Admin configuration
│   │
│   ├── services/              # Business logic
│   │   ├── youtube.py         # YouTube API integration
│   │   ├── ai_insight.py      # LLM/AI analysis
│   │   ├── comment_processing.py  # Comment processing
│   │   └── orchestrator.py    # Service orchestrator
│   │
│   ├── ml/                    # Machine Learning
│   │   ├── predict.py         # Prediction logic
│   │   ├── preprocess.py      # Text preprocessing
│   │   ├── utils_text.py      # Text utilities
│   │   ├── model/             # Trained ML models (.joblib)
│   │   └── asset/             # ML assets (kamuses, lexicons)
│   │
│   ├── llm/                   # LLM integration
│   │   └── openrouter_client.py  # OpenRouter API client
│   │
│   ├── templates/             # HTML templates
│   │   └── html/
│   │       ├── index.html     # Halaman utama
│   │       ├── video_saya.html  # Halaman video saya
│   │       └── partials/      # Template components
│   │
│   └── templatetags/          # Custom template tags
│       └── mathx.py           # Math filters
│
├── static/                    # Static files
│   ├── css/                   # Stylesheets
│   │   └── style.css          # Main stylesheet
│   ├── js/                    # JavaScript
│   │   └── main.js            # Main script
│   └── assets/                # Images & assets
│       └── image/
│
├── templates/                 # Base templates
│   ├── base.html              # Base template
│   ├── privacy.html           # Privacy policy
│   └── terms.html             # Terms of service
│
├── dataset/                   # Training dataset
│   └── dataset_training.csv
│
├── .env                       # Environment variables (tidak di-commit)
├── client_secret.json         # Google OAuth credentials
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway deployment config
├── runtime.txt                # Python version untuk deployment
└── README.md                  # Dokumentasi ini
```

---

## 🖼️ Preview Aplikasi

### 1. Halaman Utama (Beranda)

Halaman utama untuk memasukkan URL video YouTube dan melakukan analisis komentar.

![Tampilan Utama](static/assets/image/tampilan_web/tampilan_utama.png)

### 2. Hasil Analisis

Tampilan hasil deteksi komentar spam judi online dengan statistik dan AI insight.

![Hasil Analisis](static/assets/image/tampilan_web/tampilan_utama_hasil.png)

### 3. Halaman Video Saya

Dashboard untuk melihat dan mengelola video dari channel YouTube yang terhubung.

![Halaman Video Saya](static/assets/image/tampilan_web/halaman_video_saya.png)

---

## 🔑 API Keys Setup

### 1. YouTube Data API v3

1. Buka [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru atau pilih project yang ada
3. Aktifkan **YouTube Data API v3**:
   - Menu: `APIs & Services` → `Library`
   - Cari "YouTube Data API v3" → Klik `Enable`
4. Buat API Key:
   - Menu: `APIs & Services` → `Credentials`
   - Klik `+ CREATE CREDENTIALS` → `API Key`
   - Copy API Key ke file `.env`

### 2. Google OAuth 2.0

1. Di Google Cloud Console yang sama:
2. Buat OAuth Client ID:
   - Menu: `APIs & Services` → `Credentials`
   - Klik `+ CREATE CREDENTIALS` → `OAuth client ID`
   - Application type: `Web application`
   - Authorized redirect URIs:
     - `http://127.0.0.1:8000/oauth/callback/`
     - `http://localhost:8000/oauth/callback/`
3. Download JSON credentials atau copy Client ID & Secret ke file `.env`

### 3. OpenRouter API (LLM)

1. Daftar di [OpenRouter.ai](https://openrouter.ai/)
2. Login dan buka dashboard
3. Klik `Create Key` untuk membuat API key baru
4. Copy API key ke file `.env`

> **Note:** OpenRouter menyediakan model-model LLM gratis yang bisa digunakan untuk analisis AI.

---

## 🚀 Deployment

### Deploy ke Railway

1. Push code ke GitHub
2. Login ke [Railway](https://railway.app/)
3. Klik `New Project` → `Deploy from GitHub repo`
4. Pilih repository Anda
5. Tambahkan environment variables di Railway dashboard
6. Railway akan otomatis deploy aplikasi Anda

### Deploy Manual (VPS)

```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Run dengan Gunicorn
gunicorn Pendeteksi_Judol.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
```

---

## 🤝 Kontribusi

Jika ingin berkontribusi silakan

---

## 📝 Catatan Penting

- **Jangan commit file `.env`** - File ini berisi API keys dan credentials sensitif
- **Jangan commit `client_secret.json`** - Berisi OAuth credentials
- **Gunakan virtual environment** - Untuk mengisolasi dependencies
- **Update `requirements.txt`** - Setelah install package baru: `pip freeze > requirements.txt`

---

## 📄 Lisensi

Dibuat oleh [Muhayustrid](https://github.com/Muhayustrid)

---

## 📧 Kontak

Jika ada pertanyaan atau saran, silakan buka [Issue](https://github.com/Muhayustrid/anti_slot/issues) di repository ini.

---

**⭐ Jika project ini bermanfaat, jangan lupa berikan star ya!**
