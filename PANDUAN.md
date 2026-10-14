# 🎓 Panduan Lengkap: Aplikasi Pengaduan Kampus

Panduan langkah demi langkah dari nol sampai aplikasi jalan.
**Naufal Hafizh** — Pemrograman Perangkat Bergerak

---

## 📖 Daftar Isi
1. [Persiapan](#1-persiapan)
2. [Menjalankan Backend](#2-menjalankan-backend)
3. [Setup Flutter](#3-setup-flutter)
4. [Menjalankan Aplikasi](#4-menjalankan-aplikasi)
5. [Penjelasan Kode Inti](#5-penjelasan-kode-inti)
6. [Alur Data](#6-alur-data)

---

## 1. Persiapan

### Software yang dibutuhkan
| Software | Kegunaan | Status |
|----------|----------|--------|
| Node.js | Backend server | ✅ sudah ada |
| XAMPP (MySQL) | Database | ✅ sudah ada |
| Flutter SDK | Framework mobile | ⚠️ perlu install |
| Android Studio | Emulator + SDK | ✅ sudah ada |

### Struktur Proyek
```
pengaduan-kampus/
├── backend/     → server API (Node.js)
├── mobile/      → aplikasi (Flutter)
└── *.md         → dokumentasi
```

---

## 2. Menjalankan Backend

### Langkah:
1. **Buka XAMPP Control Panel** → klik **Start** di baris **MySQL**
2. Buka terminal, masuk folder backend:
   ```bash
   cd pengaduan-kampus/backend
   ```
3. Install dependency (sekali saja):
   ```bash
   npm install
   ```
4. Jalankan server:
   ```bash
   npm start
   ```
5. Jika berhasil, muncul:
   ```
   ✅ Database terhubung: pengaduan_kampus
   🚀 Server berjalan di http://localhost:3000
   ```

> ✅ Biarkan terminal ini terbuka. Backend harus tetap jalan.

---

## 3. Setup Flutter

### A. Extract Flutter
1. File `flutter_windows.zip` ada di folder Downloads
2. Extract ke `C:\Users\Naufal Hafizh\develop\` (buat folder `develop` dulu)
   - Klik kanan zip → **Extract All** → pilih `C:\Users\Naufal Hafizh\develop`
3. Hasilnya: `C:\Users\Naufal Hafizh\develop\flutter`

### B. Tambahkan Flutter ke PATH
1. Tekan **Windows + S** → cari "Environment Variables"
2. Klik **Edit the system environment variables**
3. Klik tombol **Environment Variables...**
4. Di bagian **User variables**, pilih **Path** → **Edit**
5. Klik **New** → masukkan:
   ```
   C:\Users\Naufal Hafizh\develop\flutter\bin
   ```
6. Klik **OK** di semua jendela
7. **Tutup dan buka ulang** terminal

### C. Verifikasi
```bash
flutter --version
flutter doctor
```

`flutter doctor` akan menunjukkan apa yang perlu diperbaiki.
Yang penting hijau ✅:
- Flutter SDK
- Android toolchain
- Android Studio

### D. Setujui lisensi Android (sekali saja)
```bash
flutter doctor --android-licenses
```
Ketik `y` untuk semua.

---

## 4. Menjalankan Aplikasi

### A. Siapkan Emulator
1. Buka **Android Studio**
2. Menu **Device Manager** (ikon HP di kanan)
3. Klik **Create Device** → pilih **Pixel 6** → **Next**
4. Pilih system image (misal **Android 13 / API 33**) → download → **Finish**
5. Klik ▶️ untuk menyalakan emulator

### B. Install dependency Flutter
```bash
cd pengaduan-kampus/mobile
flutter pub get
```

### C. Cek perangkat
```bash
flutter devices
```
Pastikan emulator muncul.

### D. Jalankan!
```bash
flutter run
```

Tunggu proses build (pertama kali agak lama, 2-5 menit).
Aplikasi akan muncul di emulator. 🎉

---

## 5. Penjelasan Kode Inti

### 🔹 Model (`models/`)
Kelas Dart untuk merepresentasikan data dari API.
```dart
// Konversi JSON dari API → object Dart
factory Pengaduan.fromJson(Map<String, dynamic> json) { ... }
```

### 🔹 Service (`services/`)
Tempat semua request HTTP ke backend.
```dart
// Contoh: login
static Future<User> login({required String email, required String password}) async {
  final res = await http.post(Uri.parse(ApiConfig.login), ...);
  ...
}
```

### 🔹 Konfigurasi API (`config/api.dart`)
**File paling penting untuk diubah!** Menentukan alamat server.
```dart
static const String baseUrl = 'http://10.0.2.2:3000'; // emulator
```

### 🔹 Screens (`screens/`)
Setiap file = satu halaman aplikasi.
- `splash_screen.dart` → cek login otomatis
- `login_screen.dart` → form login
- `home_screen.dart` → daftar laporan
- `buat_laporan_screen.dart` → form buat laporan
- `detail_screen.dart` → detail + admin ubah status

---

## 6. Alur Data

Contoh alur **Login**:
```
[User isi email+password]
        │
        ▼
[LoginScreen._login()]  (screens/login_screen.dart)
        │
        ▼
[AuthService.login()]   (services/auth_service.dart)
        │  http.post → /api/auth/login
        ▼
[SERVER: routes/auth.js]
        │  1. cari user by email
        │  2. bcrypt.compare password
        │  3. buat JWT token
        ▼
[Balik ke app: token + data user]
        │
        ▼
[Simpan token di SharedPreferences]
        │
        ▼
[Pindah ke HomeScreen]
```

Contoh alur **Buat Laporan**:
```
[User isi form + foto]
        │
        ▼
[PengaduanService.buat()]  → multipart/form-data
        │
        ▼
[SERVER: routes/pengaduan.js]
        │  1. cek token (middleware auth)
        │  2. simpan foto (multer)
        │  3. INSERT ke database
        ▼
[Laporan tersimpan, status = "Menunggu"]
```

---

## 🎯 Ringkasan Perintah Penting

```bash
# Backend
cd backend && npm start

# Flutter
cd mobile
flutter pub get          # install dependency
flutter devices          # cek perangkat
flutter run              # jalankan app
flutter build apk        # bikin file APK
```

---

## 💡 Tips untuk Laporan Tugas
1. **Screenshot** setiap halaman aplikasi (login, home, buat, detail)
2. **Screenshot** hasil `flutter doctor`
3. Jelaskan **arsitektur client-server** dan **REST API**
4. Sertakan **ERD database** (lihat `DOKUMENTASI_DATABASE.md`)
5. Jelaskan **fitur** dan **cara kerja** tiap bagian
6. Tunjukkan **bukti API jalan** (hasil `test-api.sh`)
