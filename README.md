# Affiliate Web

Aplikasi web katalog produk afiliasi menggunakan Django dan PostgreSQL. Fitur utama mencakup manajemen produk, kategori, pencarian, filter, serta tampilan publik yang responsif dan SEO-friendly.

## Fitur

- Autentikasi admin (login/logout)
- CRUD produk afiliasi dan kategori
- Upload dan pratinjau gambar produk
- Pencarian dan filter kategori
- Meta tag SEO otomatis
- Tampilan publik dengan Tailwind CSS CDN
- Responsif untuk semua perangkat

## Stack Teknologi

- Django 
- PostgreSQL
- Tailwind CSS (CDN)
- Bootstrap Icons
- Python 

## Struktur Folder
`
affiliate_web/
├── affiliate_app/
├── templates/
├── static/
├── media/
├── manage.py
└── db.sqlite3 (jika tidak menggunakan PostgreSQL)
`

## Instalasi

1. Clone repo:
   `git clone https://github.com/FahmiHeykal/affiliate_web.git`

2. Masuk direktori:
   `cd affiliate_web`

3. Aktifkan virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependensi:
   `pip install -r requirements.txt`

5. Migrasi database:
   `python manage.py migrate`

6. Buat superuser:
   `python manage.py createsuperuser`

7. Jalankan server:
   `python manage.py runserver`

Buka di browser: `http://127.0.0.1:8000`

## Pengembangan Lanjutan

- Tracking klik afiliasi
- Fitur upload multiple gambar
- Sorting produk
- Sitemap XML dan robots.txt
- Google Analytics integrasi
