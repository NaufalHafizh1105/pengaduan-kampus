// =========================================================
//  Konfigurasi API
//  baseUrl otomatis menyesuaikan tempat app dijalankan
// =========================================================
import 'package:flutter/foundation.dart' show kIsWeb;

class ApiConfig {
  // ── Atur IP komputer di sini (untuk HP fisik) ──
  // Cek dengan perintah: ipconfig  → lihat "IPv4 Address"
  static const String _ipKomputer = '192.168.1.10';

  // ── baseUrl otomatis ──
  // 1. Flutter Web (Chrome)  → localhost
  // 2. Android emulator      → 10.0.2.2 (alias localhost PC)
  // 3. HP fisik              → ganti ke 'http://$_ipKomputer:3000'
  static String get baseUrl {
    if (kIsWeb) return 'http://localhost:3000';
    return 'http://10.0.2.2:3000';
  }

  // ── Endpoint ──
  static String get register => '$baseUrl/api/auth/register';
  static String get login => '$baseUrl/api/auth/login';
  static String get me => '$baseUrl/api/auth/me';
  static String get pengaduan => '$baseUrl/api/pengaduan';

  // URL lengkap untuk menampilkan foto yang di-upload
  static String fotoUrl(String filename) => '$baseUrl/uploads/$filename';
}
