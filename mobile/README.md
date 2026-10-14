# 📱 Mobile — Aplikasi Pengaduan Kampus (Flutter)

Aplikasi client (mobile) untuk pengaduan fasilitas kampus.
Tugas Mata Kuliah **Pemrograman Perangkat Bergerak**.

## 🧰 Teknologi
- **Flutter** — framework mobile (Dart)
- **http** — request ke REST API
- **shared_preferences** — simpan token login
- **image_picker** — ambil foto dari kamera/galeri
- **intl** — format tanggal

## 📁 Struktur Folder
```
mobile/lib/
├── main.dart                    # titik masuk aplikasi
├── config/
│   └── api.dart                 # ⚙️ KONFIGURASI URL API (penting!)
├── models/
│   ├── user.dart                # model User
│   └── pengaduan.dart           # model Pengaduan
├── services/
│   ├── auth_service.dart        # register, login, logout
│   └── pengaduan_service.dart   # CRUD laporan
├── screens/
│   ├── splash_screen.dart       # cek login otomatis
│   ├── login_screen.dart        # halaman login
│   ├── register_screen.dart     # halaman daftar
│   ├── home_screen.dart         # daftar laporan + filter
│   ├── buat_laporan_screen.dart # form buat laporan
│   └── detail_screen.dart       # detail + ubah status (admin)
└── utils/
    └── theme.dart               # tema & warna
```

## ⚙️ Konfigurasi PENTING

Buka `lib/config/api.dart` dan **sesuaikan `baseUrl`** dengan cara kamu menjalankan app:

| Cara jalan | baseUrl |
|------------|---------|
| **Android Emulator** | `http://10.0.2.2:3000` |
| **HP fisik (WiFi sama)** | `http://192.168.x.x:3000` (lihat `ipconfig`) |
| **Chrome / Web** | `http://localhost:3000` |

> ⚠️ `10.0.2.2` adalah alamat khusus emulator Android untuk mengakses `localhost` komputer.

## 🚀 Cara Menjalankan

### 1. Backend harus jalan dulu
```bash
cd ../backend
npm start
```

### 2. Install dependency Flutter
```bash
cd mobile
flutter pub get
```

### 3. Cek perangkat tersedia
```bash
flutter devices
```

### 4. Jalankan aplikasi
```bash
flutter run
```

## 📱 Fitur
- ✅ Splash screen + auto-login (token tersimpan)
- ✅ Login & Register
- ✅ Daftar laporan + filter status
- ✅ Buat laporan (judul, kategori, lokasi, deskripsi, foto)
- ✅ Detail laporan + tampilkan foto
- ✅ Admin: ubah status + beri catatan
- ✅ Logout

## 🔑 Akun Uji
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@kampus.ac.id | admin123 |
| Mahasiswa | naufal@mhs.ac.id | 123456 |

## 🐛 Troubleshooting

**"Connection refused" / gagal konek API**
- Pastikan backend jalan (`npm start`)
- Pastikan `baseUrl` di `api.dart` sudah benar (emulator vs HP fisik)
- Untuk HP fisik: HP & PC harus di WiFi yang sama, dan firewall PC izinkan port 3000

**Foto tidak muncul**
- Pastikan backend menyajikan folder `/uploads`
- URL foto otomatis dibentuk dari `baseUrl`

**Android: izin internet**
- Sudah otomatis diatur di `AndroidManifest.xml`
