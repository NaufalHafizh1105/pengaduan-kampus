# 📱 Proyek: Aplikasi Pengaduan Fasilitas Kampus

**Pemilik:** Naufal Hafizh (Abah)
**Mata Kuliah:** Pemrograman Perangkat Bergerak
**Tujuan:** Aplikasi client-server untuk melaporkan keluhan fasilitas kampus

---

## 🏗️ Arsitektur

```
┌─────────────────────┐   HTTP/JSON    ┌──────────────────────┐
│   APLIKASI FLUTTER   │ ◄───────────► │   SERVER NODE.JS      │
│   (Android)          │   REST API     │   Express + JWT       │
│                      │                │   MySQL (XAMPP)       │
└─────────────────────┘                └──────────────────────┘
```

## 📋 Stack Teknologi
| Bagian | Teknologi |
|--------|-----------|
| Mobile (client) | Flutter + Dart |
| Backend (server) | Node.js + Express |
| Database | MySQL / MariaDB (XAMPP) |
| Auth | JWT + bcrypt |
| Upload foto | multer (backend), image_picker (Flutter) |

## ✨ Fitur
1. **Login & Register** — mahasiswa & admin
2. **Buat Laporan** — judul, deskripsi, kategori, lokasi, foto
3. **Riwayat Laporan** — lihat laporan sendiri + statusnya
4. **Detail Laporan** — lihat status & catatan admin
5. **(Admin)** Kelola semua laporan & ubah status

## 📊 Status Progres
- [x] **Tahap 1** — Cek environment
- [x] **Tahap 2** — Scaffold proyek
- [x] **Tahap 3** — Backend: database + koneksi
- [x] **Tahap 4** — Backend: API auth + laporan  ✅ TERUJI
- [ ] **Tahap 5** — Flutter: struktur + model + HTTP client
- [ ] **Tahap 6** — Flutter: UI Login & Register
- [ ] **Tahap 7** — Flutter: UI Home & Riwayat
- [ ] **Tahap 8** — Flutter: UI Buat Laporan
- [ ] **Tahap 9** — Testing end-to-end
- [ ] **Tahap 10** — Dokumentasi + laporan tugas

## 📁 Struktur Proyek
```
pengaduan-kampus/
├── backend/          # API Node.js + Express
│   ├── src/
│   ├── database/
│   └── uploads/
└── mobile/           # Aplikasi Flutter
    └── lib/
```

## 🔑 Akun Uji
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@kampus.ac.id | admin123 |
| Mahasiswa | naufal@mhs.ac.id | 123456 |

## 🚀 Cara Menjalankan
1. **MySQL** — Start MySQL di XAMPP Control Panel
2. **Backend** — `cd backend && npm start`
3. **Flutter** — `cd mobile && flutter run`
