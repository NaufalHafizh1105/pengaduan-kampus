// =========================================================
//  Tema & warna aplikasi
// =========================================================
import 'package:flutter/material.dart';

class AppTheme {
  static const Color primary = Color(0xFF1565C0);   // biru
  static const Color secondary = Color(0xFF26A69A); // teal

  static ThemeData get light => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: primary),
        scaffoldBackgroundColor: const Color(0xFFF5F7FA),
        appBarTheme: const AppBarTheme(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          elevation: 0,
          centerTitle: true,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: primary,
            foregroundColor: Colors.white,
            minimumSize: const Size.fromHeight(52),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
        ),
      );

  // Warna badge sesuai status laporan
  static Color statusColor(String status) {
    switch (status) {
      case 'Menunggu':
        return Colors.orange;
      case 'Diproses':
        return Colors.blue;
      case 'Selesai':
        return Colors.green;
      case 'Ditolak':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  static IconData statusIcon(String status) {
    switch (status) {
      case 'Menunggu':
        return Icons.hourglass_empty;
      case 'Diproses':
        return Icons.autorenew;
      case 'Selesai':
        return Icons.check_circle;
      case 'Ditolak':
        return Icons.cancel;
      default:
        return Icons.help_outline;
    }
  }
}
