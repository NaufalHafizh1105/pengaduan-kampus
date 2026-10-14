# 🚀 Backend — API Pengaduan Fasilitas Kampus

REST API untuk aplikasi pengaduan fasilitas kampus.
Tugas Mata Kuliah **Pemrograman Perangkat Bergerak**.

## 🧰 Teknologi
- **Node.js + Express** — web framework
- **MySQL / MariaDB (XAMPP)** — database
- **JWT (jsonwebtoken)** — autentikasi token
- **bcryptjs** — hash password
- **multer** — upload foto

## 📁 Struktur Folder
```
backend/
├── src/
│   ├── config/db.js          # koneksi database (connection pool)
│   ├── middleware/
│   │   ├── auth.js           # cek token JWT & role admin
│   │   └── upload.js         # upload foto (multer)
│   ├── routes/
│   │   ├── auth.js           # register, login, profil
│   │   └── pengaduan.js      # CRUD laporan pengaduan
│   └── server.js             # entry point
├── database/schema.sql       # skema + data awal
├── uploads/                  # foto yang di-upload
├── .env                      # konfigurasi (JANGAN di-commit)
└── package.json
```

## ⚙️ Cara Menjalankan

### 1. Pastikan MySQL XAMPP menyala
Buka **XAMPP Control Panel** → klik **Start** pada MySQL.

### 2. Buat database
```bash
# dari folder backend
"C:/xampp/mysql/bin/mysql.exe" -u root < database/schema.sql
```

### 3. Install dependency
```bash
npm install
```

### 4. Jalankan server
```bash
npm start          # atau: npm run dev (auto-reload)
```
Server jalan di **http://localhost:3000**

## 🔌 Daftar Endpoint

| Method | Endpoint | Akses | Fungsi |
|--------|----------|-------|--------|
| POST | `/api/auth/register` | Publik | Daftar akun baru |
| POST | `/api/auth/login` | Publik | Login, dapat token |
| GET | `/api/auth/me` | Login | Profil user saat ini |
| GET | `/api/pengaduan` | Login | Daftar laporan (mahasiswa: miliknya, admin: semua) |
| GET | `/api/pengaduan/:id` | Login | Detail laporan |
| POST | `/api/pengaduan` | Login | Buat laporan (multipart, foto opsional) |
| PUT | `/api/pengaduan/:id/status` | Admin | Ubah status + catatan |
| DELETE | `/api/pengaduan/:id` | Login | Hapus laporan |

## 🧪 Cara Tes Cepat
Jalankan script tes otomatis:
```bash
bash test-api.sh
```

Atau tes manual:
```bash
# Register
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nama":"Budi","email":"budi@mhs.ac.id","password":"123456","nim":"2021002"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"budi@mhs.ac.id","password":"123456"}'
```

## 🔑 Akun Default
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@kampus.ac.id | admin123 |

## 📝 Catatan untuk Laporan Tugas
- **Arsitektur:** Client–Server (REST API)
- **Autentikasi:** JWT (JSON Web Token), password di-hash bcrypt
- **Upload file:** multipart/form-data via multer
- **Status laporan:** Menunggu → Diproses → Selesai / Ditolak
- **Kategori:** Fasilitas, Kebersihan, Keamanan, Akademik, Lainnya
