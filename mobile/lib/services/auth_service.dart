// =========================================================
//  Service: Auth (register, login, profil, simpan token)
// =========================================================
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/api.dart';
import '../models/user.dart';

class AuthService {
  static const String _tokenKey = 'token';
  static const String _userKey = 'user';

  // ── REGISTER ──
  // Mengembalikan pesan sukses atau melempar Exception berisi pesan error
  static Future<String> register({
    required String nama,
    required String email,
    required String password,
    String? nim,
  }) async {
    final res = await http.post(
      Uri.parse(ApiConfig.register),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'nama': nama,
        'email': email,
        'password': password,
        if (nim != null && nim.isNotEmpty) 'nim': nim,
      }),
    );

    final data = jsonDecode(res.body);
    if (res.statusCode == 201) return data['message'] ?? 'Registrasi berhasil';
    throw Exception(data['message'] ?? 'Registrasi gagal');
  }

  // ── LOGIN ──
  static Future<User> login({
    required String email,
    required String password,
  }) async {
    final res = await http.post(
      Uri.parse(ApiConfig.login),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    final data = jsonDecode(res.body);
    if (res.statusCode == 200) {
      final user = User.fromJson(data['user']);
      // Simpan token & user ke penyimpanan HP
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_tokenKey, data['token']);
      await prefs.setString(_userKey, jsonEncode(data['user']));
      return user;
    }
    throw Exception(data['message'] ?? 'Login gagal');
  }

  // ── Ambil token tersimpan ──
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  // ── Ambil user tersimpan (untuk auto-login) ──
  static Future<User?> getUser() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_userKey);
    if (raw == null) return null;
    return User.fromJson(jsonDecode(raw));
  }

  // ── Logout ──
  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_userKey);
  }
}
