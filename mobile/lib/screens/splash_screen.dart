// =========================================================
//  Splash Screen — cek login otomatis, lalu arahkan
// =========================================================
import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../utils/theme.dart';
import 'login_screen.dart';
import 'home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _cekLogin();
  }

  Future<void> _cekLogin() async {
    await Future.delayed(const Duration(seconds: 2));
    final user = await AuthService.getUser();
    if (!mounted) return;

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => user != null ? const HomeScreen() : const LoginScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.primary,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.15),
                    blurRadius: 16,
                    offset: const Offset(0, 6),
                  ),
                ],
              ),
              child: Image.asset(
                'assets/logo_umb.png',
                width: 96,
                height: 96,
                fit: BoxFit.contain,
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Pengaduan Kampus',
              style: TextStyle(
                color: Colors.white,
                fontSize: 26,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Laporkan keluhan fasilitas kampus',
              style: TextStyle(color: Colors.white.withValues(alpha: 0.8), fontSize: 14),
            ),
            const SizedBox(height: 6),
            Text(
              'Universitas Muhammadiyah Bandung',
              style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 12),
            ),
            const SizedBox(height: 40),
            const CircularProgressIndicator(color: Colors.white),
          ],
        ),
      ),
    );
  }
}
